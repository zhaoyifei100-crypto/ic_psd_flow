# Chip Test 自动化生成方案

## 1. 项目概述

### 1.1 目标
实现从自然语言测试需求到可执行Python测试代码的自动化生成，通过分层架构让Designer专注于业务逻辑，Agent负责代码工程化。

### 1.2 核心思想
- **Designer专注业务**：使用AutoClass编写寄存器级操作（享受IDE自动补全）
- **Agent负责工程**：解析需求、生成框架、转换代码、组装测试类
- **分层设计**：已有函数（GSU1K1_NTO_scripts）+ 用户自定义函数 + 测试流程编排

## 2. 架构设计

### 2.1 组合模式类结构

```python
# final_test.py 生成的代码结构
class TestSuite:
    """测试套件主类 - 由Agent自动生成"""
    
    def __init__(self, board):
        self.board = board
        # 组合模式：聚合两类功能
        self.scripts = GSU1K1_scripts(board)  # 已有函数库
        self.custom = CustomFuncs(board)       # 用户自定义函数
    
    def test_prbs(self):
        """
        PRBS测试流程 - 从test_spec.md解析生成
        """
        # Step 1: 调用已有函数
        self.scripts.func_01_01_Chip_Power_Up()
        
        # Step 2: 调用用户实现的函数
        self.custom.init_prbs(port_sel="UP")
        
        # Step 3: 延时
        time.sleep(0.5)
        
        # Step 4: 调用已有函数并检查结果
        result = self.scripts.break_min_check_prbs_error("UP", 5, 1)
        
        # Step 5: 断言
        assert result[1] == 'pass', f"PRBS测试失败: {result}"
        print("✓ PRBS测试通过")


class CustomFuncs:
    """
    用户自定义函数类 - Agent从custom_funcs.py转换生成
    AutoClass语法已自动转换为真实I2C代码
    """
    
    def __init__(self, board):
        self.board = board
    
    def init_prbs(self, port_sel="UP"):
        """
        初始化PRBS - 用户用AutoClass编写，Agent自动转换
        """
        # 原AutoClass代码:
        # AutoClass.PipeUp.i2c_pipe_prbs_mode.w(0x02)
        # AutoClass.PipeUp.i2c_tx_ser_rst_man.w(1)
        
        # 转换后的真实I2C代码:
        pipe_addr = self._get_pipe_addr(port_sel)
        self.board.writeBits(pipe_addr, 0x63, 1, 3, 0x02)   # PRBS模式
        self.board.writeBits(pipe_addr, 0x1E, 2, 1, 1)      # 复位
        time.sleep(0.1)
        self.board.writeBits(pipe_addr, 0x1E, 2, 1, 0)      # 释放复位
    
    def _get_pipe_addr(self, port_sel):
        """辅助函数：根据port_sel获取PIPE地址"""
        addr_map = {
            "UP": PipeUp, "DP1": PipeDp1, "DP2": PipeDp2,
            "DP3": PipeDp3, "DP4": PipeDp4
        }
        return addr_map.get(port_sel, PipeUp)


# 测试执行入口
if __name__ == "__main__":
    print("="*60)
    print("GSU1K1 芯片测试套件")
    print("="*60)
    
    # 初始化硬件连接
    board = phy_func(i2c_port=0)
    
    # 创建测试套件
    test_suite = TestSuite(board)
    
    # 运行测试
    try:
        test_suite.test_prbs()
        print("\n✓ 所有测试通过!")
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
    except Exception as e:
        print(f"\n✗ 运行时错误: {e}")
```

### 2.2 模块职责划分

| 模块 | 职责 | 生成方式 |
|------|------|----------|
| `GSU1K1_scripts` | 提供已有功能函数（如初始化、配置脚本） | 已存在，Agent扫描识别 |
| `CustomFuncs` | 用户自定义的寄存器级操作 | 用户用AutoClass编写，Agent转换 |
| `TestSuite` | 测试流程编排和执行 | Agent从MD解析生成 |

