---
name: simple-test-runner
description: 芯片PSD3测试执行器，由Agent主导PSD3测试的执行，提供库函数索引
license: MIT
compatibility: opencode
metadata:
  author: yfzhao
  version: 1.0.0
---

# Simple Test Runner Skill

## 描述

轻量级测试执行器。本 Skill 仅提供基础功能，**代码生成由 AGENT 直接完成**。

## 设计理念

- **极简**: 只保留最必要的功能（扫描库、执行测试）
- **Agent 原生**: 代码生成、规格解析全部由 AGENT 直接完成
- **动态发现**: 自动扫描库构建索引，供 AGENT 参考

## 使用方法

### 第一步：生成库索引

```bash
python runner.py <testspec.md> --dry-run
```

这会：
1. **复制整个 `ic_psd3/library/` 到测试目录**（环境快照）
2. 扫描本地 library 构建函数索引，生成 `library_index.json`
3. **扫描 `ic_psd3/src/lab_instruments/instruments/` 下的所有驱动**，生成 `instruments.json`
4. **AGENT 现在可以基于索引生成代码**

**环境隔离**：每个测试都有自己的 library 快照，顶层文件的修改不会影响已通过的测试。

### 第二步：AGENT 生成代码

AGENT 读取 `testspec.md` + `library_index.json`，直接生成 `test_script.py`。

### 第三步：执行测试

```bash
python runner.py <testspec.md>
```

执行已生成的 `test_script.py`，显示里程碑和最终结果。

## 完整示例

```bash
# 1. 生成索引（AGENT 准备阶段）
python runner.py ic_psd3/tests/specs/phy/usb3_prbs.md --dry-run

# 2. AGENT 生成代码（AGENT 自动完成）
# AGENT 读取 testspec.md 和 library_index.json
# AGENT 生成 test_script.py

# 3. 执行测试
python runner.py ic_psd3/tests/specs/phy/usb3_prbs.md
```

## 输出结构

```
ic_psd3/tests/generated/<test_name>/
├── library/                # 库环境快照（dry-run 时复制）
│   ├── usb_common_class.py
│   ├── psd3_common_class.py
│   ├── aves_class.py
│   └── reg_define.py
├── library_index.json      # 库函数索引（AGENT 参考）
├── instruments.json        # 仪器驱动索引（AGENT 参考）
├── test_script.py          # AGENT 生成的可执行代码
├── exec.log               # 详细执行日志
└── summary.json           # 结构化结果
```

**仪器驱动发现**：
- `--dry-run` 时自动扫描 `ic_psd3/src/lab_instruments/instruments/` 目录
- 提取每个驱动的类名、初始化参数、公开方法
- 生成 `instruments.json` 供 AGENT 参考
- 例如：`tt5166_tcp_ctr.py` → `TemperatureController` 类的详细信息

**环境隔离设计**：
- `--dry-run` 阶段会复制整个 `ic_psd3/library/` 到测试目录
- 后续执行使用**本地**library，确保已通过测试不受顶层修改影响
- 如需重新同步库，删除 `library/` 目录后重新运行 `--dry-run`

## 参数说明

```bash
python runner.py <testspec.md> [选项]

选项:
  --output-dir <dir>    输出目录 (默认: ic_psd3/tests/generated/<test_name>)
  --library-dir <dir>   库目录 (默认: ic_psd3/library)
  --dry-run            仅生成索引，不执行
```

## 实现

**单个文件**: `runner.py`（约 280 行）

**核心功能**:
1. `scan_library()` - 扫描库并构建索引
2. `scan_instruments()` - 扫描仪器驱动并构建索引
3. `extract_instrument_class()` - 提取驱动类信息和初始化参数
4. `execute_test()` - 执行测试脚本，捕获输出
5. `main()` - CLI 入口点

**AGENT 职责**:
- 解析 testspec.md
- 使用 library_index.json 了解可用芯片库函数
- 使用 instruments.json 了解可用硬件驱动
- 直接生成 test_script.py（带 MILESTONE 打印）
- 调用 runner.py 执行测试

## 工作流程

```
Designer: /run-test testspec.md

Agent:
  1. 调用 runner.py --dry-run
      → 生成 library_index.json
      → 生成 instruments.json
  
  2. AGENT 直接生成代码
      → 读取 testspec.md
      → 读取 library_index.json（了解可用函数）
      → 读取 instruments.json（了解硬件驱动）
      → 生成 test_script.py（带里程碑打印）
  
  3. **告知**designer代码已经生成，需要修改（如有）
      **提示**designer检查TODO
      **等待**designer确认代码无误

  4. 调用 runner.py（无 --dry-run）
      → 执行 test_script.py
      → 显示里程碑和结果
```

## TestSpec 格式示例

```markdown
# PHY USB3 PRBS 测试

## 设备
- dut: GSU1K1 (i2c_port: 0, chip_addr: 0x58, type: ftdi)
- chamber: TemperatureController (ip: 192.168.6.211, port: 3000)

## 参数
- temperatures: [25, 85, 125]
- soak_time: 600
- prbs_duration: 5

## 测试流程
1. 复位芯片并上电
2. 初始化 PLL（无 SSC）
3. FOR temperature IN temperatures:
   - 设置温箱温度为 {temperature}°C
   - 等待 {soak_time} 秒
   - 初始化 USB3 PRBS 模式
   - 检查 PRBS {prbs_duration} 秒
```

