---
name: litellm_manage
description: LiteLLM Gateway Management - Official API Implementation
metadata:
  {
    "openclaw": {
      "emoji": "🖥️",
      "requires": { "env": ["LITELLM_SSH_KEY"] }
    }
  }
---

# LiteLLM Management Skill

Comprehensive CLI for LiteLLM gateway management using official API.

**Docs:** https://docs.litellm.ai/docs/proxy/management_cli

## Quick Start

```bash
# Set SSH key path
export LITELLM_SSH_KEY=~/.ssh/ecs_key_backup

# Get help
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py --help

# Check status
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py status

# Generate opencode config (for using with opencode CLI)
python3 openclaw_skill/litellm_manage/scripts/scan_models.py \
  -u https://www.gsaisg.top/v1 -k sk-xxxx
```

---

## Commands

### 1. Status

```bash
# Check service health
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py status
```

Shows: Service health, available models, key count, team count

---

### 2. Key Management

```bash
# List keys
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key list

# Generate key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key generate \
  --alias "员工A" --budget 20

# Generate key with models
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key generate \
  --alias "研发" --budget 10 --models "qwen3.5-plus,kimi-k2.5"

# Update key settings
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key update \
  --key sk-xxx --budget 30 --models "qwen3.5-plus"

# Suspend (disable) key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key suspend \
  --key sk-xxx

# Activate (re-enable) key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key activate \
  --key sk-xxx --budget 20

# Reset key quota/spend
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key quota-reset \
  --key sk-xxx

# Get key info
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key info \
  --key sk-xxx

# Delete key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key delete \
  --key sk-xxx

# Regenerate (rotate) key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py key regenerate \
  --key sk-xxx
```

---

### 3. User Management

```bash
# List users
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py user list

# Create user
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py user new \
  --username "员工" --budget 20 --email "user@example.com"

# Get user info
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py user info \
  --user-id xxx

# Update user
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py user update \
  --user-id xxx --budget 50 --alias "新员工"

# Delete user
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py user delete \
  --user-id xxx
```

---

### 4. Team Management

```bash
# List teams
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team list

# Create team
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team new \
  --name "研发组" --budget 100

# Get team info
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team info \
  --team-id xxx

# Update team
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team update \
  --team-id xxx --budget 200 --alias "新研发组"

# Add member to team
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team add-member \
  --team-id xxx --user-id yyy --role admin

# Remove member from team
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team remove-member \
  --team-id xxx --user-id yyy

# Delete team
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py team delete \
  --team-id xxx
```

---

### 5. Model Testing

```bash
# Test model (uses admin key by default)
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py test \
  --model qwen3.5-plus

# Test with specific key
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py test \
  --model kimi-k2.5 --key sk-xxx
```

---

### 6. Config Generation

```bash
# Generate OpenAI-compatible config
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py config openai \
  --output ~/.openai.json
```

---

### 7. Opencode Config Generator (scan_models.py)

扫描 LiteLLM 可用模型并生成 opencode 配置文件。

**功能特点：**
- 自动扫描 `/v1/models` 接口获取所有可用模型
- 根据模型 ID 智能推断参数（context window、output limit、capabilities）
- 支持 GPT、Claude、Llama、Gemini、Qwen、DeepSeek 等主流模型
- 自动过滤 embedding、dall-e、tts、whisper 等非聊天模型

**使用方法：**