## 3. 工作流程

### 3.1 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 编写测试需求文档 (test_spec.md)                          │
│ ─────────────────────────────────────                           │
│ 用户用自然语言描述测试需求：                                       │
│ - 测试目标                                                       │
│ - 执行步骤（可调用已有函数或声明新函数）                            │
│ - 断言条件                                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Agent解析并生成Demo (demo_scripts.py)                    │
│ ────────────────────────────────────────────────                │
│ Agent自动：                                                       │
│ 1. 扫描GSU1K1_NTO_scripts.py获取已有函数列表                       │
│ 2. 识别test_spec.md中的新函数声明                                  │
│ 3. 生成带TODO的函数框架（使用AutoClass语法）                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: 用户实现自定义函数 (custom_funcs.py)                      │
│ ────────────────────────────────────────────                    │
│ 用户在VSCode中：                                                  │
│ 1. 打开demo_scripts.py                                           │
│ 2. 使用AutoClass自动补全填写寄存器操作                            │
│ 3. 保存为custom_funcs.py                                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Agent生成最终测试代码 (final_test.py)                    │
│ ────────────────────────────────────────────────                │
│ Agent自动：                                                       │
│ 1. 解析custom_funcs.py中的AutoClass调用                           │
│ 2. 转换为真实I2C代码（writeBits/readReg）                         │
│ 3. 从test_spec.md生成测试流程                                     │
│ 4. 组装TestSuite类                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: 执行测试                                                 │
│ ────────────────                                                │
│ python final_test.py                                             │
└─────────────────────────────────────────────────────────────────┘
```

## 4. 文件结构

### 4.1 目录布局

```
models/gsu_eval_es4/
├── GSU1K1_NTO_scripts.py          # 已有：功能函数库
├── gsu1001_phy_func.py            # 已有：phy_func类定义
├── auto_class.py                  # 已有：AutoClass定义（IDE用）
├── GSU1K1_NTO_reg_def.py          # 已有：寄存器地址定义
│
└── test_specs/                    # 测试规格目录
    ├── README.md                  # 本方案文档
    ├── usb3_prbs_test.md          # 示例：USB3 PRBS测试需求
    ├── usb2_rx_test.md            # 示例：USB2 RX测试需求
    ├── pll_lock_test.md           # 示例：PLL锁定测试需求
    │
    └── generated/                 # 生成的代码目录
        ├── demo_usb3_prbs.py      # 生成的Demo框架
        ├── custom_usb3_prbs.py    # 用户实现的函数
        └── final_usb3_prbs.py     # 最终可执行代码
```

### 4.2 文件格式说明

#### test_spec.md 格式

```markdown
# USB3.0 PRBS测试

## 测试目标
验证USB3.0 PIPE接口的PRBS误码率测试功能。

## 前置条件
- 芯片已上电
- 参考时钟稳定

## 测试步骤

1. **芯片初始化**
   - 调用已有函数：`func_01_01_Chip_Power_Up()`
   - 调用已有函数：`func_01_01_02_PLL_no_ssc_init()`

2. **PRBS初始化**（需要新函数 `init_prbs`）
   - 配置PRBS模式为PRBS7
   - 复位Serializer
   - 使能PRBS检查

3. **等待稳定**
   - 延时500ms

4. **检查PRBS错误**
   - 调用已有函数：`break_min_check_prbs_error("UP", 5, 1)`
   - 返回结果：`[error_count, status]`

5. **结果断言**
   - `status` 必须为 `'pass'`
   - `error_count` 必须 < 10

## 清理操作
- 关闭PRBS模式
- 恢复默认配置

## 备注
- 测试端口：PipeUp
- 测试时长：约6秒
```

#### demo_scripts.py 格式

```python
"""
AutoClass Demo - USB3.0 PRBS测试
由Agent自动生成，请使用AutoClass完成TODO部分
"""

