"""
使用示例：AVESChipConfig 类

展示如何使用生成的 AVESChipConfig 类来配置芯片
使用 DeviceManager 统一管理设备
"""

# ================== 示例1: 单设备配置 ==================

from hw_bridge import DeviceManager
from library.aves_class import AVESChipConfig

# 创建 DeviceManager 并注册设备
dm = DeviceManager(auto_open=True)
dm.register("chip", "mock", chip_addr=0x58)  # 使用 mock 驱动测试

# 创建配置实例
config = AVESChipConfig(device_manager=dm, device_name="chip")

# 调用 AVES 函数 - 内部使用 device.write_reg(addr1, addr2, value)
# 例如: B0 0902 13 -> device.write_reg(0x09, 0x02, 0x13)
config.func_01_01_Chip_Power_Up()
config.func_01_01_02_PLL_no_ssc_init()

print("单设备配置完成！")


# ================== 示例2: 双设备配置 (TX/RX) ==================

# 创建 DeviceManager
dm2 = DeviceManager(auto_open=True)

# 注册 TX 和 RX 设备 (同一套脚本用于两个设备)
dm2.register("tx", "ftdi", i2c_port=0, chip_addr=0x58)
dm2.register("rx", "ftdi", i2c_port=1, chip_addr=0x58)

# 为每个设备创建配置实例
tx_config = AVESChipConfig(device_manager=dm2, device_name="tx")
rx_config = AVESChipConfig(device_manager=dm2, device_name="rx")

# 分别配置 TX 和 RX
tx_config.func_01_01_Chip_Power_Up()
rx_config.func_01_01_Chip_Power_Up()

print("双设备配置完成！")


# ================== 示例3: 动态切换设备 ==================

# 创建配置实例但不指定 DeviceManager
config3 = AVESChipConfig()

# 稍后设置 DeviceManager
config3.set_device_manager(dm2, device_name="tx")

# 现在可以使用了
config3.func_01_01_02_PLL_no_ssc_init()

print("动态切换设备完成！")