```bash
# 基础用法 - 输出到 stdout
python3 openclaw_skill/litellm_manage/scripts/scan_models.py \
  -u https://www.gsaisg.top/v1 \
  -k sk-litellm-admin-key-change-me

# 保存到文件
python3 openclaw_skill/litellm_manage/scripts/scan_models.py \
  -u https://www.gsaisg.top/v1 \
  -k sk-litellm-admin-key-change-me \
  -o ~/opencode_config.json

# 生成压缩格式的 JSON
python3 openclaw_skill/litellm_manage/scripts/scan_models.py \
  -u https://www.gsaisg.top/v1 \
  -k sk-litellm-admin-key-change-me \
  --compact

# 使用生成的 key（推荐）
python3 openclaw_skill/litellm_manage/scripts/scan_models.py \
  -u https://www.gsaisg.top/v1 \
  -k sk-xxxx \
  -o ~/.config/opencode/opencode.json
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `-u, --url` | API Base URL | `https://www.gsaisg.top/v1` |
| `-k, --key` | API Key | `sk-xxxx` |
| `-o, --output` | 输出文件路径 | `~/.config/opencode/opencode.json` |
| `-p, --pretty` | 格式化 JSON（默认） | - |
| `-c, --compact` | 压缩 JSON | - |

**当前可用模型（2026-03-10）：**

| 模型 | 参数 | 能力 |
|------|------|------|
| qwen3.5-plus | 32K / 8K | tool_call |
| kimi-k2.5 | 128K / 4K | tool_call |
| deepseek-v3.2-exp | 64K / 4K | tool_call |
| glm-5 | 32K / 4K | tool_call |
| claude-haiku-4.5 | 100K / 4K | tool_call |
| gpt-3.5-turbo | 4K / 4K | tool_call |
| gemini-3.1-pro | 32K / 4K | tool_call |
| gemini-3-flash | 32K / 4K | tool_call |

**安全建议：**

如果担心 API key 泄露，生成配置后可手动修改：

```bash
# 1. 设置环境变量
export GSAI_API_KEY=your-api-key

# 2. 编辑配置文件，将 apiKey 改为：
"apiKey": "{env:GSAI_API_KEY}"
```

**配置示例：**

生成的配置文件格式：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "gsai": {
      "name": "GSAI",
      "npm": "@ai-sdk/openai-compatible",
      "env": [],
      "models": {
        "qwen3-5-plus": {
          "id": "qwen3.5-plus",
          "name": "qwen3.5-plus",
          "tool_call": true,
          "reasoning": false,
          "limit": {
            "context": 32000,
            "output": 8192
          }
        }
      },
      "options": {
        "baseURL": "https://www.gsaisg.top/v1",
        "apiKey": "sk-xxxx"
      }
    }
  }
}
```

---

### 8. Service Control

```bash
# Restart LiteLLM
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py restart

# View logs
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py logs --lines 100
```

---

## Scripts Overview

| 脚本 | 用途 | 位置 |
|------|------|------|
| `litellm_manager.py` | LiteLLM 管理 CLI | `scripts/litellm_manager.py` |
| `scan_models.py` | 扫描模型并生成 opencode 配置 | `scripts/scan_models.py` |

---

## Official API Endpoints

| Feature | Endpoint | Method |
|---------|----------|--------|
| Key List | `/key/list` | GET |
| Key Generate | `/key/generate` | POST |
| Key Update | `/key/update` | POST |
| Key Delete | `/key/delete` | POST |
| Key Info | `/key/info` | GET |
| Key Regenerate | `/key/regenerate` | POST |
| User List | `/user/list` | GET |
| User Create | `/user/new` | POST |
| User Update | `/user/update` | POST |
| User Delete | `/user/delete` | POST |
| User Info | `/user/info` | GET |
| Team List | `/team/list` | GET |
| Team Create | `/team/new` | POST |
| Team Update | `/team/update` | POST |
| Team Delete | `/team/delete` | POST |
| Team Info | `/team/info` | GET |
| Team Member Add | `/team/member_add` | POST |
| Team Member Delete | `/team/member_delete` | POST |
| Health | `/health` | GET |
| Restart | `/admin/reload` | POST |

---

## Configuration

The skill uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `LITELLM_HOST` | LiteLLM host | 8.216.45.80 |
| `LITELLM_PORT` | LiteLLM API port | 4000 |
| `LITELLM_SSH_PORT` | SSH port for VPS access | 2222 |
| `LITELLM_SSH_KEY` | Path to SSH private key | ~/.ssh/ecs_key |
| `SSH_USER` | SSH username | root |

---

## TODO: Future Enhancements

### 4. Budget Management [TODO]

```bash
# Set key budget
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py budget key <key> [amount]