class CustomFuncs:
    """
    自定义函数类
    请在此实现test_spec.md中声明的新函数
    """
    
    def __init__(self, board):
        self.board = board
    
    def init_prbs(self, port_sel="UP"):
        """
        初始化PRBS
        
        TODO: 请使用AutoClass语法实现：
        - AutoClass.PipeUp.REG_NAME.w(value)
        - AutoClass.PipeUp.REG_NAME.r()
        
        可用PAGE: PipeUp, PipeDp1, PipeDp2, PipeDp3, PipeDp4
        提示：使用VSCode可获得自动补全
        """
        # ===== 请在此处实现 =====
        
        pass
        
        # =======================


# 可用已有函数（来自GSU1K1_NTO_scripts）：
# - func_01_01_Chip_Power_Up()
# - func_01_01_02_PLL_no_ssc_init()
# - break_min_check_prbs_error(port, mins, unit)
# ... 更多函数请查看GSU1K1_NTO_scripts.py
```

#### custom_funcs.py 格式（用户编写）

```python
"""
用户自定义函数 - USB3.0 PRBS测试
使用AutoClass语法编写，将被Agent自动转换
"""

class CustomFuncs:
    def __init__(self, board):
        self.board = board
    
    def init_prbs(self, port_sel="UP"):
        """初始化PRBS测试模式"""
        # 使用AutoClass访问寄存器（VSCode自动补全可用）
        AutoClass.PipeUp.i2c_pipe_prbs_mode.w(0x02)        # PRBS7模式
        AutoClass.PipeUp.i2c_tx_ser_rst_man.w(1)           # 复位
        time.sleep(0.1)
        AutoClass.PipeUp.i2c_tx_ser_rst_man.w(0)           # 释放复位
        AutoClass.PipeUp.i2c_prbs_en.w(1)                  # 使能PRBS
        AutoClass.PipeUp.i2c_prbs_compare_en.w(1)          # 使能比较
```

#### final_test.py 格式（Agent生成）

```python
"""
USB3.0 PRBS测试 - 最终可执行代码
由Agent自动生成，请勿手动修改
生成时间: 2024-XX-XX XX:XX:XX
来源规格: test_specs/usb3_prbs_test.md
"""

import time
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gsu1001_phy_func import phy_func
from GSU1K1_NTO_scripts import GSU1K1_scripts
from GSU1K1_NTO_reg_def import *


class CustomFuncs:
    """用户自定义函数 - AutoClass已自动转换"""
    
    def __init__(self, board):
        self.board = board
    
    def init_prbs(self, port_sel="UP"):
        """初始化PRBS测试模式"""
        pipe_addr = self._get_pipe_addr(port_sel)
        
        # AutoClass转换后的真实I2C代码
        self.board.writeBits(pipe_addr, 0x63, 1, 3, 0x02)   # i2c_pipe_prbs_mode
        self.board.writeBits(pipe_addr, 0x1E, 2, 1, 1)      # i2c_tx_ser_rst_man
        time.sleep(0.1)
        self.board.writeBits(pipe_addr, 0x1E, 2, 1, 0)      # i2c_tx_ser_rst_man
        self.board.writeBits(pipe_addr, 0x63, 4, 1, 1)      # i2c_prbs_en
        self.board.writeBits(pipe_addr, 0x64, 7, 1, 1)      # i2c_prbs_compare_en
    
    def _get_pipe_addr(self, port_sel):
        """获取PIPE地址"""
        addr_map = {
            "UP": PipeUp, "DP1": PipeDp1, "DP2": PipeDp2,
            "DP3": PipeDp3, "DP4": PipeDp4
        }
        return addr_map.get(port_sel, PipeUp)


