# AGENTS.md - Coding Guidelines for AI Agents

This document provides guidelines for AI coding agents working in this IC/PSD validation project repository.

## Project Overview

This is a chip validation workflow repository containing:
- **ic_psd2/**: Chip XML Builder - generates chip-level XML register definitions.
- **ic_psd3/**: Hardware bridge library and test automation framework.
  - `hw_bridge/`: I2C hardware abstraction layer (FTDI, Raspberry Pi, Mock).
  - `lab_instruments/`: Laboratory instrument management (PSU, Temperature Controller).
  - `psd_bridge/`: PSD2-to-PSD3 bridge utilities and script converters.
  - `library/`: Auto-generated register classes (auto_class.py, aves_class.py, reg_define.py).

## Build / Test / Lint Commands

### Python Environment Setup
**Always use a virtual environment (VENV) for all operations:**
```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install local packages in editable mode (Linux)
cd ic_psd3/src/hw_bridge && pip install -e .

# Windows: pip install hw_bridge manually if not already installed
```

### Quality Control Commands
- **Formatting**: `black ic_psd3/src/` (Configured for 100 characters in pyproject.toml).
- **Linting**: `flake8 ic_psd3/src/` (Max line length: 100).
- **Type Checking**: Use type hints (Python 3.7+ compatible).

### Testing Commands
```bash
# Run all tests
pytest

# Run single test file
pytest path/to/test.py

# Run specific test function
pytest path/to/test.py::test_func

# Run with verbose output
pytest -v

# Run test runner for PSD3 tests
python runner.py ic_psd3/tests/specs/<testspec.md>

# Dry-run to generate library index only
python runner.py ic_psd3/tests/specs/<testspec.md> --dry-run
```

### Chip XML Builder (ic_psd2)
```bash
# Execute build
python3 ic_psd2/src/chip_builder.py <config.yaml> [output_dir]

# Generate auto_class.py and reg_define.py
python -m ic_psd3.src.psd_bridge.unified_generator <XML_FILE>

# Generate aves_class.py
python -m ic_psd3.src.psd_bridge.aves_converter <AVES_FILE>
```

## Code Style Guidelines

### Python Standards
- **Target**: Python 3.7+ compatibility.
- **Formatting**: 4 spaces, no tabs. Use trailing commas in multi-line collections.
- **Line Length**: 100 characters (configured in pyproject.toml).
- **Imports**: Group in 3 sections: Standard library, Third-party, Local (relative imports preferred).
- **Type Hints**: Mandatory for all function parameters and return values.
- **Docstrings**: Use Google-style docstrings with `Args:`, `Returns:`, and `Examples:`.

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DeviceManager`, `MockDriver`, `FTDIDriver`).
- **Interfaces**: Prefix with `I` (e.g., `IDevice`).
- **Functions/Methods**: `snake_case` (e.g., `write_bits`, `read_reg`, `open_device`).
- **Variables**: `snake_case` (e.g., `chip_addr`, `reg_value`, `i2c_port`).
- **Constants**: `UPPER_CASE` (e.g., `FT_OK`, `I2C_TRANSFER_OPTIONS_START_BIT`).
- **Private Attributes**: Leading underscore (e.g., `_is_open`, `_cleanup`, `_handle`).
- **Module Files**: `snake_case.py` (e.g., `ftdi_driver.py`, `device_manager.py`).

### Error Handling & Design
- **Exceptions**: Use specific types (`ValueError`, `RuntimeError`, `ConnectionError`). Provide descriptive messages.
- **Cleanup**: Always use `finally` blocks or context managers (`__enter__`/`__exit__`).
- **Driver State**: Track connection state with `_is_open` boolean property.
- **Validation**: Validate parameters at method entry (e.g., check `len(data_list) > 256`).
- **Patterns**: 
    - **Factory**: Use for driver and instrument instantiation.
    - **Manager**: Centralized management via `InstrumentManager` or `DeviceManager`.
    - **Config-Driven**: Support YAML/JSON for environment settings.
    - **Context Managers**: Implement `__enter__`/`__exit__` for resource management.

### Hardware Bridge Conventions
1.  **I2C Addressing**: Use 16-bit format `(addr1, addr2)` representing high and low bytes.
2.  **Register Ops**: All drivers must implement `read_reg`, `write_reg`, `read_bits`, `write_bits`.
3.  **Interface**: New drivers must inherit from `IDevice` in `hw_bridge.interfaces`.
4.  **Lab Instruments**: 
    - Add drivers to `lab_instruments/instruments/`.
    - Register new classes in `lab_instruments/__init__.py`.
    - Map types in `InstrumentManager.TYPE_MAP` for configuration support.

## Skills Reference

The following skills are available in `.opencode/skills/`:

1. **rebuild-library**: Regenerate `ic_psd3/library/` from XML and AVES scripts.
2. **simple-test-runner**: PSD3 test execution with library indexing.
3. **aves-script-builder**: Generate AVES register configuration scripts from MD specs.
4. **chip-xml-builder**: Generate chip-level XML register definitions.

## Git Workflow & Testing

- **Commit Messages**: Descriptive English messages.
- **Safety**: **Do NOT commit automatically**. Only commit when explicitly requested.
- **Secrets**: Never commit credentials, `.env` files, or sensitive hardware IP.
- **Test Structure**: Mirror source code in `tests/` directory.
- **Coverage**: Test both success paths and edge-case error handling.
- **Code Review**: Ensure type hints, docstrings, and error handling are complete.

---
*Last updated: 2026-02-14*