# Set user budget
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py budget user <user> [amount]

# Set team budget
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py budget team <team> [amount]

# Generate spend report
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py budget report

# Set budget alert threshold
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py budget alert --threshold 80%
```

**Planned Features:**
- Independent budget management commands
- Spend tracking and reporting
- Alert threshold configuration

---

### 5. Usage Monitoring & Reports [TODO]

```bash
# Generate usage report
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py report daily|weekly|monthly

# Export report
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py report export <format>

# Top models by usage
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py report top-models

# Top users by usage
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py report top-users
```

**Planned Features:**
- Time-based usage reports
- Export formats (CSV, JSON)
- Usage analytics and rankings

---

### 6. Configuration Management [TODO]

```bash
# List available models
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py config list-models

# Export full configuration
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py config export

# Import configuration from backup
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py config import <file>
```

**Planned Features:**
- Model discovery and listing
- Full configuration backup/restore
- Multi-format config support

---

### 7. System Operations [TODO]

```bash
# Backup configuration
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py backup

# Restore configuration
python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py restore <backup-file>
```

**Planned Features:**
- Automated backups
- Point-in-time recovery
- Configuration versioning

---

## Troubleshooting

### SSH Connection Issues

```bash
# Test SSH connection
ssh -i ~/.ssh/ecs_key_backup -p 2222 root@8.216.45.80 "echo 'OK'"

# Check SSH key permissions
chmod 600 ~/.ssh/ecs_key_backup
```

### API Errors

- Ensure master key is accessible via SSH
- Check LiteLLM service status: `python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py status`
- View logs: `python3 openclaw_skill/litellm_manage/scripts/litellm_manager.py logs --lines 100`

## Testing

The skill includes a comprehensive test suite using pytest.

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_key_management.py   # Key lifecycle tests (10 test cases)
├── test_user_management.py  # User lifecycle tests (12 test cases)
├── test_team_management.py  # Team lifecycle tests (14 test cases)
├── test_other_commands.py   # Status/config/service tests (19 test cases)
└── test_integration.py      # Integration tests (26 test cases)
```

**Total: 81 test cases**

### Running Tests

```bash
cd openclaw_skill/litellm_manage

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_key_management.py -v

# Run with coverage
python -m pytest tests/ --cov=scripts --cov-report=html
```

### Test Coverage

| Module | Commands | Test Cases |
|--------|----------|------------|
| Key Management | list, generate, update, suspend, activate, quota-reset, info, delete, regenerate | 10 |
| User Management | list, new, info, update, delete | 12 |
| Team Management | list, new, info, update, add-member, remove-member, delete | 14 |
| Other Commands | status, test, config, restart, logs | 19 |
| Config Tools | scan_models (opencode config generator) | - |
| Integration | argument parsing, routing, error handling | 26 |

### Key Test Features

- **Mock-based testing**: All API calls and SSH commands are mocked
- **Fast execution**: Tests run in seconds without network access
- **Comprehensive coverage**: Tests success, failure, and edge cases
- **Fixtures**: Shared test data and mock objects in `conftest.py`

### Live Integration Testing

To run tests against the actual LiteLLM server:

```bash
export LITELLM_SSH_KEY=~/.ssh/ecs_key_backup

# Test all basic operations
python3 openclaw_skill/litellm_manage/tests/integration_test_live.py
```

**Verified Operations (2026-03-10):**

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

**Known Issues Fixed:**
- `key info` was failing because `/key/list` returns key hashes, not full objects. Fixed by adding `_find_key_by_input()` helper function that uses `/key/info` endpoint.

---

*Last updated: 2026-03-10*
