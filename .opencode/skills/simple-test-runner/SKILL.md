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
1. 扫描 `ic_psd3/library/*.py` 构建函数索引
2. 生成 `library_index.json` 到测试输出目录
3. **AGENT 现在可以基于索引生成代码**

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
# AGENT 生成 ic_psd3/tests/generated/usb3_prbs/test_script.py

# 3. 执行测试
python runner.py ic_psd3/tests/specs/phy/usb3_prbs.md
```

## 输出结构

```
ic_psd3/tests/generated/<test_name>/
├── library_index.json      # 库函数索引（AGENT 参考）
├── test_script.py          # AGENT 生成的可执行代码
├── exec.log               # 详细执行日志
└── summary.json           # 结构化结果
```

## 参数说明

```bash
python runner.py <testspec.md> [选项]

选项:
  --output-dir <dir>    输出目录 (默认: ic_psd3/tests/generated/<test_name>)
  --library-dir <dir>   库目录 (默认: ic_psd3/library)
  --dry-run            仅生成索引，不执行
```

## 实现

**单个文件**: `runner.py`（仅 199 行）

**三个核心功能**:
1. `scan_library()` - 扫描库并构建索引
2. `execute_test()` - 执行测试脚本，捕获输出
3. `main()` - CLI 入口点

**AGENT 职责**:
- 解析 testspec.md
- 使用 library_index.json 了解可用函数
- 直接生成 test_script.py（带 MILESTONE 打印）
- 调用 runner.py 执行测试

## 工作流程

```
Designer: /run-test testspec.md

Agent:
  1. 调用 runner.py --dry-run
     → 生成 library_index.json
  
  2. AGENT 直接生成代码
     → 读取 testspec.md
     → 读取 library_index.json（了解可用函数）
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
# USB3 PRBS 测试

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

## 注意事项

- library_index.json 位于每个测试的输出目录中
- 扫描包含: usb_common_class.py, psd3_common_class.py, aves_class.py, reg_define.py
- 代码生成完全由 AGENT 完成，本 Skill 只负责执行
- 所有生成文件使用覆盖模式
