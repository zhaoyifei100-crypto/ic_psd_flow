# PSD3 架构设计 TODO

## 项目定位

PSD3 = Qualification Phase（验证阶段）- 硬件驱动和测试自动化

**设计原则**：
- 每颗芯片独立维护（git clone后自行扩展）
- 简化设计，避免过度工程化
- HTML报告优先
- 文件系统存储（无数据库）

---

## 1. 目标架构 (Target Architecture)

```
ic_psd3/
├── infrastructure/              # 基础设施层
│   ├── drivers/                 # 硬件驱动
│   │   ├── drv_base.py          # [TODO] I2C驱动抽象基类
│   │   ├── drv_ftdi.py          # Windows FTDI驱动（现有）
│   │   └── drv_pi.py            # Linux RPi驱动（现有）
│   ├── parser/                  # 文件解析
│   │   ├── xml_parser.py        # XML寄存器解析（现有）
│   │   └── spec_parser.py       # [AGENT] opencode
│   └── binding/                 # [TODO] 寄存器绑定
│       ├── auto_class_gen.py    # AutoClass生成器
│       └── reg_converter.py     # AutoClass→I2C转换器
│
├── framework/                   # 测试框架层
│   ├── core/                    # 核心引擎
│   │   ├── test_base.py         # [TODO] TestSuite基类
│   │   ├── test_runner.py       # [TODO] 测试执行器
│   │   └── test_context.py      # [TODO] 测试上下文管理
│   ├── reporting/               # 报告生成
│   │   ├── report_gen.py        # [TODO] 报告生成器
│   │   └── html_reporter.py     # [TODO] HTML报告
│   └── utils/                   # 工具函数
│       └── data_logger.py       # [TODO] 数据记录器
│
├── library/                     # 测试库层（Common Functions）
│   └── common/                  # [TODO] 通用函数
│       ├── __init__.py
│       ├── chip_base.py         # 芯片基础操作
│       ├── power_manage.py      # 电源管理
│       └── clock_config.py      # 时钟配置
│
└── tests/                       # 测试用例层
    ├── specs/                   # 测试规格目录
    │   ├── reliability/         # [TODO] 可靠性测试规格
    │   │   ├── htb_test.md
    │   │   ├── htb_life_test.md
    │   │   ├── tc_test.md
    │   │   ├── uhs_test.md
    │   │   └── esd_test.md
    │   └── functional/          # [TODO] 功能测试规格
    │
    ├── generated/               # [TODO] 生成的测试代码
    │   └── reliability/
    │       └── htb_test/
    │           ├── demo_htb_test.py
    │           ├── custom_htb_test.py
    │           └── final_htb_test.py
    │
    └── results/                 # [TODO] 测试结果（闭环）
        └── reliability/
            └── htb_test/
                ├── 2024-01-15_001/
                │   ├── config.json
                │   ├── data.json
                │   ├── report.html
                │   └── aves_log.txt
                └── summary.csv
```

---

## 2. 核心组件设计

### 2.1 Test Flow Pipeline

基于README.md定义的5步工作流：

```
test_spec.md (自然语言规格)
    ↓ [opencode agent]
    ↓ [区分AVES func/高级func]
demo_xxx_test.py (高级func rsv for designer)
    ↓ [User Edit: AutoClass语法]
custom_xxx_test.py (用户实现)
    ↓ [Final Generator: AutoClass→I2C转换]
final_xxx_test.py (可执行代码)
    ↓ [Test Runner]
Execution Result
    ↓ [HTML Reporter]
report.html + data.json + aves_log.txt
```

### 2.2 关键类设计

#### infrastructure/drivers/drv_base.py
```python
class I2CDriverBase(ABC):
    """跨平台I2C驱动抽象基类"""
    @abstractmethod
    def read_reg(self, addr1, addr2): ...
    @abstractmethod
    def write_reg(self, addr1, addr2, value): ...
    @abstractmethod
    def write_bits(self, addr1, addr2, lsb, bits, value): ...
```

#### framework/core/test_base.py
```python
class TestSuiteBase(ABC):
    """测试套件基类"""
    def __init__(self, board, chip_id: str):
        self.board = board
        self.chip_id = chip_id
        self.scripts = None      # 已有函数库(GSU1K1_scripts)
        self.custom = None       # 用户自定义函数
        self.results = []
        
    @abstractmethod
    def setup(self): ...
    @abstractmethod
    def run(self): ...
    @abstractmethod
    def teardown(self): ...
```

#### infrastructure/binding/reg_converter.py
```python
class AutoClassConverter:
    """AutoClass语法转换器"""
    def convert_line(self, line: str) -> str:
        # AutoClass.PipeUp.REG.w(val) 
        # → board.writeBits(addr, reg, lsb, bits, val)
        ...
```

---

## 3. 可靠性测试组织 (Reliability Tests)

### 3.1 测试类别

按测试类型分目录管理：

```
tests/specs/reliability/
├── htb_test.md              # High Temperature Bias (高温偏压)
├── htb_life_test.md         # HTB寿命测试
├── tc_test.md               # Temperature Cycle (温度循环)
├── uhs_test.md              # Unbiased Humidity Storage (无偏置湿储)
├── thb_test.md              # Temperature Humidity Bias (温湿偏压)
├── esd_test.md              # ESD测试
├── latch_up_test.md         # 闩锁测试
└── data_retention_test.md   # 数据保持测试
```

