---
name: litellm_manage
description: LiteLLM Gateway Management - Official API Implementation
metadata:
  {
    "openclaw": {
      "emoji": "🖥️",
      "requires": { "env": ["LITELLM_UI_KEY"] }
    }
  }
---

# LiteLLM Management Skill

Comprehensive CLI for LiteLLM gateway management using official API.

**Docs:** https://docs.litellm.ai/docs/proxy/management_cli

## Quick Start

```bash
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py --help
```

---

## Commands

### 1. Status

```bash
# Check service health
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py status
```

Shows: Service health, available models, key count

---

### 2. Key Management

```bash
# List keys
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key list

# Generate key
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key generate \
  --alias "员工A" --budget 20

# Generate key with models
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key generate \
  --alias "研发" --budget 10 --models "qwen3.5-plus,kimi-k2.5"

# Get key info
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key info \
  --key sk-xxx

# Delete key
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key delete \
  --key sk-xxx

# Regenerate (rotate) key
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py key regenerate \
  --key sk-xxx
```

---

### 3. User Management

```bash
# List users
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py user list

# Create user
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py user new \
  --username "员工" --budget 20

# Delete user
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py user delete \
  --user-id xxx
```

---

### 4. Team Management

```bash
# List teams
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py team list

# Create team
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py team new \
  --name "研发组" --budget 100
```

---

### 5. Model Testing

```bash
# Test model (uses admin key by default)
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py test \
  --model qwen3.5-plus

# Test with specific key
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py test \
  --model kimi-k2.5 --key sk-xxx
```

---

### 6. Config Generation

```bash
# Generate OpenAI-compatible config
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py config openai \
  --output ~/.openai.json
```

---

### 7. Service Control

```bash
# Restart LiteLLM
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py restart

# View logs
python3 ~/.openclaw/workspace/skills/litellm_manage/scripts/litellm_manager.py logs --lines 100
```

---

## Official API Endpoints

| Feature | Endpoint | Method |
|---------|----------|--------|
| Key List | `/key/list` | GET |
| Key Generate | `/key/generate` | POST |
| Key Delete | `/key/delete` | POST |
| Key Info | `/key/info` | GET |
| Key Regenerate | `/key/regenerate` | POST |
| User List | `/user/list` | GET |
| User Create | `/user/new` | POST |
| User Delete | `/user/delete` | POST |
| Team List | `/team/list` | GET |
| Team Create | `/team/new` | POST |
| Health | `/health` | GET |
| Restart | `/admin/reload` | POST |

---

## Current LiteLLM Info

- **Host:** 8.216.45.80
- **Port:** 4000
- **SSH Port:** 2222
- **Config Path:** /opt/litellm/
- **UI:** https://www.gsaisg.top (admin / ${LITELLM_UI_KEY})
