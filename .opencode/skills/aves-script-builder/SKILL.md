---
name: aves-script-builder
description: 从 MD 函数定义和 Python 代码自动生成 AVES 寄存器配置脚本
license: MIT
compatibility: opencode
metadata:
  author: Agent
  version: 2.0.0
---

## 功能概述

该 Skill 旨在帮助验证工程师将高层次的函数描述转换为可执行的 AVES 脚本。
它采用 **"MD -> Python Template -> Mock Execution -> AVES"** 的流转模式，利用 IDE 的自动补全能力减少手动查表。

**核心优势**：
1. **实际执行**：使用 MockDriver 实际运行 Python 代码，支持 `if/for/while` 等复杂逻辑。
2. **完整记录**：每次 `.w()` 调用都会生成独立的 B0 行，清晰展示时序。
3. **代码注释**：生成的 AVES 脚本包含原始 AutoClass 调用作为注释，便于调试。
4. **IDE 友好**：基于 AutoClass 体系，提供寄存器名自动补全。

---

## 工作流程

### 步骤 1：准备输入
用户需要提供一个包含函数名和描述的 Markdown 文件。
例如 `func_define.md`:
```markdown
# func_reset_clock
复位所有 clock domain

# func_start_saradc  
启动 SARADC
```
Agent 读到这个文件之后进行解析，提取函数定义并生成 Python 模板。

### 步骤 2：生成 Python 模板
Agent 调用工具生成模板文件：
```bash
python3 ic_psd2/src/aves_generator.py \
  --md <YOUR_MD_PATH> \
  --template ic_psd2/output/aves_template.py
```

### 步骤 3：准备 IDE 补全库（本地）
在用户开始编写逻辑前，Agent 必须在 `ic_psd2/output` 构建临时 `auto_class.py`，以便 IDE 提供准确的自动补全，且**不影响** `ic_psd3/library` 的状态。

Agent 调用 `ic_psd2/src/generate_local_autoclass.py`：
```bash
python3 ic_psd2/src/generate_local_autoclass.py <PATH_TO_YOUR_CHIP_XML> ic_psd2/output/auto_class.py
```

完成后检查 `ic_psd2/output/auto_class.py` 是否存在。用户在编写逻辑时，IDE 会识别同目录下的库。

Agent搜索要使用的寄存器：
  **只能**使用脚本在`*.json/*.XML/*.xlsx`里搜索
  **禁止**直接读取所有`*.json/*.XML/*.xlsx`的内容，会造成用户token消耗量过大

如果Agent**不能**给出使用的寄存器：
  **告知**用户："本地补全库已准备就绪，请在 IDE 中打开 `aves_template.py` 并利用 AutoClass 补全功能编写代码。完成后请告诉我。”
如果Agent**能**给出使用的寄存器：
  **告知**用户："本地补全库已准备就绪，以下是您需要使用的寄存器：\n{REGISTER_LIST}\n


### 步骤 4：用户编写逻辑

用户在 IDE 中打开 `aves_template.py`，使用 `AutoClass` 编写逻辑：
```python
def func_reset_clock():
    """复位所有 clock domain"""
    AutoClass.Misc_Inst.i2c_xtal_domain_rst.w(1)
    AutoClass.Misc_Inst.i2c_240m_domain_rst.w(1)
    # ... 更多写入
    AutoClass.Misc_Inst.i2c_xtal_domain_rst.w(0)  # 解除复位
    AutoClass.Misc_Inst.i2c_240m_domain_rst.w(0)
```

**支持的功能**：
- 位操作：`.w(0)` 或 `.w(1)`
- 字节操作：`.w(0xFF)`
- 读取操作：`.r()`（用于 read-modify-write）
- 复杂逻辑：`if/else`、`for` 循环、变量计算

### 步骤 5：构建 AVES 脚本
Agent 使用 **MockExecutor** 实际执行 Python 代码并生成 AVES：
```bash
python3 ic_psd2/src/mock_executor.py \
  --state ic_psd2/output/xml_state.json \
  --py ic_psd2/output/aves_template.py \
  --aves ic_psd2/output/generated_aves.txt \
  --per-func
```

**生成的 AVES 格式**：
```aves
:16-01 func_reset_clock:
; AutoClass commands:
;   AutoClass.Misc_Inst.i2c_xtal_domain_rst.w(1)
;   AutoClass.Misc_Inst.i2c_240m_domain_rst.w(1)
;   AutoClass.Misc_Inst.i2c_xtal_domain_rst.w(0)
;   AutoClass.Misc_Inst.i2c_240m_domain_rst.w(0)
B0 2000 02;
B0 2000 06;
B0 2000 02;
B0 2000 00;
End
```

**特点**：
- 每次 `.w()` 调用生成一行 B0（不合并）
- 函数前显示所有 AutoClass 命令作为注释
- B0 行以 `;` 结尾

---

## 交互指南

1. **询问 MD 路径**：
   "请提供包含函数定义的 Markdown 文件路径（例如 `ic_psd2/output/func.md`）"

2. **生成模板并准备本地库**：
   生成模板后，主动执行或询问用户执行 `generate_local_autoclass.py`，确保输出到 `ic_psd2/output/auto_class.py`。
   告知用户："模板已生成到 `ic_psd2/output/aves_template.py`，且本地 IDE 补全库已在 `ic_psd2/output` 准备就绪（不影响 psd3 库）。请在 IDE 中打开并利用 AutoClass 补全功能填写代码。完成后请告诉我。"

3. **构建脚本**：
   接收到用户确认后，执行 mock_executor 并展示生成的 AVES 内容（前几行或全量）。

---

## 注意事项

- **Mock 执行**：使用 `mock_executor.py` 而非旧的 `aves_generator.py`，支持完整 Python 语法。
- **不合并写入**：每次 `.w()` 都生成独立的 B0 行，如需延时请在代码中显式控制。
- **虚拟 I2C**：MockDriver 维护虚拟 I2C 内存，读取操作会反映之前写入的值。
- **依赖文件**：需要 `xml_state.json`（由 chip_builder 生成）作为默认值来源。

---

## 文件说明

- `ic_psd2/src/aves_generator.py` - 仅用于从 MD 生成 Python 模板
- `ic_psd2/src/mock_driver.py` - 虚拟 I2C 驱动器，维护内存状态
- `ic_psd2/src/mock_executor.py` - 执行 Python 脚本并生成 AVES
- `ic_psd2/src/generate_local_autoclass.py` - 生成本地 IDE 补全库
