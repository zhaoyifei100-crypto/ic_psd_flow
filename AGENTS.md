# AGENTS.md - Coding Guidelines for AI Agents

This document provides guidelines for AI coding agents working in this IC/PSD validation project repository.

## Project Overview

This is a chip validation workflow repository containing:
- **ic_psd2/**: Chip XML Builder - generates chip-level XML register definitions.
- **ic_psd3/**: Hardware bridge library and test automation framework.
  - `hw_bridge/`: I2C hardware abstraction layer (FTDI, Raspberry Pi).
  - `lab_instruments/`: Laboratory instrument management (PSU, Temp Controller).
  - `psd_bridge/`: PSD2-to-PSD3 bridge utilities and script converters.

## Build / Test / Lint Commands

### Python Environment Setup
**Always use a virtual environment (VENV) for all operations:**
```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Install local packages in editable mode
cd ic_psd3/src/hw_bridge && pip install -e .
```

### Quality Control Commands
- **Formatting**: `black ic_psd3/src/` (Configured for 100 characters).
- **Linting**: `flake8 ic_psd3/src/` (Max line length: 100).
- **Testing**: 
    - `pytest` (Run all tests)
    - `pytest path/to/test.py` (Run single test file)
    - `pytest path/to/test.py::test_func` (Run specific test)
    - `pytest -v` (Verbose output)

### Chip XML Builder (ic_psd2)
```bash
# 执行构建
python3 ic_psd2/src/chip_builder.py <config.yaml> [output_dir]
```


## Code Style Guidelines

### Python Standards
- **Target**: Python 3.7+ compatibility.
- **Formatting**: 4 spaces, no tabs. Use trailing commas in multi-line collections.
- **Imports**: Group in 3 sections: Standard library, Third-party, Local (relative imports preferred).
- **Type Hints**: Mandatory for all function parameters and return values.
- **Docstrings**: Use Google-style docstrings with `Args:`, `Returns:`, and `Examples:`.

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DeviceManager`, `MockDriver`).
- **Interfaces**: Prefix with `I` (e.g., `IDevice`).
- **Functions/Methods**: `snake_case` (e.g., `write_bits`, `read_reg`).
- **Variables**: `snake_case` (e.g., `chip_addr`, `reg_value`).
- **Constants**: `UPPER_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_PORT`).
- **Private Attributes**: Leading underscore (e.g., `_is_open`, `_cleanup`).

### Error Handling & Design
- **Exceptions**: Use specific types (`ValueError`, `RuntimeError`). Provide descriptive messages.
- **Cleanup**: Always use `finally` blocks or context managers (`__enter__`/`__exit__`).
- **Patterns**: 
    - **Factory**: Use for driver and instrument instantiation.
    - **Manager**: Centralized management via `InstrumentManager` or `DeviceManager`.
    - **Config-Driven**: Support YAML/JSON for environment settings.

## Hardware Bridge Conventions

1.  **I2C Addressing**: Use 16-bit format `(addr1, addr2)` representing high and low bytes.
2.  **Register Ops**: All drivers must implement `read_reg`, `write_reg`, `read_bits`, `write_bits`.
3.  **Interface**: New drivers must inherit from `IDevice` in `hw_bridge.interfaces`.
4.  **Lab Instruments**: 
    - Add drivers to `lab_instruments/instruments/`.
    - Register new classes in `lab_instruments/__init__.py`.
    - Map types in `InstrumentManager.TYPE_MAP` for configuration support.

## Git Workflow & Testing

- **Commit Messages**: Descriptive English messages.
- **Safety**: **Do NOT commit automatically**. Only commit when explicitly requested.
- **Secrets**: Never commit credentials, `.env` files, or sensitive hardware IP.
- **Test Structure**: Mirror source code in `tests/` directory.
- **Coverage**: Test both success paths and edge-case error handling.

---
*Last updated: 2026-02-13*
