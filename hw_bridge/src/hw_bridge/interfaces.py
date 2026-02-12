"""
Abstract interface definition for hardware devices.

All hardware drivers must implement this interface to ensure
compatibility with the hardware bridge library.
"""

from abc import ABC, abstractmethod
from typing import List


class IDevice(ABC):
    """
    Abstract base class for all hardware I2C devices.

    This interface defines the contract that all hardware drivers
    must follow, ensuring consistent behavior across different
    platforms (FTDI, Raspberry Pi, Mock, etc.).
    """

    def __init__(self, chip_addr: int = 0x58, **kwargs):
        """
        Initialize the device.

        Args:
            chip_addr: I2C device address (7-bit format, default 0x58)
            **kwargs: Additional driver-specific parameters
        """
        self.chip_addr = chip_addr
        self._is_open = False

    @abstractmethod
    def open(self) -> None:
        """
        Open the device connection.

        Raises:
            RuntimeError: If the connection cannot be established
            Exception: For other connection errors
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the device connection and release resources.
        """
        pass

    @abstractmethod
    def write_reg(self, addr1: int, addr2: int, value: int) -> None:
        """
        Write a value to a register.

        Uses 16-bit address format: addr1 (high byte) + addr2 (low byte)

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)
            value: Value to write (8-bit)

        Raises:
            RuntimeError: If the write operation fails
        """
        pass

    @abstractmethod
    def read_reg(self, addr1: int, addr2: int) -> int:
        """
        Read a value from a register.

        Uses 16-bit address format: addr1 (high byte) + addr2 (low byte)

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)

        Returns:
            int: The 8-bit value read from the register

        Raises:
            RuntimeError: If the read operation fails
        """
        pass

    def write_bits(
        self, addr1: int, addr2: int, lsb: int, bits: int, value: int
    ) -> None:
        """
        Write specific bits to a register without affecting other bits.

        This is a convenience method that reads the current value,
        modifies the specified bits, and writes back.

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)
            lsb: Least significant bit position (0-7)
            bits: Number of bits to write (1-8)
            value: Value to write (will be masked to fit in 'bits' width)

        Raises:
            RuntimeError: If the write operation fails
            ValueError: If bit parameters are invalid
        """
        # Convert bits count to bit mask
        bit_mask = self._bits_to_mask(bits)

        # Read current value
        old_value = self.read_reg(addr1, addr2)

        # Calculate new value
        shifted_value = (value & bit_mask) << lsb
        shifted_mask = bit_mask << lsb
        clear_mask = (~shifted_mask) & 0xFF

        # Clear target bits and set new value
        new_value = (old_value & clear_mask) | shifted_value

        # Write back
        self.write_reg(addr1, addr2, new_value)

    def read_bits(self, addr1: int, addr2: int, lsb: int, bits: int) -> int:
        """
        Read specific bits from a register.

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Offset address / low byte (8-bit)
            lsb: Least significant bit position (0-7)
            bits: Number of bits to read (1-8)

        Returns:
            int: The value of the specified bits

        Raises:
            RuntimeError: If the read operation fails
            ValueError: If bit parameters are invalid
        """
        # Convert bits count to bit mask
        bit_mask = self._bits_to_mask(bits)

        # Read current value
        old_value = self.read_reg(addr1, addr2)

        # Extract target bits
        shifted_mask = bit_mask << lsb
        masked_value = old_value & shifted_mask

        return masked_value >> lsb

    def read_regs(self, addr1: int, addr2: int, num: int) -> List[int]:
        """
        Read multiple consecutive registers.

        Args:
            addr1: Page address / high byte (8-bit)
            addr2: Starting offset address / low byte (8-bit)
            num: Number of registers to read

        Returns:
            List[int]: List of 8-bit values read from consecutive addresses

        Raises:
            RuntimeError: If any read operation fails
        """
        read_list = []
        for i in range(num):
            addr_loop = addr2 + i
            read_value = self.read_reg(addr1, addr_loop)
            read_list.append(read_value)
        return read_list

    def write_page(self, addr_page: int, data_list: List[int]) -> None:
        """
        Write a full page (256 bytes) to a page address.

        This is an optional method that may be overridden by drivers
        for optimized bulk writes. Default implementation writes
        bytes one by one.

        Args:
            addr_page: Page address (high byte)
            data_list: List of up to 256 bytes to write

        Raises:
            RuntimeError: If the write operation fails
            ValueError: If data_list is too long
        """
        if len(data_list) > 256:
            raise ValueError(f"Data list too long: {len(data_list)} bytes (max 256)")

        # Default implementation: write byte by byte
        for i, data in enumerate(data_list):
            self.write_reg(addr_page, i, data & 0xFF)

    @property
    def is_open(self) -> bool:
        """Return True if the device connection is open."""
        return self._is_open

    @staticmethod
    def _bits_to_mask(bits: int) -> int:
        """
        Convert bit count to bit mask.

        1 -> 0x01, 2 -> 0x03, 3 -> 0x07, etc.

        Args:
            bits: Number of bits (1-8)

        Returns:
            int: Bit mask
        """
        if bits <= 0:
            return 0x00
        elif bits >= 8:
            return 0xFF
        else:
            return (1 << bits) - 1

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
