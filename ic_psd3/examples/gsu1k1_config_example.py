#!/usr/bin/env python3
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
    # w AG:i2c_audio_format <- 0x3
    self.device.write_bits(0x06, 0x00, 5, 3, 3)
    # w AG:i2c_audio_width <- 0x1
    self.device.write_bits(0x06, 0x00, 0, 5, 1)
    # w AG:i2c_ext_width_en <- 0x0
    self.device.write_bits(0x06, 0x01, 7, 1, 0)
    
    print("✓ 音频配置完成")


def init_clock_config():
    """初始化时钟配置"""
    print("配置时钟模块...")
    
    # 设置采样频率
    # w AG:i2c_cs_samp_freq <- 0x4
    self.device.write_bits(0x06, 0x02, 4, 4, 4)
    # w AG:i2c_cs_word_leng <- 0x2
    self.device.write_bits(0x06, 0x02, 0, 4, 2)
    
    print("✓ 时钟配置完成")


def read_chip_status():
    """读取芯片状态"""
    print("读取芯片状态...")
    
    # 读取音频生成器状态
    rb_i2c_aud_gen_open = (self.device.read_reg(0x06, 0x03) & 0x80) >> 7
    rb_i2c_aud_gen_ready = (self.device.read_reg(0x06, 0x03) & 0x40) >> 6
    
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
    
    print("\n" + "=" * 60)
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
