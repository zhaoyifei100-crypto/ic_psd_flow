"""
Configuration management for hw_bridge.

Supports loading configuration from YAML or JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """
    Configuration container for hardware bridge settings.

    Attributes:
        driver_type: Type of driver ('ftdi', 'pi', 'mock')
        chip_addr: I2C device address
        i2c_port: I2C port/bus number
        driver_options: Driver-specific options
    """

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.

        Args:
            config_dict: Configuration dictionary
        """
        self._config = config_dict or {}

    @property
    def driver_type(self) -> Optional[str]:
        """Get driver type."""
        # Try hardware.driver_type first, then driver_type
        hardware = self._config.get("hardware", {})
        return hardware.get("driver_type") or self._config.get("driver_type")

    @property
    def chip_addr(self) -> int:
        """Get I2C chip address."""
        hardware = self._config.get("hardware", {})
        addr = hardware.get("chip_addr") or self._config.get("chip_addr", 0x58)
        # Convert hex string to int if necessary
        if isinstance(addr, str):
            addr = int(addr, 0)  # auto-detect base
        return addr

    @property
    def i2c_port(self) -> int:
        """Get I2C port number."""
        hardware = self._config.get("hardware", {})
        port = hardware.get("i2c_port") or self._config.get("i2c_port", 0)
        return int(port)

    @property
    def aves_write(self) -> bool:
        """Get AVES script write flag."""
        hardware = self._config.get("hardware", {})
        return hardware.get("aves_write") or self._config.get("aves_write", False)

    @property
    def aves_path(self) -> str:
        """Get AVES script output path."""
        hardware = self._config.get("hardware", {})
        return hardware.get("aves_path") or self._config.get("aves_path", "./to_aves/")

    def get_driver_options(self) -> Dict[str, Any]:
        """
        Get driver-specific options.

        Returns:
            Dictionary of options for the create_device function
        """
        hardware = self._config.get("hardware", {})
        driver_type = self.driver_type

        # Get driver-specific section if exists
        driver_opts = hardware.get(driver_type, {}) if driver_type else {}

        # Build options dict
        options = {
            "chip_addr": self.chip_addr,
            "i2c_port": self.i2c_port,
            "aves_write": self.aves_write,
            "aves_path": self.aves_path,
        }

        # Add driver-specific options
        options.update(driver_opts)

        return options

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()


def load_config(config_path: str) -> Config:
    """
    Load configuration from a file.

    Supports YAML (.yaml, .yml) and JSON (.json) formats.

    Args:
        config_path: Path to configuration file

    Returns:
        Config: Configuration object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported or invalid

    Examples:
        >>> config = load_config('config.yaml')
        >>> print(config.driver_type)
        'ftdi'
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Determine format from extension
    suffix = config_path.suffix.lower()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            if suffix in [".yaml", ".yml"]:
                try:
                    import yaml

                    config_dict = yaml.safe_load(f)
                except ImportError:
                    raise ImportError(
                        "PyYAML is required to load YAML config files. "
                        "Install with: pip install pyyaml"
                    )
            elif suffix == ".json":
                config_dict = json.load(f)
            else:
                # Try JSON first, then YAML
                try:
                    config_dict = json.load(f)
                except json.JSONDecodeError:
                    try:
                        import yaml

                        config_dict = yaml.safe_load(f)
                    except ImportError:
                        raise ValueError(
                            f"Cannot parse config file '{config_path}'. "
                            f"Supported formats: JSON, YAML"
                        )
    except Exception as e:
        raise ValueError(f"Failed to load config from '{config_path}': {e}")

    return Config(config_dict)


def create_default_config() -> Config:
    """
    Create a default configuration.

    Returns:
        Config: Default configuration object
    """
    default_config = {
        "hardware": {
            "driver_type": "mock",
            "chip_addr": "0x58",
            "i2c_port": 0,
            "aves_write": False,
            "aves_path": "./to_aves/",
            "ftdi": {"dll_path": "./libMPSSE.dll"},
            "pi": {"use_smbus": False},
        }
    }
    return Config(default_config)


def save_config(config: Config, output_path: str, format: str = "yaml") -> None:
    """
    Save configuration to a file.

    Args:
        config: Configuration object to save
        output_path: Path to output file
        format: Output format ('yaml' or 'json')

    Raises:
        ValueError: If format is not supported
    """
    output_path = Path(output_path)
    config_dict = config.to_dict()

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        if format.lower() in ["yaml", "yml"]:
            try:
                import yaml

                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            except ImportError:
                raise ImportError(
                    "PyYAML is required to save YAML config files. "
                    "Install with: pip install pyyaml"
                )
        elif format.lower() == "json":
            json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'")