class TestSuite:
    """USB3.0 PRBS测试套件"""
    
    def __init__(self, board):
        self.board = board
        self.scripts = GSU1K1_scripts(board)
        self.custom = CustomFuncs(board)
        self.results = []
    
    def test_prbs(self):
        """
        USB3.0 PRBS测试
        来源: test_specs/usb3_prbs_test.md
        """
        print("\n" + "="*60)
        print("USB3.0 PRBS测试")
        print("="*60)
        
        try:
            # Step 1: 芯片初始化
            print("\n[1/5] 芯片初始化...")
            self.scripts.func_01_01_Chip_Power_Up()
            self.scripts.func_01_01_02_PLL_no_ssc_init()
            print("✓ 初始化完成")
            
            # Step 2: PRBS初始化
            print("\n[2/5] PRBS初始化...")
            self.custom.init_prbs(port_sel="UP")
            print("✓ PRBS初始化完成")
            
            # Step 3: 等待稳定
            print("\n[3/5] 等待稳定 (500ms)...")
            time.sleep(0.5)
            print("✓ 稳定完成")
            
            # Step 4: 检查PRBS错误
            print("\n[4/5] 检查PRBS错误...")
            result = self.scripts.break_min_check_prbs_error("UP", 5, 1)
            error_count, status = result[0], result[1]
            print(f"  错误计数: {error_count}")
            print(f"  状态: {status}")
            
            # Step 5: 断言结果
            print("\n[5/5] 结果断言...")
            assert status == 'pass', f"PRBS状态异常: {status}"
            assert error_count < 10, f"PRBS错误过多: {error_count}"
            print("✓ 所有断言通过")
            
            # 记录结果
            self.results.append({"test": "PRBS", "result": "PASS"})
            print("\n" + "="*60)
            print("✓ USB3.0 PRBS测试通过!")
            print("="*60)
            return True
            
        except AssertionError as e:
            self.results.append({"test": "PRBS", "result": f"FAIL: {e}"})
            print(f"\n✗ 测试失败: {e}")
            return False
        except Exception as e:
            self.results.append({"test": "PRBS", "result": f"ERROR: {e}"})
            print(f"\n✗ 运行时错误: {e}")
            return False
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "="*60)
        print("测试摘要")
        print("="*60)
        for r in self.results:
            status = "✓" if r["result"] == "PASS" else "✗"
            print(f"{status} {r['test']}: {r['result']}")


def main():
    """主函数"""
    print("="*60)
    print("GSU1K1 芯片测试套件")
    print("="*60)
    
    # 初始化硬件
    print("\n初始化硬件连接...")
    board = phy_func(i2c_port=0)
    print("✓ 硬件连接成功")
    
    # 创建测试套件
    test_suite = TestSuite(board)
    
    # 运行测试
    test_suite.test_prbs()
    
    # 打印摘要
    test_suite.print_summary()


if __name__ == "__main__":
    main()
```

## 5. 实施步骤

### Phase 1: 基础工具开发（1-2天）

1. **MD解析器**
   - 提取测试目标、步骤、断言
   - 识别已有函数和新函数声明

2. **函数扫描器**
   - 扫描GSU1K1_NTO_scripts.py获取函数列表
   - 建立函数签名数据库

3. **AutoClass转换器**
   - 解析AutoClass语法
   - 转换为writeBits/readReg调用
   - 维护地址映射表

### Phase 2: Demo生成器（1天）

1. **生成带TODO的函数框架**
2. **集成AutoClass语法提示**
3. **生成可用函数列表注释**

### Phase 3: 测试类生成器（1-2天）

1. **从MD生成测试流程**
2. **组装TestSuite类**
3. **生成主函数和错误处理**
4. **添加日志和报告功能**

### Phase 4: 集成与测试（1天）

1. **开发CLI工具**
   ```bash
   python -m chip_test_tool generate-demo test_specs/usb3_prbs_test.md
   python -m chip_test_tool generate-final test_specs/usb3_prbs_test.md
   ```

2. **编写示例测试规格**
   - usb3_prbs_test.md
   - usb2_rx_test.md
   - pll_lock_test.md

3. **端到端测试**

## 6. 使用示例

### 完整使用流程

```bash
# 1. 编写测试需求
cat > test_specs/my_test.md << 'EOF'
# 我的测试
## 步骤
1. 调用func_01_01_Chip_Power_Up()
2. 需要新函数my_config()
3. 断言结果
EOF

