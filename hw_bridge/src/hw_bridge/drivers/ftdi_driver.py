"""
FTDI I2C driver for Windows.

Uses libMPSSE.dll for USB-to-I2C communication.
Compatible with FTDI FT2232H, FT4232H, and similar chips.
"""

import ctypes
import datetime
import os
import time
from pathlib import Path
from typing import List, Optional
from ..interfaces import IDevice


# FTDI Constants
FT_OK = 0
FT_OPEN_BY_SERIAL_NUMBER = 1

# I2C Transfer Options
I2C_TRANSFER_OPTIONS_START_BIT = 0x01
I2C_TRANSFER_OPTIONS_STOP_BIT = 0x02
I2C_TRANSFER_OPTIONS_BREAK_ON_NACK = 0x04
I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES = 0x08
I2C_TRANSFER_OPTIONS_FAST_TRANSFER = 0x30

# I2C Config Options
I2C_DISABLE_3PHASE_CLOCKING = 0x00000001
I2C_ENABLE_DRIVE_ONLY_ZERO = 0x00000002
I2C_ENABLE_PULLUPS = 0x00000004
I2C_DISABLE_SCHMITT_TRIGGER = 0x00000008
I2C_ENABLE_FAST_TRANSFER = 0x00000010
I2C_ENABLE_HIGH_SPEED = 0x00000020
I2C_ENABLE_STRETCH_CLOCK = 0x00000040
I2C_DISABLE_ACK_POLLING = 0x00000080
I2C_ENABLE_STRICT_ADDRESS_CHECK = 0x00000100
I2C_ENABLE_DEBUG_MODE = 0x00000200


class ChannelConfig(ctypes.Structure):
    """I2C Channel Configuration structure."""

    _fields_ = [
        ("ClockRate", ctypes.c_uint32),
        ("LatencyTimer", ctypes.c_uint8),
        ("Options", ctypes.c_uint32),
    ]


class FT_DEVICE_LIST_INFO_NODE(ctypes.Structure):
    """FTDI Device List Info Node structure."""

    _fields_ = [
        ("Flags", ctypes.c_ulong),
        ("Type", ctypes.c_ulong),
        ("ID", ctypes.c_ulong),
        ("LocId", ctypes.c_ulong),
        ("SerialNumber", ctypes.c_char * 16),
        ("Description", ctypes.c_char * 64),
        ("ftHandle", ctypes.c_void_p),
    ]


