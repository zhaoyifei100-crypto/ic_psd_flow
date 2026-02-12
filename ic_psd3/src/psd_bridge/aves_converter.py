"""
AVES Converter for PSD3 - Convert AVES scripts to Python class with DeviceManager support.

This script converts AVES scripts to a Python class that uses the new hw_bridge DeviceManager
for centralized device management, supporting multi-device configurations (e.g., TX/RX boards).

Usage:
    cd ic_psd3
    python -m src.psd_bridge.aves_converter
"""

import os
import re
from typing import Optional, List, Dict, Tuple


class AVESConverter:
    """Convert AVES scripts to Python class with DeviceManager support."""

    def __init__(
        self,
        aves_script_path: str,
        output_dir: str = "library",
        chip_name: str = "GSU1K1_NTO",
        class_name: str = "AVESChipConfig",
    ):
        """
        Initialize the AVES converter.

        Args:
            aves_script_path: Path to the AVES script file (e.g., gsu1001_2025_nto_scripts.txt)
            output_dir: Output directory for generated files
            chip_name: Chip name for register definition file
            class_name: Name of the generated Python class
        """
        self.aves_script_path = aves_script_path
        self.output_dir = output_dir
        self.chip_name = chip_name
        self.class_name = class_name
        self.output_file = "aves_class.py"
        self.c_header_file = f"{chip_name}_scripts.h"
        self.c_source_file = f"{chip_name}_scripts.c"

    def convert(self) -> None:
        """
        Main conversion entry point.
        Converts AVES script to Python class with DeviceManager support.
        """
        print(f"Converting AVES script: {self.aves_script_path}")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Parse AVES script
        functions = self._parse_aves_script()
        print(f"Found {len(functions)} functions")

        # Generate Python class
        self._generate_aves_class(functions)

        # Generate C header and source files
        self._generate_c_header(functions)
        self._generate_c_source(functions)

        print(f"Conversion completed!")
        print(f"  - Python class: {os.path.join(self.output_dir, self.output_file)}")
        print(f"  - C header: {os.path.join(self.output_dir, self.c_header_file)}")
        print(f"  - C source: {os.path.join(self.output_dir, self.c_source_file)}")

    def _parse_aves_script(self) -> List[Tuple[str, str, List[str]]]:
        """
        Parse AVES script and extract functions.

        Returns:
            List of tuples: (func_index, func_name, commands)
            Each command is a line from the AVES script
        """
        functions = []
        current_func = None
        current_commands = []

        with open(self.aves_script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            # Skip empty lines and comments (lines starting with ;)
            if not line or line.startswith(";"):
                continue

            # Check for function definition: :XX-XX Function Name:
            if line.startswith(":") and line.endswith(":"):
                # Save previous function if exists
                if current_func and current_commands:
                    functions.append(
                        (
                            current_func[0],  # index like "01-01"
                            current_func[1],  # name like "Chip Power Up"
                            current_commands,
                        )
                    )

                # Parse new function
                func_content = line[1:-1].strip()  # Remove : at start and end
                # Split into index and name (e.g., "01-01 Chip Power Up")
                # Support 2-4 segments with 2-3 digits each (e.g., 01-01, 01-01-02, 01-01-002, 01-01-02-02)
                match = re.match(r"(\d{2,3}(?:[-_]\d{2,3})+)\s+(.+)", func_content)
                if match:
                    func_index = match.group(1)
                    func_name = match.group(2)
                    current_func = (func_index, func_name)
                    current_commands = []
                else:
                    # Handle cases without index
                    current_func = ("00-00", func_content)
                    current_commands = []
                continue

            # Check for End keyword
            if line.lower() == "end":
                if current_func and current_commands:
                    functions.append(
                        (current_func[0], current_func[1], current_commands)
                    )
                    current_func = None
                    current_commands = []
                continue

            # Collect commands within function
            if current_func is not None:
                current_commands.append(line)

        # Handle last function if file doesn't end with End
        if current_func and current_commands:
            functions.append((current_func[0], current_func[1], current_commands))

        return functions

    def _sanitize_func_name(self, func_index: str, func_name: str) -> str:
        """
        Convert function name to valid Python identifier.
        Matches the behavior of old GetAVES.replace_func_name().

        Args:
            func_index: Function index like "01-01" or "01-01-02"
            func_name: Original function name

        Returns:
            Valid Python function name like "func_01_01_Chip_Power_Up"
        """
        # Replace hyphens with underscores in index
        index_part = func_index.replace("-", "_")

        # Sanitize function name - match old GetAVES behavior:
        # - Letters and numbers: keep as is
        # - Dot (.): replace with 'p'
        # - All other characters: replace with '_'
        name_chars = []
        for char in func_name:
            if char.isalnum():  # Keep letters and numbers
                name_chars.append(char)
            elif char == ".":  # Dot becomes 'p'
                name_chars.append("p")
            else:  # Everything else becomes '_'
                name_chars.append("_")

        name_part = "".join(name_chars)

        return f"func_{index_part}_{name_part}"

    def _parse_command(self, command: str) -> Optional[str]:
        """
        Parse an AVES command and convert to Python code.

        Args:
            command: AVES command line

        Returns:
            Python code string or None if not a valid command
        """
        # Handle include statements: include this "..." "XX-XX Function Name"
        # or: include "XX-XX Function Name"
        if command.startswith("include"):
            # Find all quoted strings in the command
            matches = re.findall(r'"([^"]+)"', command)
            if matches:
                # The last quoted string contains the function name
                called_func = matches[-1]
                # Try to match the function name pattern
                func_match = re.match(
                    r"(\d{2}[-_]\d{2}(?:[-_]\d{2})?)\s+(.+)", called_func
                )
                if func_match:
                    func_index = func_match.group(1)
                    func_name = func_match.group(2)
                    py_func_name = self._sanitize_func_name(func_index, func_name)
                    return f"self.{py_func_name}()"
            return None

        # Handle I2C write commands: XX XXXX XX ; comment
        # Format: DeviceAddr(2 hex) SubAddr(4 hex) Data(2 hex)
        # Note: DeviceAddr is the I2C chip address, already set in DeviceManager
        #       SubAddr is 16-bit, split into high byte (addr1) and low byte (addr2)
        # Example: B0 0902 13 -> write_reg(0x09, 0x02, 0x13)
        parts = command.split(";")
        cmd_part = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""

        # Split command into parts
        tokens = cmd_part.split()
        if len(tokens) >= 3:
            # Parse: B0 0902 13
            # device_addr = tokens[0]  # B0 - not used, already set in DeviceManager
            sub_addr = tokens[1]  # 0902 - 16-bit sub-address
            data = tokens[2]  # 13 - data value

            # Split 16-bit sub-address into high and low bytes
            # 0902 -> high=09, low=02
            sub_addr_high = sub_addr[0:2]  # First 2 chars (high byte)
            sub_addr_low = sub_addr[2:]  # Last 2 chars (low byte)

            # Convert to proper hex format
            addr1_hex = f"0x{sub_addr_high.lower()}"
            addr2_hex = f"0x{sub_addr_low.lower()}"
            data_hex = f"0x{data.lower()}"

            comment_str = f"  # {comment}" if comment else ""
            return (
                f"device.write_reg({addr1_hex}, {addr2_hex}, {data_hex}){comment_str}"
            )

        return None

    def _generate_c_header(self, functions: List[Tuple[str, str, List[str]]]) -> None:
        """
        Generate C header file with function declarations.

        Args:
            functions: List of parsed functions
        """
        output_path = os.path.join(self.output_dir, self.c_header_file)

        lines = []
        for func_index, func_name, _ in functions:
            func_c_name = self._sanitize_func_name(func_index, func_name)
            lines.append(f"void {func_c_name}();")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Generated: {output_path}")

    def _generate_c_source(self, functions: List[Tuple[str, str, List[str]]]) -> None:
        """
        Generate C source file with function implementations.

        Args:
            functions: List of parsed functions
        """
        output_path = os.path.join(self.output_dir, self.c_source_file)

        lines = []
        # Include header
        lines.append(f'#include "{self.c_header_file}"')

        for func_index, func_name, commands in functions:
            func_c_name = self._sanitize_func_name(func_index, func_name)

            # Function definition
            lines.append(f"void {func_c_name}(){{")

            # Generate commands
            for cmd in commands:
                c_cmd = self._parse_c_command(cmd)
                if c_cmd:
                    lines.append(f"    {c_cmd}")

            lines.append("}")
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Generated: {output_path}")

    def _parse_c_command(self, command: str) -> Optional[str]:
        """
        Parse an AVES command and convert to C code.

        Args:
            command: AVES command line

        Returns:
            C code string or None if not a valid command
        """
        # Handle include statements
        if command.startswith("include"):
            matches = re.findall(r'"([^"]+)"', command)
            if matches:
                called_func = matches[-1]
                func_match = re.match(
                    r"(\d{2}[-_]\d{2}(?:[-_]\d{2})?)\s+(.+)", called_func
                )
                if func_match:
                    func_index = func_match.group(1)
                    func_name = func_match.group(2)
                    c_func_name = self._sanitize_func_name(func_index, func_name)
                    return f"{c_func_name}();"
            return None

        # Handle I2C write commands: XX XXXX XX ; comment
        parts = command.split(";")
        cmd_part = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""

        tokens = cmd_part.split()
        if len(tokens) >= 3:
            # device_addr = tokens[0]  # Not used in C output
            sub_addr = tokens[1]
            data = tokens[2]

            # Split 16-bit sub-address
            sub_addr_high = sub_addr[0:2]
            sub_addr_low = sub_addr[2:] if len(sub_addr) > 2 else "00"

            comment_str = f" //{comment}" if comment else ""
            return f"writeReg(0x{sub_addr_high.lower()},0x{sub_addr_low.lower()},0x{data.lower()});{comment_str}"

        return None

    def _generate_aves_class(self, functions: List[Tuple[str, str, List[str]]]) -> None:
        """
        Generate the AVES configuration Python class.

        Args:
            functions: List of parsed functions
        """
        output_path = os.path.join(self.output_dir, self.output_file)

        # Build class content
        lines = []

        # Header and imports
        lines.append('"""')
        lines.append(f"{self.class_name} - AVES script configuration class")
        lines.append(f"Auto-generated from: {os.path.basename(self.aves_script_path)}")
        lines.append('"""')
        lines.append("")
        lines.append("from typing import Optional")
        lines.append("from hw_bridge import DeviceManager")
        lines.append("")
        lines.append("")
        lines.append(f"class {self.class_name}:")
        lines.append('    """')
        lines.append("    AVES script configuration for chip initialization.")
        lines.append("    ")
        lines.append(
            "    This class provides methods to configure the chip using I2C commands"
        )
        lines.append(
            "    converted from AVES scripts. It supports DeviceManager for centralized"
        )
        lines.append(
            "    device management, enabling multi-device configurations (e.g., TX/RX boards)."
        )
        lines.append("    ")
        lines.append("    Usage (DeviceManager mode - recommended):")
        lines.append("        >>> from hw_bridge import DeviceManager")
        lines.append("        >>> dm = DeviceManager(auto_open=True)")
        lines.append(
            '        >>> dm.register("tx", "ftdi", i2c_port=0, chip_addr=0x58)'
        )
        lines.append(
            '        >>> dm.register("rx", "ftdi", i2c_port=1, chip_addr=0x58)'
        )
        lines.append(
            '        >>> tx_config = AVESChipConfig(device_manager=dm, device_name="tx")'
        )
        lines.append(
            '        >>> rx_config = AVESChipConfig(device_manager=dm, device_name="rx")'
        )
        lines.append("        >>> tx_config.func_01_01_Chip_Power_Up()")
        lines.append('    """')
        lines.append("")
        lines.append("    def __init__(")
        lines.append("        self,")
        lines.append("        device_manager: Optional[DeviceManager] = None,")
        lines.append('        device_name: str = "chip"')
        lines.append("    ):")
        lines.append('        """')
        lines.append("        Initialize the AVES chip configuration.")
        lines.append("")
        lines.append("        Args:")
        lines.append(
            "            device_manager: DeviceManager instance for device access."
        )
        lines.append(
            "                           If None, you must set it before calling methods."
        )
        lines.append(
            "            device_name: Name of the device in the DeviceManager."
        )
        lines.append('        """')
        lines.append("        self._device_manager = device_manager")
        lines.append("        self._device_name = device_name")
        lines.append("")
        lines.append("    def _get_device(self):")
        lines.append('        """Get the device instance from DeviceManager."""')
        lines.append("        if self._device_manager is None:")
        lines.append(
            '            raise RuntimeError("DeviceManager not set. Initialize with device_manager parameter.")'
        )
        lines.append("        return self._device_manager[self._device_name]")
        lines.append("")
        lines.append(
            "    def set_device_manager(self, device_manager: DeviceManager, device_name: str = None):"
        )
        lines.append('        """')
        lines.append("        Set or update the DeviceManager.")
        lines.append("")
        lines.append("        Args:")
        lines.append("            device_manager: DeviceManager instance")
        lines.append("            device_name: Optional new device name")
        lines.append('        """')
        lines.append("        self._device_manager = device_manager")
        lines.append("        if device_name:")
        lines.append("            self._device_name = device_name")
        lines.append("")

        # Generate functions
        for func_index, func_name, commands in functions:
            py_func_name = self._sanitize_func_name(func_index, func_name)

            lines.append(f"    def {py_func_name}(self):")
            lines.append(f'        """{func_index} {func_name}"""')
            lines.append(f'        print("Cfg {py_func_name}...")')
            lines.append("        device = self._get_device()")

            for cmd in commands:
                py_cmd = self._parse_command(cmd)
                if py_cmd:
                    lines.append(f"        {py_cmd}")

            lines.append("")

        # Write to file
        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Generated: {output_path}")


def main():
    """Main entry point for command-line usage."""
    import sys

    # Default paths relative to ic_psd3
    aves_script = "import/gsu1001_2025_nto_scripts.txt"
    output_dir = "library"
    chip_name = "GSU1K1_NTO"

    # Allow command-line overrides
    if len(sys.argv) > 1:
        aves_script = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        chip_name = sys.argv[3]

    converter = AVESConverter(
        aves_script_path=aves_script, output_dir=output_dir, chip_name=chip_name
    )
    converter.convert()


if __name__ == "__main__":
    main()
