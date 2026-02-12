#!/usr/bin/env python3
"""
DeviceManager 使用示例

展示如何使用 DeviceManager 管理多个硬件设备
"""

from hw_bridge import DeviceManager, get_manager


def example_basic_usage():
    """基础使用示例 - 立即打开模式"""
    print("=" * 60)
    print("示例 1: 立即打开模式（推荐）")
    print("=" * 60)

    # 创建 manager，auto_open=True（默认）
    # 设备会在 register 时立即打开
    manager = DeviceManager(auto_open=True)

    # 注册两块板子
    manager.register("tx_board", "mock", chip_addr=0x58)
    manager.register("rx_board", "mock", chip_addr=0x59)

    # 直接随时随地使用，不需要 with，不需要传递 device
    print("\n1. 写入寄存器:")
    manager["tx_board"].write_reg(0x26, 0x00, 0xAB)
    manager["rx_board"].write_reg(0x26, 0x00, 0xCD)

    print("\n2. 读取寄存器:")
    tx_val = manager["tx_board"].read_reg(0x26, 0x00)
    rx_val = manager["rx_board"].read_reg(0x26, 0x00)
    print(f"   TX: 0x{tx_val:02X}, RX: 0x{rx_val:02X}")

    print("\n3. 位操作:")
    manager["tx_board"].write_bits(0x26, 0x01, lsb=2, bits=4, value=0x0A)
    bits = manager["tx_board"].read_bits(0x26, 0x01, lsb=2, bits=4)
    print(f"   写入 0x0A 到 [5:2]，读取到: 0x{bits:02X}")

    # 清理
    manager.close_all()
    print("\n✓ 示例 1 完成\n")


def example_lazy_mode():
    """延迟打开模式"""
    print("=" * 60)
    print("示例 2: 延迟打开模式")
    print("=" * 60)

    # auto_open=False，设备在第一次访问时才打开
    manager = DeviceManager(auto_open=False)

    print("\n1. 注册设备（此时还未打开）:")
    manager.register("board_a", "mock", chip_addr=0x58)
    print(f"   board_a 是否已打开: {manager.is_open('board_a')}")

    print("\n2. 第一次访问时自动打开:")
    manager["board_a"].write_reg(0x26, 0x00, 0xFF)  # 这里才会打开
    print(f"   board_a 是否已打开: {manager.is_open('board_a')}")

    manager.close_all()
    print("\n✓ 示例 2 完成\n")


def example_global_manager():
    """全局管理器"""
    print("=" * 60)
    print("示例 3: 全局管理器（跨模块访问）")
    print("=" * 60)

    print("\n1. 在模块 A 中注册设备:")
    # 使用 get_manager() 获取全局实例
    get_manager().register("global_board", "mock", chip_addr=0x58)

    print("\n2. 在模块 B 中访问同一设备:")
    # 任何地方都能访问同一个 manager
    val = get_manager()["global_board"].read_reg(0x26, 0x00)
    print(f"   读取值: 0x{val:02X}")

    print("\n3. 列出所有全局设备:")
    devices = get_manager().list_devices()
    print(f"   设备列表: {devices}")

    # 重置全局管理器
    DeviceManager.reset_global()
    print("\n✓ 示例 3 完成\n")


def example_device_discovery():
    """设备发现和检查"""
    print("=" * 60)
    print("示例 4: 设备发现和状态检查")
    print("=" * 60)

    manager = DeviceManager()
    manager.register("dev1", "mock", chip_addr=0x58)
    manager.register("dev2", "mock", chip_addr=0x59)

    print("\n1. 检查设备是否存在:")
    if "dev1" in manager:
        print("   dev1 已注册")

    print("\n2. 获取设备数量:")
    print(f"   共 {len(manager)} 个设备")

    print("\n3. 列出所有设备:")
    print(f"   {manager.list_devices()}")

    print("\n4. 安全获取（带默认值）:")
    dev = manager.get("dev1")
    if dev:
        print(f"   获取到 dev1: {dev}")

    not_found = manager.get("non_existent", default=None)
    print(f"   不存在的设备: {not_found}")

    manager.close_all()
    print("\n✓ 示例 4 完成\n")


def example_error_handling():
    """错误处理"""
    print("=" * 60)
    print("示例 5: 错误处理")
    print("=" * 60)

    manager = DeviceManager()

    print("\n1. 访问不存在的设备:")
    try:
        manager["non_existent"].write_reg(0x26, 0x00, 0xFF)
    except KeyError as e:
        print(f"   捕获错误: {e}")

    print("\n2. 重复注册设备:")
    manager.register("test_dev", "mock", chip_addr=0x58)
    try:
        manager.register("test_dev", "mock", chip_addr=0x58)
    except ValueError as e:
        print(f"   捕获错误: {e}")

    manager.close_all()
    print("\n✓ 示例 5 完成\n")


def example_mixed_modes():
    """混合模式（实际应用场景）"""
    print("=" * 60)
    print("示例 6: 实际应用场景")
    print("=" * 60)

    manager = DeviceManager(auto_open=True)

    print("\n1. 初始化阶段 - 注册所有设备:")
    # TX 板 - FTDI 端口 0
    manager.register("tx", "mock", chip_addr=0x58)
    # RX 板 - FTDI 端口 1
    manager.register("rx", "mock", chip_addr=0x59)
    # 调试板 - Mock 用于测试
    manager.register("debug", "mock", chip_addr=0x5A)

    print(f"   已注册: {manager.list_devices()}")

    print("\n2. 测试阶段 - 随时随地使用:")
    print("   TX 初始化...")
    manager["tx"].write_reg(0x26, 0x00, 0x01)
    manager["tx"].write_reg(0x26, 0x01, 0x02)

    print("   RX 初始化...")
    manager["rx"].write_reg(0x26, 0x00, 0x11)
    manager["rx"].write_reg(0x26, 0x01, 0x12)

    print("   调试信息...")
    manager["debug"].write_reg(0x26, 0x00, 0xFF)

    print("\n3. 验证阶段:")
    tx_val = manager["tx"].read_reg(0x26, 0x00)
    rx_val = manager["rx"].read_reg(0x26, 0x00)
    print(f"   TX 状态: 0x{tx_val:02X}, RX 状态: 0x{rx_val:02X}")

    print("\n4. 清理阶段:")
    manager.close_all()
    print("   所有设备已关闭")

    print("\n✓ 示例 6 完成\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("hw_bridge DeviceManager 使用示例")
    print("=" * 60 + "\n")

    example_basic_usage()
    example_lazy_mode()
    example_global_manager()
    example_device_discovery()
    example_error_handling()
    example_mixed_modes()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
