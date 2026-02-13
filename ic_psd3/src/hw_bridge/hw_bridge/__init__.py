"""
hw_bridge - Hardware bridge library for I2C communication.

This library provides a unified interface for I2C communication
across different hardware platforms (FTDI, Raspberry Pi, etc.).
"""

from .interfaces import IDevice
from .factory import create_device
from .device_manager import DeviceManager, get_manager
from .utils.config import load_config, Config

__version__ = "0.1.0"
__all__ = [
    "IDevice",
    "create_device",
    "DeviceManager",
    "get_manager",
    "load_config",
    "Config",
]
