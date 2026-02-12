"""
Device Manager for managing multiple hardware devices.

Provides centralized device management with automatic lifecycle handling.
Supports immediate or lazy initialization, named device access, and
automatic cleanup on program exit.
"""

import atexit
import weakref
from typing import Dict, Optional, Any
from .interfaces import IDevice
from .factory import create_device


class DeviceManager:
    """
    Centralized hardware device manager.

    Manages multiple I2C devices with automatic lifecycle handling.
    Supports immediate or lazy initialization and named device access.

    Features:
        - Register devices by name
        - Immediate or lazy initialization
        - Dictionary-style access (manager['device_name'])
        - Automatic cleanup on program exit
        - Device discovery and listing

    Examples:
        >>> # Immediate open mode (recommended)
        >>> manager = DeviceManager(auto_open=True)
        >>> manager.register('tx_board', 'ftdi', i2c_port=0, chip_addr=0x58)
        >>> manager.register('rx_board', 'ftdi', i2c_port=1, chip_addr=0x58)
        >>>
        >>> # Use anywhere without 'with' block
        >>> manager['tx_board'].write_reg(0x26, 0x00, 0xFF)
        >>> manager['rx_board'].read_reg(0x26, 0x00)
        >>>
        >>> # Cleanup when done
        >>> manager.close_all()

        >>> # Lazy initialization mode
        >>> manager = DeviceManager(auto_open=False)
        >>> manager.register('board_a', 'mock', chip_addr=0x58)
        >>> # Device opens automatically on first access
        >>> manager['board_a'].write_reg(0x26, 0x00, 0xFF)
    """

    # Class-level registry for global access
    _global_instance: Optional["DeviceManager"] = None

    def __init__(self, auto_open: bool = True, register_atexit: bool = True):
        """
        Initialize the device manager.

        Args:
            auto_open: If True, devices open immediately on register().
                      If False, devices open lazily on first access.
            register_atexit: If True, automatically close all devices
                           on program exit.
        """
        self._auto_open = auto_open
        self._devices: Dict[str, IDevice] = {}  # name -> device instance
        self._configs: Dict[str, tuple] = {}  # name -> (driver_type, kwargs)

        # Register cleanup on exit
        if register_atexit:
            atexit.register(self._cleanup)

    def register(self, name: str, driver_type: str, **kwargs) -> IDevice:
        """
        Register a new device.

        If auto_open=True (default), the device is opened immediately.
        If auto_open=False, the device opens on first access.

        Args:
            name: Unique device identifier (e.g., 'tx_board', 'rx_board')
            driver_type: Driver type ('ftdi', 'pi', 'mock')
            **kwargs: Driver-specific parameters
                - chip_addr: I2C device address
                - i2c_port: I2C port/bus number
                - Other driver-specific options

        Returns:
            IDevice: The registered device instance (if auto_open=True)

        Raises:
            ValueError: If name is already registered
            RuntimeError: If device cannot be opened (when auto_open=True)

        Examples:
            >>> manager = DeviceManager()
            >>> manager.register('tx', 'ftdi', i2c_port=0, chip_addr=0x58)
            >>> manager.register('rx', 'ftdi', i2c_port=1, chip_addr=0x58)
        """
        if name in self._configs:
            raise ValueError(f"Device '{name}' is already registered")

        # Store configuration for lazy initialization
        self._configs[name] = (driver_type, kwargs)

        # Immediate open if enabled
        if self._auto_open:
            device = self._open_device(name, driver_type, kwargs)
            self._devices[name] = device
            return device

        return None

    def _open_device(self, name: str, driver_type: str, kwargs: dict) -> IDevice:
        """
        Open a device and return the instance.

        Internal method to create and open a device.
        """
        try:
            device = create_device(driver_type, **kwargs)
            device.open()
            return device
        except Exception as e:
            raise RuntimeError(f"Failed to open device '{name}' ({driver_type}): {e}")

    def __getitem__(self, name: str) -> IDevice:
        """
        Get device by name using dictionary syntax.

        If device is not yet opened (lazy mode), opens it automatically.

        Args:
            name: Device name

        Returns:
            IDevice: Device instance

        Raises:
            KeyError: If device name is not registered
            RuntimeError: If device cannot be opened

        Examples:
            >>> manager['tx_board'].write_reg(0x26, 0x00, 0xFF)
            >>> val = manager['rx_board'].read_reg(0x26, 0x00)
        """
        # Return already opened device
        if name in self._devices:
            return self._devices[name]

        # Lazy initialization
        if name in self._configs:
            driver_type, kwargs = self._configs[name]
            device = self._open_device(name, driver_type, kwargs)
            self._devices[name] = device
            return device

        raise KeyError(
            f"Device '{name}' not found. Registered devices: {list(self._configs.keys())}"
        )

    def get(self, name: str, default: Any = None) -> Optional[IDevice]:
        """
        Get device by name with default value.

        Similar to dict.get(), returns default if device not found.

        Args:
            name: Device name
            default: Default value if device not found

        Returns:
            IDevice or default: Device instance or default value

        Examples:
            >>> device = manager.get('tx_board')
            >>> if device:
            ...     device.write_reg(0x26, 0x00, 0xFF)
        """
        try:
            return self[name]
        except KeyError:
            return default

    def unregister(self, name: str) -> None:
        """
        Unregister and close a device.

        Args:
            name: Device name to unregister

        Examples:
            >>> manager.unregister('tx_board')
        """
        if name in self._devices:
            try:
                self._devices[name].close()
            except Exception:
                pass  # Ignore errors during close
            del self._devices[name]

        if name in self._configs:
            del self._configs[name]

    def close_all(self) -> None:
        """
        Close all registered devices.

        Safely closes all devices and clears the registry.
        Call this on program exit or when done with all devices.

        Examples:
            >>> manager.close_all()
        """
        errors = []

        for name, device in list(self._devices.items()):
            try:
                device.close()
            except Exception as e:
                errors.append(f"{name}: {e}")

        self._devices.clear()
        self._configs.clear()

        if errors:
            raise RuntimeError(f"Errors closing devices: {'; '.join(errors)}")

    def _cleanup(self) -> None:
        """
        Internal cleanup method called on program exit.

        Automatically closes all devices to prevent resource leaks.
        """
        if self._devices:
            try:
                self.close_all()
            except Exception:
                pass  # Ignore errors during cleanup

    def list_devices(self) -> list:
        """
        List all registered device names.

        Returns:
            list: List of registered device names

        Examples:
            >>> manager.register('tx', 'mock')
            >>> manager.register('rx', 'mock')
            >>> manager.list_devices()
            ['tx', 'rx']
        """
        return list(self._configs.keys())

    def is_open(self, name: str) -> bool:
        """
        Check if a device is currently open.

        Args:
            name: Device name

        Returns:
            bool: True if device is open, False otherwise

        Examples:
            >>> manager.register('tx', 'mock')  # auto_open=True
            >>> manager.is_open('tx')
            True
        """
        return name in self._devices and self._devices[name].is_open

    def __contains__(self, name: str) -> bool:
        """
        Check if device is registered.

        Examples:
            >>> if 'tx_board' in manager:
            ...     manager['tx_board'].write_reg(...)
        """
        return name in self._configs

    def __len__(self) -> int:
        """Return number of registered devices."""
        return len(self._configs)

    def __repr__(self) -> str:
        """String representation."""
        devices = ", ".join(f"'{name}'" for name in self._configs.keys())
        return f"DeviceManager([{devices}])"

    # ============== Class Methods for Global Access ==============

    @classmethod
    def get_global(cls) -> "DeviceManager":
        """
        Get or create the global DeviceManager instance.

        Useful for applications that need a single shared manager.

        Returns:
            DeviceManager: Global manager instance

        Examples:
            >>> # In any module, get the global manager
            >>> manager = DeviceManager.get_global()
            >>> manager['tx_board'].write_reg(...)
        """
        if cls._global_instance is None:
            cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def reset_global(cls) -> None:
        """
        Reset the global DeviceManager instance.

        Closes all devices and clears the global instance.
        Useful for testing or when restarting the application.
        """
        if cls._global_instance is not None:
            cls._global_instance.close_all()
            cls._global_instance = None

    @classmethod
    def global_register(cls, name: str, driver_type: str, **kwargs) -> IDevice:
        """
        Register a device with the global manager.

        Convenience method for quick global registration.

        Examples:
            >>> DeviceManager.global_register('tx', 'mock')
            >>> DeviceManager.get_global()['tx'].write_reg(...)
        """
        return cls.get_global().register(name, driver_type, **kwargs)


# ============== Convenience Functions ==============


def get_manager() -> DeviceManager:
    """
    Get the global DeviceManager instance.

    Convenience function for quick access.

    Examples:
        >>> from hw_bridge import get_manager
        >>> get_manager().register('tx', 'mock')
        >>> get_manager()['tx'].write_reg(...)
    """
    return DeviceManager.get_global()
