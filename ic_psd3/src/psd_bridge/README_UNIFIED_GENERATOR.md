# AutoClass 统一生成器使用指南

## 概述

`unified_generator.py` 整合了 XML 解析和代码生成功能，提供三个核心功能：

1. **生成 AutoClass** - 创建 IDE 友好的嵌套类结构
2. **替换 AutoClass 调用** - 将占位符转换为实际 I2C 操作代码
3. **生成寄存器定义文件** - 提取 IIC memory 的 pagename 和地址定义

## 架构设计

### 核心思想

- **AutoClass 作为中间层**：利用 IDE 自动补全功能
- **方法体为 pass**：占位符，等待被替换为真实 I2C 代码
- **替换机制**：正则表达式匹配 `AutoClass.PAGE.reg.r()/w(val)` 并生成 I2C 代码

### 两阶段工作流

```
阶段 1: IDE 开发
┌─────────────────────────────────┐
│ 在 IDE 中编写配置脚本            │
│ 使用 AutoClass 进行自动补全      │
│ 例: AutoClass.AG.reg.r()        │
└────────────┬────────────────────┘
             │
阶段 2: 代码替换
┌─────────────────────────────────┐
│ 运行 replace_autoclass_calls()  │
│ 替换为真实 I2C 代码             │
│ 例: self.device.read_reg(0x06, 0x00)
└─────────────────────────────────┘
```

## 使用方法

### 方法 1: 命令行使用

```bash
# 仅生成 auto_class.py
python3 unified_generator.py path/to/your.xml

# 生成 auto_class.py 和 reg_define.py
python3 unified_generator.py path/to/your.xml --reg-define

# 生成并替换目标文件
python3 unified_generator.py path/to/your.xml --replace my_script.py

# 同时生成所有文件
python3 unified_generator.py path/to/your.xml --reg-define --replace my_script.py

# 自定义输出路径
python3 unified_generator.py path/to/your.xml \
  --reg-define library/my_defines.py \
  --replace my_script.py
```

### 方法 2: Python 代码使用

```python
from psd_bridge.unified_generator import AutoClassGenerator

# 1. 创建生成器
generator = AutoClassGenerator(
    xml_file_path='import/GSU1K1_NTO.xml',
    class_instance_name='self.device'  # 生成代码中的设备实例名
)

# 2. 生成 AutoClass 文件
auto_class_path = generator.generate_auto_class('library/auto_class.py')

# 3. 生成寄存器定义文件
reg_define_path = generator.generate_reg_define('library/reg_define.py')

# 4. 替换配置脚本中的 AutoClass 调用
generator.replace_autoclass_calls('my_config.py')

# 或者一步到位
auto_path, replace_path, reg_define_file = generator.generate_all(
    target_file='my_config.py',
    reg_define_path='library/reg_define.py'
)
```

## 生成的代码示例

### AutoClass 结构 (IDE 自动补全用)

```python
class AutoClass:
    class AG:
        """Page: AG, Address: 0x06"""
        class i2c_audio_format:
            """Register: i2c_audio_format, Address: 0x0600"""
            @staticmethod
            def r():
                """Read register value"""
                pass
            
            @staticmethod
            def w(val):
                """Write value to register"""
                pass
```

### 替换后的代码 (实际 I2C 操作)

```python
# 读取操作
rb_i2c_audio_format = (self.device.read_reg(0x06, 0x00) & 0xE0) >> 5

# 写入操作
# w AG:i2c_audio_format <- 0x3
self.device.write_bits(0x06, 0x00, 5, 3, 3)
```

### 生成的 reg_define.py (寄存器定义)

```python
# 从 XML 自动提取的 I2C 页面地址
AG = 0x06
CdrUp = 0x10
CdrDp1 = 0x11
CdrDp2 = 0x12
# ... 更多页面定义

# 页面名称到地址的映射
PAGE_MAP = {
    "AG": 0x06,
    "CdrUp": 0x10,
    "CdrDp1": 0x11,
    # ...
}

# 反向映射：地址到页面名称
ADDR_MAP = {
    0x06: "AG",
    0x10: "CdrUp",
    0x11: "CdrDp1",
    # ...
}
```

使用示例：

```python
from library.reg_define import *

# 直接使用常量
device.read_reg(AG, 0x00)        # 读取 AG 页面地址 0x00

# 使用映射进行动态查询
page_addr = PAGE_MAP["CdrUp"]
device.write_bits(page_addr, 0x01, 0, 8, 0xFF)

# 反向查询
page_name = ADDR_MAP[0x10]
print(f"Page address 0x10 is {page_name}")
```

## 配置脚本示例

```python
from library.auto_class import AutoClass

# 在 IDE 中编写，利用自动补全
def config_chip():
    # 读取寄存器
    value = AutoClass.AG.i2c_audio_format.r()
    print(f"Audio format: {value}")
    
    # 写入寄存器
    AutoClass.AG.i2c_audio_format.w(0x3)
    
    # 多个操作
    AutoClass.RX1.clock_setting.w(0xFF)
    AutoClass.TX1.gain_control.w(0x80)

if __name__ == "__main__":
    config_chip()
```

运行替换后，变成：

