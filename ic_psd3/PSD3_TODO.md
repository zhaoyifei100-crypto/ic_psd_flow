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
├── src/              # 基础设施层
│   ├── hw_bridge/                 # 硬件驱动
│   ├── lab_instruments/        # lab instruments
│   └── psd_bridge/                 # PSD2toPSD3 bridge
│       ├── aves_converter.py    # AVESClass自动生成器
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
├── import      #PSD2 import files
│    ├── GSU1K1_NTO.xml      # chip xml file
    ├── gsu1001_2025_nto_scripts.txt        #AVES scripts write only


├── library/                     # 测试库层（Common Functions）
│       ├── aves_class.py       # auto gen from AVES scripts
│       ├── usb_common_class.py       # usb公用的common class
                                        # 这个文件应该要统一管理，TODO
│       └── psd3_class.py     # 本项目特有的 PSD3 chip function class

│
└── tests/                       # 测试用例层
    ├── specs/                   # 测试规格目录
    │   ├── phy/         # [TODO] 可靠性测试规格
    │   │   ├── usb3_prbs.md
    │   │   ├── ...
    │   └── reliability/          # [TODO] 可靠测试规格
    │   └── functional/          # [TODO] 功能测试规格
    │
    ├── generated/               # [TODO] 生成的测试代码
    │   └── phy/
    │       └── usb3_prbs/
    │           ├── custom_htb_test.py      #AGI输出给用户修改
    │           └── final_htb_test.py       #AGI自己整合成最终版本
    │
    └── results/                 # [TODO] 测试结果（闭环）
        └── phy/
            └── usb3_prbs/
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
customer_xxx_test.py (需要designer编辑)
    ↓ [Final Generator: AutoClass→I2C转换]
final_xxx_test.py (可执行代码)
    ↓ [Test Runner]
Execution Result
    ↓ [HTML Reporter]
report.html + data.json + aves_log.txt
```

### 2.2 关键类设计

...

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
