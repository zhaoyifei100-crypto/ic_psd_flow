---
name: email
description: Email templates for user notifications
---

# Email Templates

## 模板 1: Key 创建成功通知

**使用场景**: 创建新 Key 后发送给用户

**Subject**: 
```
[LiteLLM] Your API Key is Ready - {alias}
```

**Body**:
```
Hi,

Your LiteLLM API access has been created successfully.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 API KEY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{key}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 BUDGET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly Limit: ${budget}
Reset: 1st of each month

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 API ENDPOINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{api_url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AVAILABLE MODELS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• qwen3.5-plus (Alibaba)
• kimi-k2.5 (Moonshot)
• deepseek-v3.2-exp (DeepSeek)
• glm-5 (Zhipu)
• claude-haiku-4.5 (Anthropic)
• gpt-3.5-turbo (OpenAI)
• gemini-3.1-pro (Google)
• gemini-3-flash (Google)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ OPENCODE CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Save the attached "opencode.json" to:
   ~/.config/opencode/opencode.json

2. Or manually configure with these settings:
   
   Base URL: {api_url}
   API Key: {key}
   
   Provider ID: gsai
   NPM Package: @ai-sdk/openai-compatible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Configure opencode (see above)
2. Select model: gsai/qwen3.5-plus
3. Start chatting!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 KEY INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alias: {alias}
Created: {created_at}
Status: Active

Need help? Contact your administrator.

Best regards,
LiteLLM Team
```

---

## 模板 2: Key 信息详情

**使用场景**: 向用户发送 Key 的完整信息

**Subject**:
```
[LiteLLM] Key Information - {alias}
```

**Body**:
```
Hi,

Your LiteLLM API access details:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 API CREDENTIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key: {key}
Alias: {alias}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly Budget: ${budget}
Current Spend: ${spend}
Usage: {usage_percent}%
Reset Date: {reset_date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 API ENDPOINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{api_url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For opencode users:
• Download and save the attached config file
• Location: ~/.config/opencode/opencode.json
• Or use: Base URL + API Key (see above)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 CURRENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: {status}
Last Active: {last_active}

Best regards,
LiteLLM Team
```

---

## 模板 3: Budget Alert (预算告警)

**使用场景**: 预算使用超过阈值时

**Subject**:
```
[LiteLLM Alert] Budget {usage_percent}% Used - {alias}
```

**Body**:
```
Hi,

Your LiteLLM API key is approaching its budget limit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ BUDGET ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key: {key}
Alias: {alias}

Current Usage:
• Spent: ${spend}
• Budget: ${budget}
• Usage: {usage_percent}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When your budget reaches 100%, this key will be
automatically suspended until the next reset.

Next Reset: {reset_date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 RECOMMENDED ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Monitor your usage
2. Contact admin if you need more budget
3. Consider optimizing API calls

Key Status: {status}

Best regards,
LiteLLM Team
```

---

## 模板 4: Key Suspended (Key 已暂停)

**使用场景**: Key 被暂停时通知用户

**Subject**:
```
[LiteLLM Alert] Key Suspended - {alias}
```

**Body**:
```
Hi,

Your LiteLLM API key has been suspended.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 SUSPENSION DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key: {key}
Alias: {alias}
Reason: {reason}
Suspended At: {suspended_at}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• This key can no longer make API calls
• Applications using this key will fail
• Existing configurations need to be updated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔓 TO REACTIVATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contact your administrator for assistance:
• Email: {admin_email}
• Or reply to this email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FINAL USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spent: ${total_spend}
Budget: ${budget}

We apologize for any inconvenience.

Best regards,
LiteLLM Team
```

---

## 模板 5: Monthly Report (月度报告)

**使用场景**: 每月发送用量报告

**Subject**:
```
[LiteLLM Report] Monthly Usage - {month}
```

**Body**:
```
Hi,

Your LiteLLM monthly usage report.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY - {month}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key: {key} ({alias})

Usage:
• Total Requests: {total_requests}
• Total Tokens: {total_tokens}
• Cost: ${total_cost}
• Budget: ${budget}
• Remaining: ${remaining_budget}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔝 TOP MODELS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{top_models_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 BUDGET STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usage: {usage_percent}%
Status: {budget_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 YOUR API DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Endpoint: {api_url}
Key: {key}

Best regards,
LiteLLM Team
```

---

## 变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| {key} | API Key | sk-xxxx... |
| {alias} | Key 别名 | dev-key |
| {budget} | 预算金额 | 50.00 |
| {spend} | 当前花费 | 42.50 |
| {usage_percent} | 使用百分比 | 85% |
| {api_url} | API 地址 | https://www.gsaisg.top/v1 |
| {created_at} | 创建时间 | 2026-03-10 |
| {reset_date} | 重置日期 | 2026-04-01 |
| {status} | 状态 | Active / Suspended |
| {reason} | 暂停原因 | Budget exceeded |
| {admin_email} | 管理员邮箱 | admin@company.com |

---

## 附件说明

模板 1 和 2 通常附带 opencode.json 配置文件，内容格式：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "gsai": {
      "name": "GSAI",
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "{api_url}",
        "apiKey": "{key}"
      },
      "models": { ... }
    }
  }
}
```

---

## AGENT 使用指南

使用 **gog skill** 发送邮件：

### 发送 Key 创建通知

```bash
# 1. 准备邮件内容
SUBJECT="[LiteLLM] Your API Key is Ready - dev-key"
BODY=$(cat << 'EOF'
Hi,

Your LiteLLM API access has been created successfully.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 API KEY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sk-xxxxx...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 BUDGET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly Limit: $50.00
Reset: 1st of each month

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 API ENDPOINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
https://www.gsaisg.top/v1

[更多内容省略...]
EOF
)

# 2. 使用 gog 发送邮件
gog gmail send \
  --to user@example.com \
  --subject "$SUBJECT" \
  --body "$BODY"
```

### 常用命令

```bash
# 发送 Key 创建通知
gog gmail send --to user@example.com --subject "[LiteLLM] Your API Key is Ready - {alias}" --body "{body}"

# 发送预算告警
gog gmail send --to user@example.com --subject "[LiteLLM Alert] Budget {usage_percent}% Used - {alias}" --body "{body}"

# 发送 Key 暂停通知
gog gmail send --to user@example.com --subject "[LiteLLM Alert] Key Suspended - {alias}" --body "{body}"

# 发送月度报告
gog gmail send --to user@example.com --subject "[LiteLLM Report] Monthly Usage - {month}" --body "{body}"
```

### 批量发送

```bash
# 给多个用户发送
for email in user1@example.com user2@example.com; do
  gog gmail send \
    --to "$email" \
    --subject "$SUBJECT" \
    --body "$BODY"
done
```

**注意**：发送前设置 `GOG_ACCOUNT=you@gmail.com` 避免重复指定账号。