### 3.2 闭环数据流

每个测试目录包含完整数据链：

```
tests/results/reliability/htb_test/
├── 2024-01-15_batch001/          # 批次1数据
│   ├── config.json               # 测试参数配置
│   ├── data.json                 # 结构化测试数据
│   ├── report.html               # HTML报告（主要输出）
│   ├── aves_log.txt              # I2C命令日志
│   └── intermediate/             # 中间读数（HTB特有）
│       ├── 168h.json
│       ├── 500h.json
│       └── 1000h.json
├── 2024-01-15_batch002/          # 批次2数据
├── summary.csv                   # 跨批次汇总表
└── trend_chart.html              # 趋势图表
```

---

## 4. Test Spec Markdown格式

标准模板：

```markdown
# HTB Test (High Temperature Bias)

## 测试目标
验证芯片在高温125°C下的长期稳定性

## 测试参数
- Temperature: 125°C
- Duration: 1000 hours
- Sample Size: 77
- Vcc: Max rated voltage

## 前置条件
- 调用已有函数: `func_01_01_Chip_Power_Up()`
- 调用已有函数: `func_01_01_02_PLL_no_ssc_init()`

## 测试步骤
1. **初始测试** (0h)
   - 调用已有函数: `run_parametric_test()`
   
2. **HTB应力** (需要新函数 `monitor_htb_conditions`)
   - 设置温度125°C
   - 施加最大电压
   - 监控芯片状态

3. **中间读数** (168h, 500h, 1000h)
   - 调用已有函数: `run_parametric_test()`
   - 断言: 参数漂移 < 10%

## 断言条件
- 0h→1000h参数漂移 < 10%
- 无功能失效

## 清理
- 恢复常温
- 芯片下电
```

---

## 5. Common Functions管理

### 5.1 目录结构

```
library/
└── common/                      # 通用函数库
    ├── __init__.py
    ├── chip_aves.py             # 芯片基础操作, build from aves scripts
    └── chip_phy.py              # PHY高级函数，可读可写，例如PRBScheck
```

TODO 增加仪器程控，使用python3的pyvisa
		最好使用以太网协议，不要用GPIB，以太网配置一个ip地址就可以远程控制

### 5.2 使用方式

```python
# final_test.py中引用
from library.common import ChipBase, PowerManager

class TestSuite:
    def __init__(self, board):
        self.common = ChipBase(board)
        self.power = PowerManager(board)
        # 芯片特定函数（暂不迁移）
        # self.scripts = GSU1K1_scripts(board)
```

---

## 6. 执行模式

### 6.1 支持模式

1. **单芯片顺序执行**（默认）
   ```bash
   python tests/generated/reliability/htb_test/final_htb_test.py --chip-id GSU1K1-001
   ```

2. **双芯片同时收发**（扩展）
   ```bash
   python tests/runner.py --config dual_chip_config.yaml
   ```

### 6.2 长时间测试处理

对于1000h HTB测试：
- 主程序运行在前台，定时采样
- 或使用后台模式：`nohup python test.py &`
- 采样间隔可配置（如每24h自动读数）

---

## 7. 开发计划

### Phase 1: 基础设施 (1周)
- [ ] 创建目录结构
- [ ] 实现drv_base.py抽象基类
- [ ] 迁移drv_ftdi.py/drv_pi.py继承基类
- [ ] 实现spec_parser.py (Markdown解析)

### Phase 2: 核心框架 (1周)
- [ ] 实现test_base.py
- [ ] 实现test_runner.py
- [ ] 实现AutoClassConverter
- [ ] 实现Demo/Final代码生成器

### Phase 3: 报告系统 (3天)
- [ ] 实现html_reporter.py
- [ ] 设计HTML报告模板
- [ ] 实现data_logger.py

### Phase 4: 示例实现 (3天)
- [ ] 创建HTB test spec示例
- [ ] 完整走通5步工作流
- [ ] 生成示例报告

### Phase 5: 文档 (2天)
- [ ] 编写用户使用手册
- [ ] 编写开发扩展指南
- [ ] 更新README.md

---

## 8. 非目标 (Out of Scope)

为了保持简洁，以下功能**暂不实现**：

- ❌ 多芯片支持（每芯片独立仓库）
- ❌ 数据库（SQLite/PostgreSQL）
- ❌ Excel/PDF报告（仅HTML）
- ❌ Web Dashboard（仅本地文件）
- ❌ CI/CD集成（仅本地执行）
- ❌ GSU1K1_scripts.py迁移（保持现有位置）

---

## 9. 待决策事项

- [ ] **Hardware抽象层**: 是否需要统一的`phy_func`类作为所有驱动的统一接口？
  - Option A: 保持FTDI/PI独立（简单）
  - Option B: 统一phy_func接口（兼容性好）
  - 决策影响: drv_base.py的设计

---

## 10. 参考文档

- README.md: 完整的Test Flow设计（625行）
- auto_py_script.py: AutoClass生成和转换逻辑
- xml_parser.py: 寄存器解析参考

