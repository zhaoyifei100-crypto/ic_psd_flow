#!/usr/bin/env python3
"""
hw_bridge 使用示例

展示如何使用 hw_bridge 库进行 I2C 通信
"""

from hw_bridge import create_device, load_config


def example_basic_usage():
    """基础使用示例"""
    print("=" * 50)
    print("示例 1: 基础使用")
    print("=" * 50)

    # 创建 Mock 驱动 (无需硬件)
    device = create_device("mock", chip_addr=0x58)

    # 使用上下文管理器自动管理连接
    with device:
        # 写寄存器 (addr1=页地址, addr2=偏移地址)
        device.write_reg(0x26, 0x00, 0xFF)

        # 读寄存器
        value = device.read_reg(0x26, 0x00)
        print(f"读取寄存器 0x2600: 0x{value:02X}")

        # 位操作 (写入第2-5位)
        device.write_bits(0x26, 0x01, lsb=2, bits=4, value=0x0A)
        bits_value = device.read_bits(0x26, 0x01, lsb=2, bits=4)
        print(f"读取位 [5:2]: 0x{bits_value:02X}")

        # 批量读取
        values = device.read_regs(0x26, 0x00, num=4)
        print(f"批量读取 4 个寄存器: {[hex(v) for v in values]}")

    print()


def example_with_config():
    """使用配置文件"""
    print("=" * 50)
    print("示例 2: 使用配置文件")
    print("=" * 50)

    # 加载配置文件
    try:
        config = load_config("config_example.yaml")
        print(f"从配置文件加载:")
        print(f"  驱动类型: {config.driver_type}")
        print(f"  芯片地址: 0x{config.chip_addr:02X}")
        print(f"  I2C 端口: {config.i2c_port}")

        # 使用配置创建设备
        options = config.get_driver_options()
        device = create_device(config.driver_type, **options)
        print(f"  成功创建设备!")

    except FileNotFoundError:
        print("配置文件不存在,使用默认配置")
        device = create_device("mock")

    print()


def example_mock_features():
    """Mock 驱动特性演示"""
    print("=" * 50)
    print("示例 3: Mock 驱动特性")
    print("=" * 50)

    device = create_device("mock", chip_addr=0x58, verbose=False)
    device.open()

    # 预设寄存器值
    device.set_register(0x26, 0x10, 0xAB)
    device.set_register(0x26, 0x11, 0xCD)

    # 读取预设值
    print("预设寄存器值:")
    print(f"  0x2610 = 0x{device.read_reg(0x26, 0x10):02X}")
    print(f"  0x2611 = 0x{device.read_reg(0x26, 0x11):02X}")

    # 显示统计
    stats = device.get_statistics()
    print(f"\n操作统计:")
    print(f"  写入次数: {stats['writes']}")
    print(f"  读取次数: {stats['reads']}")
    print(f"  总操作数: {stats['total_operations']}")
    print(f"  已定义寄存器数: {stats['registers_defined']}")

    # 转储所有寄存器
    print(f"\n寄存器转储:")
    device.dump_registers()

    device.close()
    print()


def example_platform_auto_detect():
    """平台自动检测"""
    print("=" * 50)
    print("示例 4: 平台自动检测")
    print("=" * 50)

    from hw_bridge.factory import auto_detect_driver

    driver_type = auto_detect_driver()
    print(f"检测到平台: {driver_type}")

    if driver_type:
        print(f"推荐驱动: {driver_type}")
        # device = create_device(driver_type)
    else:
        print("未知平台,使用 Mock 驱动")
        # device = create_device('mock')

    print()


if __name__ == "__main__":
    print("\nhw_bridge 库使用示例\n")

    example_basic_usage()
    example_with_config()
    example_mock_features()
    example_platform_auto_detect()

    print("=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)
