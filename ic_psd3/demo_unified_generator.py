#!/usr/bin/env python3
"""
AutoClass Unified Generator - 完整示例

演示如何使用 unified_generator.py 进行 IDE 友好的寄存器配置和代码生成。
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from psd_bridge.unified_generator import AutoClassGenerator


def main():
    """主函数：演示完整工作流"""

    print("=" * 70)
    print("AutoClass Unified Generator - 完整演示")
    print("=" * 70)

    # ========== 步骤 1: 创建生成器 ==========
    print("\n[步骤 1] 初始化生成器...")
    xml_file = "import/GSU1K1_NTO.xml"

    if not os.path.exists(xml_file):
        print(f"✗ 错误: XML 文件不存在: {xml_file}")
        return 1

    generator = AutoClassGenerator(
        xml_file_path=xml_file, class_instance_name="self.device"
    )
    print("✓ 生成器初始化成功")

    # ========== 步骤 2: 生成 AutoClass ==========
    print("\n[步骤 2] 生成 AutoClass 文件...")
    auto_class_path = generator.generate_auto_class("library/auto_class.py")
    print(f"✓ AutoClass 生成: {auto_class_path}")

    # 显示统计信息
    with open(auto_class_path) as f:
        auto_class_content = f.read()
        lines = len(auto_class_content.splitlines())
        size_kb = len(auto_class_content) / 1024

    print(f"  - 文件大小: {size_kb:.1f} KB")
    print(f"  - 代码行数: {lines} 行")

    # ========== 步骤 3: 创建示例配置脚本 ==========
    print("\n[步骤 3] 创建示例配置脚本...")
    example_script = "examples/gsu1k1_config_example.py"
    os.makedirs("examples", exist_ok=True)

    with open(example_script, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
"""
GSU1K1 芯片配置脚本示例

这是一个使用 AutoClass 进行寄存器配置的示例。
在 IDE 中编写时，可以利用自动补全功能。
"""

from library.auto_class import AutoClass


def init_audio_config():
    """初始化音频配置"""
    print("配置音频模块...")
    
    # 设置音频格式 - 利用 IDE 自动补全
    AutoClass.AG.i2c_audio_format.w(0x3)
    AutoClass.AG.i2c_audio_width.w(0x1)
    AutoClass.AG.i2c_ext_width_en.w(0x0)
    
    print("✓ 音频配置完成")


def init_clock_config():
    """初始化时钟配置"""
    print("配置时钟模块...")
    
    # 设置采样频率
    AutoClass.AG.i2c_cs_samp_freq.w(0x4)
    AutoClass.AG.i2c_cs_word_leng.w(0x2)
    
    print("✓ 时钟配置完成")


def read_chip_status():
    """读取芯片状态"""
    print("读取芯片状态...")
    
    # 读取音频生成器状态
    aud_gen_open = AutoClass.AG.i2c_aud_gen_open.r()
    aud_gen_ready = AutoClass.AG.i2c_aud_gen_ready.r()
    
    print(f"✓ 音频生成器状态: open={aud_gen_open}, ready={aud_gen_ready}")


def main():
    """主函数"""
    print("=" * 60)
    print("GSU1K1 芯片配置示例")
    print("=" * 60)
    
    # 执行配置
    init_audio_config()
    init_clock_config()
    read_chip_status()
    
    print("\\n" + "=" * 60)
    print("配置完成！")
    print("="*60)
    print("""
下一步：
1. 在 IDE 中打开此脚本
2. 在 AutoClass 调用处输入自动补全
3. 运行: python3 unified_generator.py examples/gsu1k1_config_example.py
4. 查看 examples/gsu1k1_config_example.py.bak (原始文件)
5. 生成的代码已替换为实际 I2C 操作
    """)


if __name__ == "__main__":
    main()
''')

    print(f"✓ 示例脚本创建: {example_script}")

    # ========== 步骤 4: 演示替换功能 ==========
    print("\n[步骤 4] 演示代码替换功能...")
    print("原始脚本内容（部分）:")

    with open(example_script) as f:
        lines = f.readlines()

    # 显示第一个 AutoClass 调用
    for i, line in enumerate(lines):
        if "AutoClass." in line:
            print(f"  行 {i + 1}: {line.rstrip()}")
            if i > 5:  # 只显示几行
                break

    print("\n替换后的代码（将生成以下内容）:")
    print("  - 寄存器地址自动转换")
    print("  - 掩码和位移自动计算")
    print("  - 生成 read_reg() 和 write_bits() 调用")

    # 实际执行替换
    print("\n[步骤 5] 执行实际替换...")
    output_file = generator.replace_autoclass_calls(example_script, backup=True)

    print(f"✓ 替换完成: {output_file}")
    print(f"✓ 原始文件备份: {example_script}.bak")

    # 显示替换后的代码
    print("\n替换后的代码（部分）:")
    with open(output_file) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "read_reg\|write_bits" in line or "self.device" in line:
            print(f"  行 {i + 1}: {line.rstrip()}")
            if i > 15:
                break

    # ========== 输出总结 ==========
    print("\n" + "=" * 70)
    print("完成总结")
    print("=" * 70)
    print(f"""
✓ AutoClass 文件: {auto_class_path}
✓ 示例脚本: {example_script}
✓ 替换后脚本: {output_file}
✓ 备份文件: {example_script}.bak

关键文件位置:
- XML 定义: {xml_file}
- AutoClass (IDE): library/auto_class.py
- 生成器: src/psd_bridge/unified_generator.py

下次使用:
  python3 unified_generator.py import/GSU1K1_NTO.xml --replace my_script.py
""")

    return 0


if __name__ == "__main__":
    sys.exit(main())
