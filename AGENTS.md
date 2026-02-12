# AGENTS.md - Coding Guidelines for AI Agents

This document provides guidelines for AI coding agents working in this IC/PSD validation project repository.

## Project Overview

This is a chip validation workflow repository containing:
- **ic_psd2/**: Chip XML Builder - generates chip-level XML register definitions
- **ic_psd3/**: Hardware bridge library and test automation framework
  - `hw_bridge/`: I2C hardware abstraction layer
  - `lab_instruments/`: Laboratory instrument management
  - `psd_bridge/`: PSD2-to-PSD3 bridge utilities

## Build / Test / Lint Commands

### Python Environment Setup

**Always use virtual environment (VENV) for all operations:**

```bash
# Create virtual environment (one-time setup)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate          # macOS/Linux
# OR
.venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
cd ic_psd3/src/hw_bridge && pip install -e .
cd ../../..                       # Return to project root

# Deactivate when done
deactivate
```

**Important**: All Python commands must run **within the activated VENV**.

### Code Quality Tools (configured in pyproject.toml)
```bash
black ic_psd3/src/           # Format code (line length: 100)
flake8 ic_psd3/src/          # Lint (max line length: 100)
pytest                       # Run all tests
pytest path/to/test.py       # Run single test file
pytest path/to/test.py::test_func  # Run single test function
pytest -v                    # Verbose output
```

### Chip XML Builder Commands (ic_psd2)
```bash
cd ic_psd2/scripts
python skill_helper.py state
python skill_helper.py init <chip_name> <modules_dir> [output_dir]
python skill_helper.py check
python skill_helper.py build
python chip_cli.py status
```

## Code Style Guidelines

### Python Version
- Target Python 3.7+ compatibility

### Formatting
- **Line length**: 100 characters (configured in pyproject.toml)
- Use **Black** for formatting, **Flake8** for linting
- **Indentation**: 4 spaces (no tabs)
- Use trailing commas in multi-line collections

### Imports
Order imports in 3 groups with blank lines:
1. Standard library
2. Third-party
3. Local/application imports (use relative imports within same package)

```python
import atexit
from typing import Dict, List, Optional

import yaml

from .interfaces import IDevice
from ..drivers.mock_driver import MockDriver
```

### Type Hints
- Use for all function parameters and return values
- Import from `typing`: `Dict`, `List`, `Optional`, `Any`, `Union`
- Use string literals for forward references: `-> "DeviceManager"`

### Naming Conventions
- **Classes**: PascalCase (`DeviceManager`, `MockDriver`)
- **Functions/Methods**: snake_case (`write_reg`, `read_bits`)
- **Variables**: snake_case (`chip_addr`, `write_log`)
- **Constants**: UPPER_CASE (`TYPE_MAP`, `MAX_RETRIES`)
- **Private attributes**: leading underscore (`_is_open`, `_cleanup`)
- **Abstract base classes**: Prefix with `I` (`IDevice`)

### Docstrings
Use Google-style docstrings with:
- One-line summary
- `Args:`, `Returns:`, `Raises:`, `Examples:` sections

```python
def write_bits(self, addr1: int, addr2: int, lsb: int, bits: int, value: int) -> None:
    """Write specific bits to a register.

    Args:
        addr1: Page address / high byte (8-bit)
        addr2: Offset address / low byte (8-bit)
        lsb: Least significant bit position (0-7)
        bits: Number of bits to write (1-8)
        value: Value to write

    Raises:
        RuntimeError: If write operation fails
        ValueError: If bit parameters are invalid

    Examples:
        >>> device.write_bits(0x26, 0x01, lsb=2, bits=4, value=0x0A)
    """
```

### Error Handling
- Use specific exceptions: `ValueError`, `RuntimeError`, `KeyError`
- Provide descriptive error messages
- Use try/except with minimal scope
- Clean up resources in `finally` blocks or use context managers

```python
try:
    device = create_device(driver_type, **kwargs)
    device.open()
except Exception as e:
    raise RuntimeError(f"Failed to open device: {e}")
```

### Class Design
- Use abstract base classes (ABC) for interfaces
- Implement context managers (`__enter__`, `__exit__`)
- Use properties for read-only attributes (`@property`)
- Use class methods for factory patterns (`@classmethod`)

```python
class IDevice(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
```

### Architecture Patterns
- **Factory Pattern**: Creating driver instances
- **Manager Pattern**: Centralized resource management
- **Interface Pattern**: Abstract base classes defining contracts
- **Configuration-Driven**: Support YAML/JSON configuration files

### File Organization
- One class per file (generally)
- Group related classes in packages
- Use `__init__.py` to expose public API
- Place tests in `tests/` directory mirroring source structure

### Comments
- Use comments sparingly - prefer self-documenting code
- Comment the "why", not the "what"

### Git Workflow
- Write descriptive commit messages
- **Do NOT commit automatically** - Only commit when user explicitly requests it
- Never commit secrets, credentials, or sensitive data
- Keep `.gitignore` updated
- Warn users before committing generated files or sensitive data

## Testing

- Use pytest for all tests
- Test file naming: `test_*.py` or `*_test.py`
- Test function naming: `test_<function>_<scenario>()`
- Use mock drivers for hardware-independent tests
- Test both success and error paths

## Language Support

- **Code**: Use English (variables, functions, comments)
- **Documentation**: Can use Chinese for user-facing docs
- **Commit messages**: Prefer English

## Key Project-Specific Conventions

1. **Hardware Bridge**: All drivers must implement `IDevice` interface
2. **I2C Addressing**: Use 16-bit format `(addr1, addr2)` - high byte + low byte
3. **Register Operations**: Provide `read_reg`, `write_reg`, `read_bits`, `write_bits`
4. **Instrument Manager**: Use configuration-driven instantiation via YAML
5. **XML Builder**: State-driven workflow (empty → init → ready → done)

---

*Last updated: 2026-02-12*