# 2. 生成Demo
python -m chip_test_tool generate-demo test_specs/my_test.md
# 输出: test_specs/generated/demo_my_test.py

# 3. 用户编辑（在VSCode中使用AutoClass补全）
code test_specs/generated/demo_my_test.py
# 保存为 test_specs/generated/custom_my_test.py

# 4. 生成最终代码
python -m chip_test_tool generate-final test_specs/my_test.md
# 输出: test_specs/generated/final_my_test.py

# 5. 执行测试
python test_specs/generated/final_my_test.py
```

## 7. 关键技术点

### 7.1 AutoClass到I2C的转换规则

| AutoClass语法 | 转换后的I2C代码 | 说明 |
|--------------|----------------|------|
| `AutoClass.PipeUp.REG.w(val)` | `board.writeBits(addr, reg, lsb, bits, val)` | 写寄存器 |
| `AutoClass.PipeUp.REG.r()` | `board.readReg(addr, reg)` | 读寄存器 |
| `AutoClass.CdrUp.REG.w(val)` | `board.writeBits(CdrUp, reg, lsb, bits, val)` | 不同PAGE |

### 7.2 地址映射表

```python
# 从GSU1K1_NTO_reg_def.py导入
PAGE_ADDR_MAP = {
    "PipeUp": 0x31,
    "PipeDp1": 0x32,
    "PipeDp2": 0x33,
    "PipeDp3": 0x34,
    "PipeDp4": 0x35,
    "CdrUp": 0x10,
    "CdrDp1": 0x11,
    # ... 更多PAGE
}

# 从XML解析
REG_ADDR_MAP = {
    "PipeUp": {
        "i2c_pipe_prbs_mode": {"addr": 0x63, "lsb": 1, "bits": 3},
        "i2c_tx_ser_rst_man": {"addr": 0x1E, "lsb": 2, "bits": 1},
        # ... 更多寄存器
    }
}
```

### 7.3 错误处理策略

```python
# 1. 函数不存在
if func_name not in available_funcs:
    raise ValueError(f"函数 {func_name} 不存在，请检查test_spec.md")

# 2. AutoClass语法错误
try:
    parse_autoclass(line)
except ParseError as e:
    print(f"AutoClass语法错误 @ {file}:{line_num}: {e}")
    print(f"  问题代码: {line}")

# 3. 寄存器不存在
if reg_name not in REG_ADDR_MAP[page]:
    raise ValueError(f"寄存器 {page}.{reg_name} 不存在")
```

## 8. 扩展性考虑

### 8.1 支持多芯片

```
test_specs/
├── GSU1K1/                    # 芯片型号目录
│   ├── usb3_prbs_test.md
│   └── usb2_test.md
├── GSU2K1/                    # 另一款芯片
│   ├── pcie_test.md
│   └── sata_test.md
```

### 8.2 支持多测试场景

```python
class TestSuite:
    def test_prbs_short(self):    # 快速测试
        ...
    
    def test_prbs_long(self):     # 长时间测试
        ...
    
    def test_prbs_margin(self):   # 裕量测试
        ...
```

### 8.3 支持测试数据记录

```python
def test_prbs(self):
    result = {
        "timestamp": time.time(),
        "test_name": "PRBS",
        "params": {"port": "UP", "duration": 5},
        "metrics": {"error_count": err_cnt, "ber": ber},
        "result": "PASS"
    }
    self.save_result(result)
```

## 9. 总结

本方案通过**自然语言需求 → AutoClass实现 → 自动化生成**的流程，实现了：

1. **Designer友好**：使用AutoClass享受IDE自动补全
2. **Agent高效**：自动化代码生成和转换
3. **架构清晰**：组合模式实现功能分层
4. **易于维护**：MD文档即需求，可追溯

预计开发周期：**5个工作日**

下一步：**开始Phase 1开发**
