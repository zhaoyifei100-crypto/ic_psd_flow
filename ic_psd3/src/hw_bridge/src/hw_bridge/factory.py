"""
Factory module for creating hardware device instances.

Provides a unified way to instantiate different hardware drivers
based on configuration or driver type specification.
"""

from typing import Optional, Dict, Any
from .interfaces import IDevice


def create_device(driver_type: str, **kwargs) -> IDevice:
    """
    Factory function to create hardware device instances.

    Args:
        driver_type: Type of driver to create ('ftdi', 'pi', 'mock')
        **kwargs: Additional parameters passed to the driver constructor
            - chip_addr: I2C device address (default: 0x58)
            - i2c_port: I2C port/bus number (driver-specific)
            - aves_write: Enable AVES script logging (default: False)
            - aves_path: Path for AVES script output (default: "./to_aves/")

    Returns:
        IDevice: Instance of the requested driver

    Raises:
        ValueError: If the driver_type is not recognized
        ImportError: If required dependencies for the driver are missing
        RuntimeError: If the driver cannot be initialized

    Examples:
        >>> # Create FTDI driver
        >>> device = create_device('ftdi', i2c_port=0, chip_addr=0x58)
        >>>
        >>> # Create Raspberry Pi driver
        >>> device = create_device('pi', i2c_port=1, chip_addr=0x58)
        >>>
        >>> # Create Mock driver for testing
        >>> device = create_device('mock')
    """
    driver_type = driver_type.lower().strip()

    if driver_type == "ftdi":
        from .drivers.ftdi_driver import FtdiDriver

        return FtdiDriver(**kwargs)

    elif driver_type == "pi":
        from .drivers.pi_driver import RaspberryPiDriver

        return RaspberryPiDriver(**kwargs)

    elif driver_type == "mock":
        from .drivers.mock_driver import MockDriver

        return MockDriver(**kwargs)

    else:
        raise ValueError(
            f"Unknown driver type: '{driver_type}'. "
            f"Supported types: 'ftdi', 'pi', 'mock'"
        )


def create_device_from_config(config: Dict[str, Any]) -> IDevice:
    """
    Create a device instance from a configuration dictionary.

    Args:
        config: Configuration dictionary with the following structure:
            {
                'driver_type': 'ftdi' | 'pi' | 'mock',
                'chip_addr': 0x58,  # optional
                'i2c_port': 0,      # optional
                # ... driver-specific options
            }

    Returns:
        IDevice: Configured device instance

    Raises:
        ValueError: If configuration is invalid
        KeyError: If required configuration keys are missing

    Examples:
        >>> config = {
        ...     'driver_type': 'ftdi',
        ...     'chip_addr': 0x58,
        ...     'i2c_port': 0
        ... }
        >>> device = create_device_from_config(config)
    """
    if not isinstance(config, dict):
        raise ValueError("Config must be a dictionary")

    if "driver_type" not in config:
        raise KeyError("Configuration must contain 'driver_type'")

    # Extract driver type and remove it from kwargs
    driver_type = config.pop("driver_type")

    return create_device(driver_type, **config)


def get_available_drivers() -> list:
    """
    Get a list of available driver types.

    Returns:
        list: List of supported driver type strings
    """
    return ["ftdi", "pi", "mock"]


def auto_detect_driver() -> Optional[str]:
    """
    Auto-detect the appropriate driver for the current platform.

    Returns:
        str: Recommended driver type ('ftdi' for Windows, 'pi' for Linux)
        None: If platform cannot be determined

    Examples:
        >>> driver_type = auto_detect_driver()
        >>> device = create_device(driver_type)
    """
    import platform

    system = platform.system()

    if system == "Windows":
        return "ftdi"
    elif system == "Linux":
        return "pi"
    else:
        return None
