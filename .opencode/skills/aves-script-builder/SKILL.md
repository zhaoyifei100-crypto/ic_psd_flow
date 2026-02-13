---
name: aves-script-builder
description: 从 MD 函数定义和 Python 代码自动生成 AVES 寄存器配置脚本
license: MIT
compatibility: opencode
metadata:
  author: Agent
  version: 1.0.0
---

## 功能概述

该 Skill 旨在帮助验证工程师将高层次的函数描述转换为可执行的 AVES 脚本。
它采用 **"MD -> Python Template -> AVES"** 的流转模式，利用 IDE 的自动补全能力减少手动查表。

**核心优势**：
1. **自动合并**：多个位域写入同一字节时，自动合并为一条 AVES 命令。
2. **默认值补全**：未显式赋值的位将保留 XML 中的默认值。
3. **IDE 友好**：基于 AutoClass 体系，提供寄存器名自动补全。

---

## 工作流程

### 步骤 1：准备输入
用户需要提供一个包含函数名和描述的 Markdown 文件。
例如 `func_define.md`:

```markdown
# ChipInit
初始化基础时钟。

# AudioCfg
配置音频格式为 I2S。
```
Agent 读到这个文件之后进行解析，提取函数定义并生成 Python 模板

### 步骤 2：生成 Python 模板
Agent 调用工具生成模板文件：
```bash
python3 ic_psd2/src/aves_generator.py \
  --state ic_psd2/output/xml_state.json \
  --md <YOUR_MD_PATH> \
  --template ic_psd2/output/aves_template.py
```
Agent 不要尝试去psd3.import文件夹读取里面的旧文件

### 步骤 3：用户编写逻辑
用户在 IDE 中打开 `aves_template.py`，使用 `AutoClass` 编写逻辑：
```python
def AudioCfg():
    """配置音频格式为 I2S。"""
    AutoClass.AG.i2c_audio_format.w(0x1)
    AutoClass.AG.i2c_audio_width.w(0x18)
```

### 步骤 4：构建 AVES 脚本
Agent 解析 Python 代码并输出结果：
```bash
python3 ic_psd2/src/aves_generator.py \
  --state ic_psd2/output/xml_state.json \
  --py ic_psd2/output/aves_template.py \
  --aves ic_psd2/output/generated_aves.txt
```

---

## 交互指南

1. **询问 MD 路径**：
   "请提供包含函数定义的 Markdown 文件路径（例如 `ic_psd2/output/func.md`）"

2. **生成并展示模板**：
   生成模板后，告知用户："模板已生成到 `ic_psd2/output/aves_template.py`。请在 IDE 中打开并利用 AutoClass 补全功能填写代码。完成后请告诉我。"

3. **构建脚本**：
   接收到用户确认后，执行构建并展示生成的 AVES 内容（前几行或全量）。

---

## 注意事项
- **只支持写入**：AVES 脚本仅支持 `write_reg`，因此 Python 中的 `.r()` 调用将被忽略。
- **静态解析**：仅支持简单的赋值语句，不支持 `if/for` 等复杂逻辑。
- **位域对齐**：工具会自动处理跨字节字段。
