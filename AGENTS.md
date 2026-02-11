# AGENTS.md - IC PSD Flow Repository

This repository contains tools for IC (Integrated Circuit) Product Stage Definition (PSD) workflow - similar to IPD Stage-Gate management for semiconductor development.

- **PSD2 (ic_psd2)**: Development Phase - Chip XML Builder for register map generation
- **PSD3 (ic_psd3)**: Qualification Phase - Hardware drivers and test automation

## Build Commands

```bash
# Install dependencies
pip install -r requirements.txt

# For ic_psd2 - Chip XML Builder
python ic_psd2/scripts/chip_cli.py init --chip-name <NAME> --modules-dir <DIR>
python ic_psd2/scripts/chip_cli.py check
python ic_psd2/scripts/chip_cli.py build
python ic_psd2/scripts/chip_cli.py export --format json

# Direct builder usage
python ic_psd2/src/chip_builder.py <config.yaml> [output_dir]
```

## Test Commands

**No formal test framework configured.** Run manual tests:

```bash
# Test XML parser
python ic_psd3/src/xml_parser.py

# Test FTDI driver (requires hardware)
python ic_psd3/src/drv_ftdi.py

# Test PI driver (requires Raspberry Pi)
python ic_psd3/src/drv_pi.py
```

## Lint Commands

**No linting configured.** Recommended setup:

```bash
# Install linting tools
pip install flake8 black isort mypy

# Run linting (manual)
flake8 ic_psd2/ ic_psd3/
black --check ic_psd2/ ic_psd3/
isort --check ic_psd2/ ic_psd3/
```

## Code Style Guidelines

### Python Style

- **Python Version**: Python 3.7+
- **Indentation**: 4 spaces (no tabs)
- **Line Length**: 100 characters max
- **Quotes**: Double quotes for docstrings, single for strings

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `ChipXMLBuilder`, `DrvFTDI` |
| Functions | snake_case | `load_config()`, `write_reg()` |
| Variables | snake_case | `base_addr`, `chip_info` |
| Constants | UPPER_CASE | `FT_OK`, `I2C_TRANSFER_OPTIONS_START_BIT` |
| Private | _leading_underscore | `_parse_mask()`, `_built_tree` |

### Import Order

```python
# 1. Standard library
import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass

# 2. Third-party
from openpyxl import Workbook
import yaml  # optional

# 3. Local modules
from scripts.skill_helper import get_state
```

### Type Hints

Use type hints for function signatures:

```python
def load_config(self, config_path: str) -> None:
    ...

def add_instance(
    self,
    name: str,
    module_name: str,
    base_addr: int,
    instance_id: int = 0,
) -> "ChipXMLBuilder":
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def build(self) -> ET.Element:
    """
    Execute build process.

    Returns:
        Root XML Element.

    Raises:
        ValueError: If configuration is invalid.
        RuntimeError: If build fails.
    """
```

### Error Handling

```python
# Raise specific exceptions
if not os.path.exists(xml_path):
    raise FileNotFoundError(f"Module XML not found: {xml_path}")

# RuntimeError for execution failures
if status != FT_OK:
    raise RuntimeError(f"I2C write failed: {status}")

# Try-except with context
try:
    builder.load_config(config_path)
except ImportError as e:
    raise ImportError("Install PyYAML: pip install pyyaml") from e
```

### File Structure

```python
#!/usr/bin/env python3
"""
Module short description.

Longer description here.

Author: name
Date: YYYY-MM-DD
"""

# Imports
# ...

# Constants
# ...

# Classes/Functions
# ...

if __name__ == "__main__":
    # CLI or test code
    pass
```

### Chinese Comments

Comments can be in Chinese for this codebase (business requirement), but:
- Keep technical terms in English (e.g., "XML parser", "I2C driver")
- Use docstrings for public API documentation
- Variable/function names must be English

## Project Structure

```
ic_psd2/                    # Development Phase - XML Builder
├── src/
│   └── chip_builder.py     # Main ChipXMLBuilder class
├── scripts/
│   ├── chip_cli.py         # CLI interface
│   └── skill_helper.py     # Skill automation helper
├── .chip-builder/
│   └── config.yaml         # Builder configuration
└── models/                 # Module XML files

ic_psd3/                    # Qualification Phase - Test & Drivers
├── src/
│   ├── drv_ftdi.py         # FTDI I2C driver (Windows)
│   ├── drv_pi.py           # Raspberry Pi I2C driver (Linux)
│   ├── xml_parser.py       # XML parser utilities
│   └── auto_py_script.py   # Test script generator
└── README.md               # Detailed workflow documentation
```

## Key Dependencies

- `openpyxl>=3.0.0` - Excel file handling
- `pyyaml` - YAML config parsing (optional)
- `ctypes` - FTDI DLL interface (Windows)

## Hardware Notes

- **FTDI Driver**: Windows only, requires `libMPSSE.dll`
- **PI Driver**: Linux only, requires `i2ctransfer` tool
- Default I2C address: `0xB0` (GS Coolink chips)

## Common Tasks

```bash
# Generate chip XML from modules
python ic_psd2/src/chip_builder.py config.yaml ./output

# Parse XML to generate Python register definitions
python -c "from ic_psd3.src.xml_parser import XMLParser; p = XMLParser('file.xml'); p.get_regdefing_py()"
```
