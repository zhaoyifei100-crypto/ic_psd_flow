"""
Mock driver for testing without hardware.

This driver simulates I2C operations without requiring actual hardware.
Useful for development, testing, and CI/CD pipelines.
"""

from typing import List, Optional
from ..interfaces import IDevice


class MockDriver(IDevice):
    """
    Mock I2C driver for testing purposes.

    This driver stores all written values in memory and returns them
    when reading. It does not communicate with any actual hardware.

    Attributes:
        registers: Dictionary storing register values (key: (addr1, addr2))
        write_log: List of all write operations performed
        read_log: List of all read operations performed
    """

    def __init__(
        self,
        chip_addr: int = 0x58,
        default_value: int = 0x00,
        verbose: bool = True,
        **kwargs,
    ):
        """
        Initialize the Mock driver.

        Args:
            chip_addr: I2C device address (for interface compatibility)
            default_value: Default value for unread registers
            verbose: If True, print operations to stdout
            **kwargs: Additional parameters (ignored)
        """
        super().__init__(chip_addr=chip_addr)
        self._default_value = default_value & 0xFF
        self._verbose = verbose

        # Storage for register values
        self.registers: dict = {}

        # Operation logs
        self.write_log: List[tuple] = []
        self.read_log: List[tuple] = []

        # Statistics
        self._write_count = 0
        self._read_count = 0

    def open(self) -> None:
        """
        Open the mock device.

        This is a no-op for the mock driver, but sets the is_open flag.
        """
        self._is_open = True
        if self._verbose:
            print("[MOCK] Device opened")

    def close(self) -> None:
        """
        Close the mock device.

        Clears the is_open flag.
        """
        self._is_open = False
        if self._verbose:
            print("[MOCK] Device closed")

    def write_reg(self, addr1: int, addr2: int, value: int) -> None:
        """
        Write a value to a register.

        Stores the value in memory and logs the operation.

        Args:
            addr1: Page address / high byte
            addr2: Offset address / low byte
            value: Value to write (8-bit)
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        # Mask to 8-bit
        value = value & 0xFF

        # Store value
        key = (addr1, addr2)
        old_value = self.registers.get(key, self._default_value)
        self.registers[key] = value

        # Log operation
        self.write_log.append((addr1, addr2, value))
        self._write_count += 1

        if self._verbose:
            print(
                f"[MOCK] Write 0x{addr1:02X}{addr2:02X} = 0x{value:02X} "
                f"(was 0x{old_value:02X})"
            )

    def read_reg(self, addr1: int, addr2: int) -> int:
        """
        Read a value from a register.

        Returns the stored value or the default value if never written.

        Args:
            addr1: Page address / high byte
            addr2: Offset address / low byte

        Returns:
            int: The stored or default value
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        # Get value
        key = (addr1, addr2)
        value = self.registers.get(key, self._default_value)

        # Log operation
        self.read_log.append((addr1, addr2, value))
        self._read_count += 1

        if self._verbose:
            print(f"[MOCK] Read 0x{addr1:02X}{addr2:02X} = 0x{value:02X}")

        return value

    def get_register(self, addr1: int, addr2: int) -> Optional[int]:
        """
        Get the current value of a register without logging.

        Args:
            addr1: Page address / high byte
            addr2: Offset address / low byte

        Returns:
            int or None: The stored value, or None if never written
        """
        return self.registers.get((addr1, addr2))

    def set_register(self, addr1: int, addr2: int, value: int) -> None:
        """
        Set a register value directly without logging.

        This is useful for pre-configuring the mock state before tests.

        Args:
            addr1: Page address / high byte
            addr2: Offset address / low byte
            value: Value to set
        """
        self.registers[(addr1, addr2)] = value & 0xFF

    def clear_registers(self) -> None:
        """Clear all stored register values."""
        self.registers.clear()

    def clear_logs(self) -> None:
        """Clear operation logs."""
        self.write_log.clear()
        self.read_log.clear()
        self._write_count = 0
        self._read_count = 0

    def get_statistics(self) -> dict:
        """
        Get operation statistics.

        Returns:
            dict: Dictionary with 'writes', 'reads', 'total_operations'
        """
        return {
            "writes": self._write_count,
            "reads": self._read_count,
            "total_operations": self._write_count + self._read_count,
            "registers_defined": len(self.registers),
        }

    def dump_registers(self) -> None:
        """Print all defined registers and their values."""
        print("[MOCK] Register dump:")
        for (addr1, addr2), value in sorted(self.registers.items()):
            print(f"  0x{addr1:02X}{addr2:02X} = 0x{value:02X}")

    def write_page(self, addr_page: int, data_list: List[int]) -> None:
        """
        Write a full page efficiently.

        Args:
            addr_page: Page address
            data_list: List of bytes to write
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        if len(data_list) > 256:
            raise ValueError(f"Data list too long: {len(data_list)} bytes (max 256)")

        # Bulk write for efficiency
        for i, data in enumerate(data_list):
            key = (addr_page, i)
            self.registers[key] = data & 0xFF

        # Log as single operation
        self.write_log.append((addr_page, 0, len(data_list)))
        self._write_count += len(data_list)

        if self._verbose:
            print(f"[MOCK] Write page 0x{addr_page:02X}: {len(data_list)} bytes")
