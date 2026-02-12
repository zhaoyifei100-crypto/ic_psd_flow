"""
Raspberry Pi I2C driver.

Linux I2C driver using i2ctransfer command-line tool.
Compatible with Raspberry Pi and other Linux I2C buses.
"""

import datetime
import subprocess
import time
from typing import List
from ..interfaces import IDevice


class RaspberryPiDriver(IDevice):
    """
    Raspberry Pi I2C driver using i2ctransfer.

    This driver uses the Linux i2ctransfer command-line tool to
    communicate with I2C devices on Raspberry Pi and other Linux systems.

    Requirements:
        - Linux system with I2C support
        - i2ctransfer tool (usually in i2c-tools package)
        - Appropriate permissions to access I2C bus

    Attributes:
        i2c_port: I2C bus number (e.g., 1 for /dev/i2c-1)
        chip_addr: I2C device address (7-bit format)
    """

    def __init__(
        self,
        i2c_port: int = 1,
        chip_addr: int = 0x58,
        aves_write: bool = False,
        aves_path: str = "./to_aves/",
        i2ctransfer_path: str = "/usr/sbin/i2ctransfer",
        **kwargs,
    ):
        """
        Initialize the Raspberry Pi driver.

        Args:
            i2c_port: I2C bus number (default: 1 for /dev/i2c-1)
            chip_addr: I2C device address in 7-bit format (default: 0x58)
            aves_write: Enable AVES script logging
            aves_path: Path for AVES script output
            i2ctransfer_path: Path to i2ctransfer executable
            **kwargs: Additional parameters (ignored)
        """
        super().__init__(chip_addr=chip_addr)
        self.i2c_port = i2c_port
        self.aves_write = aves_write
        self.i2ctransfer_path = i2ctransfer_path

        # Setup AVES logging
        if self.aves_write:
            import os

            os.makedirs(aves_path, exist_ok=True)
            now = datetime.datetime.now()
            StyleTime = now.strftime("%Y_%m_%d_%H_%M_%S")
            self.write_to = os.path.join(aves_path, f"aves_{StyleTime}.txt")
        else:
            self.write_to = None

    def _run_command(self, cmd: str) -> str:
        """
        Execute a shell command and return output.

        Args:
            cmd: Command string to execute

        Returns:
            str: Command output

        Raises:
            RuntimeError: If command fails
        """
        try:
            output = subprocess.check_output(
                cmd, shell=True, stderr=subprocess.STDOUT, encoding="utf-8"
            )
            return output.strip()
        except subprocess.CalledProcessError as e:
            error_msg = (
                f"Command failed (exit {e.returncode}): {cmd}\nOutput: {e.output}"
            )
            raise RuntimeError(error_msg)

    def open(self) -> None:
        """
        Open the I2C device.

        Verifies that the i2ctransfer tool is available.
        """
        # Check if i2ctransfer exists
        try:
            result = self._run_command(f"which {self.i2ctransfer_path}")
            if not result:
                raise RuntimeError(f"i2ctransfer not found at {self.i2ctransfer_path}")
        except RuntimeError:
            raise RuntimeError(
                f"i2ctransfer not found. Please install i2c-tools package.\n"
                f"Path checked: {self.i2ctransfer_path}"
            )

        self._is_open = True

    def close(self) -> None:
        """Close the I2C device (no-op for this driver)."""
        self._is_open = False

    def write_reg(self, addr1: int, addr2: int, value: int) -> None:
        """
        Write a value to a register.

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)
            value: Value to write (8-bit)

        Raises:
            RuntimeError: If write fails
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        # Build command: w3 = write 3 bytes
        write_cmd = (
            f"{self.i2ctransfer_path} -f -y {self.i2c_port} "
            f"w3@{hex(self.chip_addr)} "
            f"{hex(addr1)} {hex(addr2)} {hex(value)}"
        )

        # Retry on failure
        max_retries = 10
        for attempt in range(max_retries):
            try:
                self._run_command(write_cmd)
                break
            except RuntimeError as e:
                if attempt < max_retries - 1:
                    print(
                        f"[PI] Write failed, retrying ({attempt + 1}/{max_retries})..."
                    )
                    time.sleep(0.1)
                else:
                    raise RuntimeError(
                        f"Write failed after {max_retries} attempts: {e}"
                    )

        # Log to AVES if enabled
        if self.aves_write:
            self._log_to_aves(addr1, addr2, value)

    def read_reg(self, addr1: int, addr2: int) -> int:
        """
        Read a value from a register.

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)

        Returns:
            int: The 8-bit value read

        Raises:
            RuntimeError: If read fails
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        # Build command: w2 (write 2 bytes for address), r1 (read 1 byte)
        read_cmd = (
            f"{self.i2ctransfer_path} -f -y {self.i2c_port} "
            f"w2@{hex(self.chip_addr)} "
            f"{hex(addr1)} {hex(addr2)} "
            f"r1"
        )

        # Retry on failure
        max_retries = 10
        for attempt in range(max_retries):
            try:
                read_out = self._run_command(read_cmd)
                # Parse hex string to int
                return int(read_out, 16)
            except (RuntimeError, ValueError) as e:
                if attempt < max_retries - 1:
                    print(
                        f"[PI] Read failed, retrying ({attempt + 1}/{max_retries})..."
                    )
                    time.sleep(0.1)
                else:
                    raise RuntimeError(f"Read failed after {max_retries} attempts: {e}")

        return 0  # Should never reach here

    def _log_to_aves(self, addr1: int, addr2: int, value: int) -> None:
        """
        Log operation to AVES script file.

        Args:
            addr1: Page address
            addr2: Offset address
            value: Value written
        """
        if not self.write_to:
            return

        # Format: B0 0101 FF
        device_addr = f"{(self.chip_addr << 1):02x}"
        addr1_str = f"{addr1:02x}"
        addr2_str = f"{addr2:02x}"
        value_str = f"{value:02x}"

        print_str = f"{device_addr} {addr1_str}{addr2_str} {value_str};\n"

        with open(self.write_to, "a") as f:
            f.write(print_str)

    def write_bits(
        self, addr1: int, addr2: int, lsb: int, bits: int, value: int
    ) -> None:
        """
        Write specific bits to a register.

        Uses parent implementation.
        """
        super().write_bits(addr1, addr2, lsb, bits, value)

        # Also log to AVES if enabled
        if self.aves_write:
            # Read back to get final value for logging
            final_value = self.read_reg(addr1, addr2)
            self._log_to_aves(addr1, addr2, final_value)

    def read_bits(self, addr1: int, addr2: int, lsb: int, bits: int) -> int:
        """
        Read specific bits from a register.

        Uses parent implementation.
        """
        return super().read_bits(addr1, addr2, lsb, bits)

    def read_regs(self, addr1: int, addr2: int, num: int) -> List[int]:
        """
        Read multiple consecutive registers.

        Uses parent implementation.
        """
        return super().read_regs(addr1, addr2, num)
