# Testing Guide

This document describes the comprehensive test suite for the `litellm_manage` skill.

## Overview

The skill includes **81 test cases** covering all functionality using pytest.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_key_management.py   # Key lifecycle tests (10 test cases)
├── test_user_management.py  # User lifecycle tests (12 test cases)
├── test_team_management.py  # Team lifecycle tests (14 test cases)
├── test_other_commands.py   # Status/config/service tests (19 test cases)
├── test_integration.py      # Integration tests (26 test cases)
└── integration_test_live.py # Live SSH integration tests
```

## Test Coverage

| Module | Commands | Test Cases |
|--------|----------|------------|
| Key Management | list, generate, update, suspend, activate, quota-reset, info, delete, regenerate | 10 |
| User Management | list, new, info, update, delete | 12 |
| Team Management | list, new, info, update, add-member, remove-member, delete | 14 |
| Other Commands | status, test, config, restart, logs | 19 |
| Config Tools | scan_models (opencode config generator) | - |
| Integration | argument parsing, routing, error handling | 26 |
| **Total** | | **81** |

## Running Tests

### Prerequisites

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
cd openclaw_skill/litellm_manage
python -m pytest tests/ -v
```

### Run Specific Test File

```bash
python -m pytest tests/test_key_management.py -v
```

### Run Specific Test

```bash
python -m pytest tests/test_key_management.py::TestKeyGenerate::test_key_generate_success -v
```

### Run with Coverage

```bash
python -m pytest tests/ --cov=scripts --cov-report=html
```

## Key Test Features

- **Mock-based testing**: All API calls and SSH commands are mocked for fast, isolated testing
- **Fast execution**: Tests run in seconds without network access
- **Comprehensive coverage**: Tests success, failure, and edge cases
- **Fixtures**: Shared test data and mock objects in `conftest.py`

## Live Integration Testing

To run tests against the actual LiteLLM server via SSH:

```bash
export LITELLM_SSH_KEY=~/.ssh/ecs_key_backup

# Run live integration test
python3 openclaw_skill/litellm_manage/tests/integration_test_live.py
```

### Verified Operations (2026-03-10)

| Command | Status | Notes |
|---------|--------|-------|
| `status` | ✅ Working | Shows 8 healthy models |
| `key list` | ✅ Working | Lists all keys |
| `key generate` | ✅ Working | Creates keys with budget/models |
| `key info` | ✅ Working | Fixed: now uses `/key/info` API |
| `key update` | ✅ Working | Updates budget, models, etc. |
| `key suspend` | ✅ Working | Sets budget to 0 |
| `key activate` | ✅ Working | Restores budget |
| `key delete` | ✅ Working | Deletes keys |
| `user list` | ✅ Working | Shows all users |
| `user new` | ✅ Working | Creates users with budget |
| `team list` | ✅ Working | Shows all teams |
| `team new` | ✅ Working | Creates teams with budget |

### Known Issues Fixed

- `key info` was failing because `/key/list` returns key hashes, not full objects. Fixed by adding `_find_key_by_input()` helper function that uses `/key/info` endpoint.

## Fixtures

The `conftest.py` file provides the following fixtures:

- `mock_env_vars`: Mock environment variables
- `mock_api_response`: Mock successful API response
- `mock_api_error`: Mock error API response
- `sample_key_data`: Sample key data dictionary
- `sample_user_data`: Sample user data dictionary
- `sample_team_data`: Sample team data dictionary
- `mock_ssh_exec`: Mock SSH execution function
- `mock_api_call`: Mock API call function
- `mock_subprocess_run`: Mock subprocess.run for SSH commands
- `mock_get_master_key`: Mock get_master_key function

## Writing New Tests

1. Add test file in `tests/` directory
2. Import pytest and the module under test
3. Use fixtures from `conftest.py`
4. Follow naming convention: `test_*.py`
5. Use descriptive test function names: `test_<functionality>_<scenario>`

### Example Test

```python
def test_key_generate_with_models(mock_api_call, capsys):
    """Test generating key with specific models."""
    mock_api_call.return_value = {"key": "sk-new-key"}
    
    args = MagicMock()
    args.alias = "test"
    args.models = "model1,model2"
    
    manager.cmd_key_generate(args)
    
    captured = capsys.readouterr()
    assert "API Key created" in captured.out
```

## CI/CD Integration

Add to your CI pipeline:

```yaml
# Example GitHub Actions
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - run: pip install pytest pytest-cov
    - run: cd openclaw_skill/litellm_manage && python -m pytest tests/ --cov=scripts
```

## Test Runners

### Using run_tests.py

A convenient test runner is provided:

```bash
cd openclaw_skill/litellm_manage
python run_tests.py

# With options
python run_tests.py --cov
python run_tests.py tests/test_key_management.py
```

---

*Last updated: 2026-03-10*