```python
def config_chip():
    # 读取寄存器
    rb_i2c_audio_format = (self.device.read_reg(0x06, 0x00) & 0xE0) >> 5
    print(f"Audio format: {rb_i2c_audio_format}")
    
    # 写入寄存器
    # w AG:i2c_audio_format <- 0x3
    self.device.write_bits(0x06, 0x00, 5, 3, 3)
    
    # 多个操作
    # w RX1:clock_setting <- 0xFF
    self.device.write_bits(0x11, 0x00, 0, 8, 255)
    # w TX1:gain_control <- 0x80
    self.device.write_bits(0x12, 0x00, 0, 8, 128)
```

## 关键特性

### 1. IDE 自动补全

- **嵌套类结构**：`AutoClass.PAGE.register.method()`
- **类型提示**：每个方法都有文档字符串
- **代码提示**：寄存器地址和描述显示在 docstring 中

### 2. 寄存器定义常量

- **直接导入使用**：`from library.reg_define import *`
- **多种访问方式**：直接常量、字典映射、反向查询
- **自动生成**：从 XML 中提取所有 IIC memory 的页面地址

### 3. 自动地址转换

- **16 位地址拆分**：`0x0600` → `addr1=0x06, addr2=0x00`
- **掩码和位移**：自动计算 LSB 位置和位数
- **多字节寄存器**：支持跨字节的寄存器操作

### 4. 错误处理

- **未找到寄存器**：替换时生成 `# ERROR: PAGE.reg not found` 注释
- **备份原文件**：替换前自动备份为 `.bak`
- **详细日志**：显示所有读写操作数量

## 文件结构

```
ic_psd3/
├── import/
│   ├── GSU1K1_NTO.xml          # 源 XML 寄存器定义
│   └── gsu1001_2025_nto_scripts.txt
├── library/
│   ├── auto_class.py            # 生成的 AutoClass (IDE 自动补全)
│   └── reg_define.py            # 生成的寄存器定义 (页面地址常量)
└── src/psd_bridge/
    └── unified_generator.py     # 统一生成器 (核心)
```

## 工作原理

### 步骤 1: XML 解析
- 读取寄存器 XML 文件
- 提取页面、寄存器、地址、掩码、位移信息
- 按页面组织成两级哈希表

### 步骤 2: 生成 AutoClass
- 为每个页面创建子类
- 为每个寄存器创建嵌套类
- 生成 `r()` 和 `w(val)` 方法（方法体为 pass）

### 步骤 3: 生成寄存器定义
- 提取所有 interface 节点中的页面名称和地址
- 生成 Python 常量定义（`PAGE_NAME = 0xADDRESS`）
- 创建双向映射字典：PAGE_MAP 和 ADDR_MAP

### 步骤 4: 替换调用
- 正则表达式匹配 `AutoClass.PAGE.reg.r/w(...)`
- 查询寄存器信息获取地址、掩码、位移
- 生成实际的 `read_reg()` 和 `write_bits()` 代码

## 数据结构

### 内部格式：寄存器信息字典

```python
{
    "register_name": "i2c_audio_format",
    "byte_address": "0x0600",
    "byte_mask": "0xE0",
    "byte_shift": "5",
    "effective_bits": 3,
    ...
}
```

## 统计信息 (GSU1K1_NTO.xml)

- **总页数**：38 个
- **寄存器数**：7,136 个
- **生成的 AutoClass 文件大小**：85+ KB
- **生成的 reg_define 文件大小**：8+ KB
- **支持的 I2C 操作**：read_reg(), write_bits()
- **页面地址范围**：0x02 - 0x4B (十进制：2 - 75)

## 性能

- **XML 解析**：< 1 秒
- **AutoClass 代码生成**：< 2 秒
- **reg_define 代码生成**：< 0.5 秒
- **替换操作**：取决于脚本大小（典型情况 < 1 秒）
- **总耗时**：< 3 秒（包含所有操作）

## 注意事项

1. **寄存器名称转换**：特殊字符（`:`, `/` 等）会被转换为 `_`
2. **类名有效性**：以数字开头的类名会添加 `reg_` 前缀
3. **去重**：同一页面下重复的寄存器名称只生成一次
4. **备份机制**：替换时自动创建 `.bak` 备份，可用 `--no-backup` 禁用

## 集成 DeviceManager

生成的代码兼容 `hw_bridge.DeviceManager` 架构：

```python
from hw_bridge import DeviceManager
from library.auto_class import AutoClass

# 创建设备管理器
dm = DeviceManager()
device = dm.get_device("chip", driver_type="mock")

# 替换后的代码自动使用 device 实例
rb_value = device.read_reg(0x06, 0x00)
device.write_bits(0x06, 0x00, 5, 3, 3)
```

## 许可

与项目保持一致。

---

**文档版本**：2.0  
**最后更新**：2026-02-12

## 更新历史

### v2.0 (2026-02-12)
- 新增功能：`generate_reg_define()` - 生成 I2C 页面地址定义文件
- 新增命令行选项：`--reg-define` - 支持生成寄存器定义
- 增强 `generate_all()` 方法以支持 reg_define 输出路径
- 添加 PAGE_MAP 和 ADDR_MAP 双向映射
- 完善文档和使用示例

### v1.0 (初始版本)
- AutoClass 代码生成和 IDE 补全
- AutoClass 调用替换为实际 I2C 代码
