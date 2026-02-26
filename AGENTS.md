# AGENTS.md - Coding Guidelines for AI Agents

This document provides comprehensive guidelines for AI coding agents (like yourself) working in this IC/PSD validation project repository. Adhere strictly to these conventions.

## Project Overview

This is a chip validation workflow repository containing hardware abstraction layers and automation tools:
- **ic_psd2/**: Chip XML Builder. Merges sub-module register definitions into a full chip XML.
  - `src/chip_builder.py`: Main logic using Excel or YAML configuration.
  - `src/aves_generator.py`: Generates AVES scripts from XML.
- **ic_psd3/**: Hardware bridge library and test automation framework.
  - `src/hw_bridge/`: I2C hardware abstraction layer (FTDI, Raspberry Pi, Mock).
  - `src/lab_instruments/`: Laboratory instrument management (PSU, Temperature Controller).
  - `src/psd_bridge/`: Bridge utilities and script converters (unified_generator, aves_converter).
  - `library/`: Auto-generated register classes (`auto_class.py`, `aves_class.py`, `reg_define.py`).
  - `tests/`: Test specifications (specs/) and generated test code (generated/).

## Build / Test / Quality Control

### Python Environment Setup
**Always use a virtual environment for all operations:**
```bash
# Initial Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install core library in editable mode
cd ic_psd3/src/hw_bridge && pip install -e .
```

### Testing Commands (pytest)
```bash
# Run all tests
pytest

# Run a single test file (most common for development)
pytest ic_psd3/tests/generated/test_register_ops.py

# Run a specific test function
pytest path/to/test.py::test_specific_feature

# Run with output capture disabled (see prints/logs)
pytest -s

# Run with verbose output and coverage
pytest -v --cov=ic_psd3/src/
```

### Quality Control & Linting
- **Formatting**: `black ic_psd3/src/` (Line length: 100).
- **Linting**: `flake8 ic_psd3/src/` (Max line length: 100).
- **Type Checking**: Use type hints (Python 3.7+ compatible). Use `mypy` if available.
- **Ruff (Alternative)**: `ruff check .` and `ruff format .` are preferred for speed.

## Code Style Guidelines

### Python Standards & Formatting
- **Version**: Target Python 3.7+ compatibility.
- **Indentation**: 4 spaces, no tabs.
- **Line Length**: 100 characters (strictly enforced by black).
- **Imports**: Group into three sections separated by blank lines:
    1. Standard Library
    2. Third-party packages
    3. Local/Relative imports
- **Docstrings**: Mandatory Google-style docstrings for all public classes and methods.
  ```python
  def read_reg(self, addr1: int, addr2: int) -> int:
      """Reads a value from a register.
      
      Args:
          addr1: Page/High byte address.
          addr2: Offset/Low byte address.
          
      Returns:
          int: 8-bit register value.
          
      Raises:
          RuntimeError: If hardware communication fails.
      """
  ```

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DeviceManager`, `FTDIDriver`).
- **Interfaces**: Prefix with `I` (e.g., `IDevice`).
- **Functions/Methods**: `snake_case` (e.g., `write_bits`, `read_reg`).
- **Variables**: `snake_case` (e.g., `chip_addr`, `reg_value`).
- **Constants**: `UPPER_CASE` (e.g., `DEFAULT_I2C_ADDR`, `MAX_RETRIES`).
- **Private Attributes**: Single leading underscore (e.g., `_is_open`, `_handle`).
- **Module Files**: `snake_case.py`.

### Hardware Bridge & Error Handling
1.  **I2C Addressing**: Use 16-bit format `(addr1, addr2)` representing high and low bytes.
2.  **IDevice Implementation**: All new drivers must inherit from `IDevice` in `hw_bridge.interfaces` and implement `open()`, `close()`, `read_reg()`, and `write_reg()`.
3.  **Error Handling**: Use specific exceptions (`ValueError`, `RuntimeError`, `ConnectionError`). Provide descriptive messages.
4.  **Resource Cleanup**: Always use context managers (`__enter__`/`__exit__`) or `finally` blocks for hardware handles.
5.  **State Tracking**: Track hardware connection state with a private `_is_open` boolean and a public property.

## Project Structure & Git Workflow

- **Tests**: Mirror the source code structure in the `tests/` directory.
- **Test Coverage**: Focus on both "Happy Path" success and robust edge-case/error handling.
- **Commit Messages**: Clear, descriptive English messages (e.g., "Add support for Raspberry Pi SMBus 2.0").
- **Safety**: **DO NOT** commit hardware secrets, API keys, or credentials.
- **Review**: Ensure type hints, docstrings, and error handling are complete before finishing a task.

## Git Safety Protocol

When performing git operations, follow these safety rules:
1. **No Destructive Commands**: Never run `push --force`, `hard reset`, or skip hooks unless explicitly asked.
2. **Commit Message Style**: Follow the repository's commit message style (usually concise 1-2 sentences).
3. **Branching**: Create feature branches for non-trivial changes.
4. **Pull Requests**: Provide a clear summary of changes in the PR body.

## Skills & Automated Workflows

Leverage the tools in `.opencode/skills/` for specialized tasks:
1.  **rebuild-library**: Use to sync `ic_psd3/library/` with new XML definitions. Rebuilds `auto_class.py` and `aves_class.py`.
2.  **simple-test-runner**: Execute PSD3 tests from markdown specifications (`tests/specs/`). Supports dry-run for library indexing.
3.  **aves-script-builder**: From MD function definition and Python code auto-generate AVES register configuration script.
4.  **chip-xml-builder**: Through config file drive generate chip level XML register define file.

## Best Practices for Coding Agents

1. **Grep and Glob First**: Before modifying code, use `grep` and `glob` extensively to understand the codebase structure and naming patterns.
2. **Context Matters**: Read surrounding code and existing tests to ensure your changes integrate naturally.
3. **Self-Verification**: Write unit tests for new logic whenever possible.
4. **Incremental Changes**: Make small, logical commits if multiple tasks are requested.
5. **Ask for Clarification**: If a task is ambiguous or requires significant architectural changes, confirm with the user first.
6. **Hardware Safety**: Since this project interacts with physical hardware, be extremely careful with register write operations. Verify addresses and bit masks twice.

## Key Design Patterns & Architectures

1.  **Factory Pattern**: Use `factory.py` for driver and instrument instantiation.
2.  **Manager Pattern**: Centralized management via `InstrumentManager` or `DeviceManager`.
3.  **Config-Driven**: Extensive use of YAML/JSON for environment and device settings.
4.  **Context Management**: Implement `__enter__`/`__exit__` for all hardware-interacting classes.
5.  **Interface-Based Development**: Ensure all drivers strictly follow the `IDevice` or `IInstrument` contracts.

---
*Last updated: 2026-02-24*