class FtdiDriver(IDevice):
    """
    FTDI USB-to-I2C driver using libMPSSE.

    This driver communicates with I2C devices through FTDI USB chips
    using the libMPSSE library. It supports FT2232H, FT4232H, and
    similar FTDI chips with MPSSE support.

    Requirements:
        - Windows operating system
        - FTDI D2XX drivers (ftd2xx.dll)
        - libMPSSE.dll (included with this library)
        - FTDI USB device connected

    Attributes:
        i2c_port: FTDI port number (0 or 1 for dual-port devices)
        chip_addr: I2C device address
        handle: FTDI device handle
    """

    def __init__(
        self,
        i2c_port: int = 0,
        chip_addr: int = 0x58,
        dll_path: Optional[str] = None,
        aves_write: bool = False,
        aves_path: str = "./to_aves/",
        clock_rate: int = 400000,
        **kwargs,
    ):
        """
        Initialize the FTDI driver.

        Args:
            i2c_port: FTDI port number (0 or 1, default: 0)
            chip_addr: I2C device address in 7-bit format (default: 0x58)
            dll_path: Path to libMPSSE.dll (default: auto-detect)
            aves_write: Enable AVES script logging
            aves_path: Path for AVES script output
            clock_rate: I2C clock rate in Hz (default: 400000 = 400kHz)
            **kwargs: Additional parameters (ignored)
        """
        super().__init__(chip_addr=chip_addr)
        self.i2c_port = i2c_port
        self._clock_rate = clock_rate
        self.aves_write = aves_write

        # DLL handles
        self._ftd2xx = None
        self._libmpsse = None
        self._handle = ctypes.c_void_p()

        # Device info
        self._num_devices = ctypes.c_ulong()
        self._bytes_written = ctypes.c_ulong()

        # Setup AVES logging
        if self.aves_write:
            os.makedirs(aves_path, exist_ok=True)
            now = datetime.datetime.now()
            StyleTime = now.strftime("%Y_%m_%d_%H_%M_%S")
            self.write_to = os.path.join(aves_path, f"aves_{StyleTime}.txt")
        else:
            self.write_to = None

        # Store DLL path
        self._dll_path = dll_path

    def _load_dlls(self) -> None:
        """
        Load FTDI DLL libraries.

        Raises:
            RuntimeError: If DLLs cannot be loaded
        """
        try:
            # Load ftd2xx.dll (system installed)
            self._ftd2xx = ctypes.windll.ftd2xx
        except Exception as e:
            raise RuntimeError(
                f"Failed to load ftd2xx.dll. Please install FTDI D2XX drivers. Error: {e}"
            )

        # Load libMPSSE.dll
        if self._dll_path:
            dll_path = Path(self._dll_path)
        else:
            # Try to find in package directory
            dll_path = Path(__file__).parent / "libMPSSE.dll"

        if not dll_path.exists():
            # Try current working directory
            dll_path = Path("libMPSSE.dll")

        if not dll_path.exists():
            raise RuntimeError(
                f"libMPSSE.dll not found. Expected at: {dll_path}\n"
                f"Please ensure the DLL is in the package directory or specify dll_path."
            )

        try:
            self._libmpsse = ctypes.CDLL(str(dll_path))
        except Exception as e:
            raise RuntimeError(f"Failed to load libMPSSE.dll from {dll_path}: {e}")

    def open(self) -> None:
        """
        Open the FTDI device and initialize I2C.

        This method:
        1. Loads required DLLs
        2. Opens the FTDI device
        3. Configures I2C channel
        4. Verifies I2C connection

        Raises:
            RuntimeError: If device cannot be opened or configured
        """
        # Load DLLs
        self._load_dlls()

        # Open device
        self._open_device()

        # Configure I2C
        self._configure_i2c()

        # Check connection
        self._check_connection()

        self._is_open = True

    def _open_device(self) -> None:
        """
        Open the FTDI USB device.

        Raises:
            RuntimeError: If device cannot be opened
        """
        # Get device list
        status = FT_OK
        status |= self._ftd2xx.FT_CreateDeviceInfoList(ctypes.byref(self._num_devices))

        if self._num_devices.value == 0:
            raise RuntimeError("No FTDI devices found. Please check USB connection.")

        # Allocate device list
        device_list_type = FT_DEVICE_LIST_INFO_NODE * self._num_devices.value
        devices = device_list_type()

        status |= self._ftd2xx.FT_GetDeviceInfoList(
            devices, ctypes.byref(self._num_devices)
        )

        if status != FT_OK:
            raise RuntimeError(f"Failed to get device list. Status: {status}")

        # Check port number
        if self.i2c_port >= self._num_devices.value:
            raise RuntimeError(
                f"Port {self.i2c_port} not available. "
                f"Found {self._num_devices.value} device(s)."
            )

        # Open device by serial number
        status |= self._ftd2xx.FT_OpenEx(
            devices[self.i2c_port].SerialNumber,
            FT_OPEN_BY_SERIAL_NUMBER,
            ctypes.byref(self._handle),
        )

        # Reset device
        status |= self._ftd2xx.FT_ResetDevice(self._handle)

        if status != FT_OK:
            raise RuntimeError(f"Failed to open FTDI device. Status: {status}")

    def _configure_i2c(self) -> None:
        """
        Configure the I2C channel.

        Raises:
            RuntimeError: If configuration fails
        """
        config = ChannelConfig()
        config.ClockRate = self._clock_rate
        config.LatencyTimer = 1  # 1 ms
        config.Options = I2C_ENABLE_FAST_TRANSFER | I2C_ENABLE_HIGH_SPEED

        status = self._libmpsse.I2C_InitChannel(self._handle, ctypes.byref(config))
        if status != FT_OK:
            raise RuntimeError(f"Failed to configure I2C. Status: {status}")

        time.sleep(0.5)  # Allow configuration to settle

    def _check_connection(self) -> None:
        """
        Verify I2C connection by attempting a write operation.

        Raises:
            RuntimeError: If connection check fails
        """
        check_options = (
            I2C_TRANSFER_OPTIONS_START_BIT
            | I2C_TRANSFER_OPTIONS_STOP_BIT
            | I2C_TRANSFER_OPTIONS_BREAK_ON_NACK
        )

        command = [0x00, 0x00]  # Dummy write

        for attempt in range(20):
            status = self._libmpsse.I2C_DeviceWrite(
                self._handle,
                ctypes.c_uint32(self.chip_addr),
                ctypes.c_uint32(2),
                (ctypes.c_uint8 * 2)(*command),
                ctypes.byref(self._bytes_written),
                ctypes.c_uint32(check_options),
            )

            if status == FT_OK:
                return

        raise RuntimeError(
            "I2C connection check failed. Please verify:\n"
            "1. Device is connected and powered\n"
            "2. I2C address is correct (current: 0x{:02X})\n"
            "3. Wiring is correct".format(self.chip_addr)
        )

    def close(self) -> None:
        """
        Close the FTDI device and release resources.
        """
        if self._ftd2xx and self._handle:
            try:
                self._ftd2xx.FT_Close(self._handle)
            except Exception:
                pass  # Ignore errors during close

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

        options = (
            I2C_TRANSFER_OPTIONS_START_BIT
            | I2C_TRANSFER_OPTIONS_STOP_BIT
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER
        )

        command = [addr1, addr2, value]

        status = self._libmpsse.I2C_DeviceWrite(
            self._handle,
            ctypes.c_uint32(self.chip_addr),
            ctypes.c_uint32(3),
            (ctypes.c_uint8 * 3)(*command),
            ctypes.byref(self._bytes_written),
            ctypes.c_uint32(options),
        )

        if status != FT_OK:
            raise RuntimeError(f"I2C write failed. Status: {status}")

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

        # Write address (no stop)
        w_options = (
            I2C_TRANSFER_OPTIONS_START_BIT
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER
        )

        command = [addr1, addr2]

        status = self._libmpsse.I2C_DeviceWrite(
            self._handle,
            ctypes.c_uint32(self.chip_addr),
            ctypes.c_uint32(2),
            (ctypes.c_uint8 * 2)(*command),
            ctypes.byref(self._bytes_written),
            ctypes.c_uint32(w_options),
        )

        if status != FT_OK:
            raise RuntimeError(f"I2C write address failed. Status: {status}")

        # Read data (with stop)
        r_options = (
            I2C_TRANSFER_OPTIONS_START_BIT
            | I2C_TRANSFER_OPTIONS_STOP_BIT
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER
        )

        rb_buffer = (ctypes.c_uint8 * 1)()

        status = self._libmpsse.I2C_DeviceRead(
            self._handle,
            ctypes.c_uint32(self.chip_addr),
            ctypes.c_uint32(1),
            rb_buffer,
            ctypes.byref(self._bytes_written),
            ctypes.c_uint32(r_options),
        )

        if status != FT_OK:
            raise RuntimeError(f"I2C read failed. Status: {status}")

        return int(rb_buffer[0])

    def write_page(self, addr_page: int, data_list: List[int]) -> None:
        """
        Write a full page (256 bytes) efficiently.

        Args:
            addr_page: Page address (high byte)
            data_list: List of bytes to write

        Raises:
            RuntimeError: If write fails
            ValueError: If data_list is too long
        """
        if not self._is_open:
            raise RuntimeError("Device not open. Call open() first.")

        if len(data_list) > 256:
            raise ValueError(f"Data list too long: {len(data_list)} bytes (max 256)")

        options = (
            I2C_TRANSFER_OPTIONS_START_BIT
            | I2C_TRANSFER_OPTIONS_STOP_BIT
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES
            | I2C_TRANSFER_OPTIONS_FAST_TRANSFER
        )

        # Build command: [page_addr, 0x00, data...]
        command = [addr_page, 0x00]
        command.extend([d & 0xFF for d in data_list])

        c_command = (ctypes.c_uint8 * len(command))(*command)

        status = self._libmpsse.I2C_DeviceWrite(
            self._handle,
            ctypes.c_uint32(self.chip_addr),
            ctypes.c_uint32(len(command)),
            c_command,
            ctypes.byref(self._bytes_written),
            ctypes.c_uint32(options),
        )

        if status != FT_OK:
            raise RuntimeError(f"I2C page write failed. Status: {status}")

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
        device_addr = "b0"  # GS Coolink default
        addr1_str = f"{addr1:02x}"
        addr2_str = f"{addr2:02x}"
        value_str = f"{value:02x}"

        print_str = f"{device_addr} {addr1_str}{addr2_str} {value_str};\n"

        with open(self.write_to, "a") as f:
            f.write(print_str)
