# AVES Converter - 使用说明

## 功能简介

AVES Converter 将 AVES 脚本转换为 Python 类，使用 `DeviceManager` 统一管理设备，支持多设备配置（如 TX/RX 双板）。

## 生成文件

转换完成后会在 `ic_psd3/library/` 目录下生成：

1. **aves_class.py** - AVES 配置类（132个函数）
2. **GSU1K1_NTO_reg_def.py** - 寄存器定义文件

## 使用方法

### 基本转换

```bash
cd ic_psd3
python -m src.psd_bridge.aves_converter
```

### 自定义参数

```bash
python -m src.psd_bridge.aves_converter \
    import/gsu1001_2025_nto_scripts.txt \
    library/ \
    GSU1K1_NTO
```

## 寄存器写入格式

AVES 脚本格式：`B0 0902 13` (设备地址 子地址 数据)

转换后：`device.write_reg(0x09, 0x02, 0x13)`

说明：
- `B0` 是 I2C 设备地址（创建设备时已设置，不在写入命令中）
- `0902` 是 16-bit 子地址，拆分为 `0x09` (high byte) 和 `0x02` (low byte)
- `13` 是数据值

## 使用生成的类

### 单设备配置

```python
import sys
sys.path.insert(0, 'src/hw_bridge/src')

from hw_bridge import DeviceManager
from library.aves_class import AVESChipConfig

# 创建 DeviceManager
dm = DeviceManager(auto_open=True)
dm.register('chip', 'mock', chip_addr=0x58)

# 创建配置实例
config = AVESChipConfig(device_manager=dm, device_name='chip')

# 调用 AVES 函数
config.func_01_01_Chip_Power_Up()
config.func_01_01_02_PLL_no_ssc_init()
```

### 双设备配置 (TX/RX)

```python
from hw_bridge import DeviceManager
from library.aves_class import AVESChipConfig

# 创建 DeviceManager
dm = DeviceManager(auto_open=True)

# 注册 TX 和 RX 设备
dm.register('tx', 'ftdi', i2c_port=0, chip_addr=0x58)
dm.register('rx', 'ftdi', i2c_port=1, chip_addr=0x58)

# 为每个设备创建配置实例
tx_config = AVESChipConfig(device_manager=dm, device_name='tx')
rx_config = AVESChipConfig(device_manager=dm, device_name='rx')

# 分别配置
tx_config.func_01_01_Chip_Power_Up()
rx_config.func_01_01_Chip_Power_Up()
```

## 特性

- ✓ 自动解析 AVES 脚本中的 132 个函数
- ✓ 正确处理 `include` 语句（91 个函数调用）
- ✓ 正确处理寄存器地址格式（16-bit 地址拆分为 high/low byte）
- ✓ 支持 DeviceManager 统一管理设备
- ✓ 支持多设备配置（TX/RX 双板）
- ✓ 保留原始注释
- ✓ 类型注解支持

## 转换统计

- **源文件**: `gsu1001_2025_nto_scripts.txt`
- **生成函数**: 132 个
- **Include 调用**: 91 个
- **I2C 寄存器操作**: 3849 行

## 与原始实现对比

| 项目 | 原始 (get_aves.py) | 新实现 (aves_converter.py) |
|------|-------------------|---------------------------|
| 调用方式 | `self.writeReg(0x09, 0x02, 0x13)` | `device.write_reg(0x09, 0x02, 0x13)` |
| 设备管理 | 各自创建驱动实例 | DeviceManager 统一管理 |
| 多设备支持 | 需要手动管理 | 通过 device_name 切换 |
| 地址格式 | addr1=high, addr2=low | addr1=high, addr2=low (相同) |

## 注意事项

1. 生成的类依赖 `hw_bridge` 包，请确保已安装：
   ```bash
   cd ic_psd3/src/hw_bridge && pip install -e .
   ```

2. 使用 `mock` 驱动可以进行离线测试

3. 实际硬件测试请使用 `ftdi` 或 `pi` 驱动

4. 寄存器地址已正确拆分：
   - AVES: `B0 0902 13` → Python: `write_reg(0x09, 0x02, 0x13)`
   - B0 是设备地址，09 是 high byte，02 是 low byte，13 是数据