## 标准导入模板

测试脚本位于 `ic_psd3/tests/generated/<test_name>/` 目录，Python 会自动将该目录加入 `sys.path`，因此直接导入即可：

```python
#!/usr/bin/env python3

# 标准库
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# 本地 library 模块（runner 在 dry-run 时已复制到测试目录）
from library.usb_common_class import USBCommonClass
from library.aves_class import AVESChipConfig
from library.psd3_common_class import PSD3CommonClass

# pip 安装的包
from hw_bridge import DeviceManager
```

**重要说明**：
- 无需修改 `sys.path`，当前目录已自动在 path 中
- `library/` 是 dry-run 阶段复制的本地快照，确保环境隔离
- `hw_bridge` 通过 `pip install -e ic_psd3/src/hw_bridge` 安装到 venv

## 注意事项
- 在当前环境下新建venv，安装requirements.txt后执行，特别注意要安装ic_psd3/src/hw_bridge
- library_index.json 位于每个测试的输出目录中
- 扫描**本地**library[usb_common_class.py, psd3_common_class.py, aves_class.py, reg_define.py]
- 代码生成完全由 AGENT 完成，本 Skill 只负责执行
- 所有生成文件使用覆盖模式

## 常见踩坑 ⚠️



### 1. 类名混淆

**问题**: 库中的类名与预期不符。

| 错误用法 | 正确类名 | 文件 |
|---------|---------|------|
| `AvesClass` | `AVESChipConfig` | aves_class.py |
| `USBCommonClass()` 无参初始化 | `USBCommonClass(device)` | usb_common_class.py |

**排查方法**:
```bash
grep "^class " ic_psd3/library/*.py
```

### 2. DeviceManager API 错误

**问题**: 使用了不存在的方法。

| 错误 | 正确 | 说明 |
|-----|-----|------|
| `device_manager.create_device()` | `device_manager.register()` | 应使用 register 方法 |
| `DeviceManager()` | `DeviceManager(auto_open=True)` | 需指定参数以正确初始化 |

**正确用法**:
```python
dm = DeviceManager(auto_open=True)
dut = dm.register(name="dut", driver_type="mock", i2c_port=0, chip_addr=0x58)
dm.close_all()  # 清理
```

### 3. 类初始化方式错误

**问题**: USBCommonClass 不是无参初始化的。

**❌ 错误**:
```python
usb_class = usb_common.USBCommonClass()
usb_class.set_device_manager(device_manager, "dut")
```

**✓ 正确**:
```python
usb_obj = usb_common.USBCommonClass(dut)  # 直接传设备对象
```

### 4. 直接寄存器访问 vs 类方法

**问题**: USBCommonClass 没有 `write_reg()` 方法，应通过设备对象访问。

**❌ 错误**:
```python
usb_obj.write_reg(CDR_UP_ADDR, 0x9E, 0x0F)
```

**✓ 正确**:
```python
dut.write_reg(CDR_UP_ADDR, 0x9E, 0x0F)  # 通过设备对象
```



### 5. 模拟设备 vs 真实硬件驱动

**问题**: 在非Windows系统运行，FTDI驱动不可用。

**症状**:
```
AttributeError: module 'ctypes' has no attribute 'windll'
```

**解决方案**:
```python
# 开发/演示阶段使用 mock 驱动
TEST_CONFIG = {
    "dut_type": "mock",  # ✓ 支持：mock, ftdi (Windows), pi
    ...
}
```

**可用驱动**:
- `mock` - 仿真设备，返回默认值（推荐用于开发）
- `ftdi` - 真实FTDI硬件（仅Windows + FTDI驱动）
- `pi` - Raspberry Pi I2C（仅Pi系统）

### 6. 缺失的作用域变量

**问题**: 在 try 块中初始化的变量在 finally 块中使用。

**❌ 错误**:
```python
try:
    device_manager = DeviceManager()
    # ...
finally:
    device_manager.close_all()  # 如果初始化失败，变量不存在
```

**✓ 正确**:
```python
device_manager = None
try:
    device_manager = DeviceManager()
    # ...
finally:
    if device_manager:
        device_manager.close_all()
```


### 7. 库函数索引理解不完全

**问题**: 生成的 library_index.json 中函数签名需要仔细解读。

**关键字段**:
- `args` - 完整的函数参数（包括类型提示）
- `docstring` - 文档字符串（说明参数含义）
- `methods` - 该类的所有方法

**使用示例**:
```python
# 库索引中看到:
"check_usb3_prbs_with_break": {
    "args": "self, pipe_addr: int, mins: int, unit: int",
    "docstring": "Check USB3.0 PRBS with break on error.\n\nReturns:\n    List: [error_count, check_result]"
}

# 应该这样调用:
prbs_result = usb_obj.check_usb3_prbs_with_break(
    pipe_addr=0x31,
    mins=5,
    unit=1
)
error_count = prbs_result[0]  # 返回值是列表，第一个元素是错误计数
```





