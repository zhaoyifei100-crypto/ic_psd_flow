"""
Mock I2C Driver for PSD2
--------------------------------------
用于 AVES 脚本生成的虚拟 I2C 驱动器

功能：
1. 维护虚拟 I2C Memory
2. 从 xml_state.json 加载默认值
3. 记录所有写入操作到 write_log
4. 支持 read_reg/write_reg/write_bits 三种操作

作者：AI Assistant
"""

import json
import re
from typing import Dict, List, Tuple, Optional


class MockDriver:
    """
    虚拟 I2C 驱动器

    模拟真实的 I2C 设备行为，用于在生成 AVES 脚本前验证和执行配置逻辑。
    所有写入操作都会被记录到 write_log，用于生成最终的 AVES 脚本。

    Attributes:
        i2c_mem: 虚拟 I2C 内存，键为 (addr1, addr2)，值为当前字节值
        write_log: 写入操作记录，格式为 [(addr1, addr2, value), ...]
        reg_map: 寄存器映射，从 xml_state 解析得到 {(if_name, reg_name): field_info}
        default_bytes: 默认字节值 {(if_name, addr): default_val}
    """

    def __init__(self):
        self.i2c_mem: Dict[Tuple[int, int], int] = {}
        self.write_log: List[Tuple[int, int, int]] = []
        self.reg_map: Dict[Tuple[str, str], dict] = {}
        self.default_bytes: Dict[Tuple[str, int], int] = {}

    def init_from_xml_state(self, xml_state_path: str):
        """
        从 xml_state.json 加载所有默认值

        Args:
            xml_state_path: xml_state.json 文件路径
        """
        with open(xml_state_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 假设只有一个 device
        device = data.get("device", [{}])[0]
        interfaces = device.get("interface", [])

        for interface in interfaces:
            if_name = interface.get("name")
            fields = interface.get("field", [])

            for field in fields:
                caption = field.get("caption")
                if not caption:
                    continue

                # 解析 mask 和 shift
                mask_dict = self._parse_hex_dict(field.get("mask", "{}"))
                shift_dict = self._parse_hex_dict(field.get("shift", "{}"))
                default_val = field.get("defaultvalue", "0x0")

                field_info = {
                    "interface": if_name,
                    "caption": caption,
                    "default": default_val,
                    "masks": mask_dict,
                    "shifts": shift_dict,
                    "name": field.get("name", ""),
                }
                self.reg_map[(if_name, caption)] = field_info

                # 计算并存储默认值到 i2c_mem
                self._apply_field_default(if_name, field_info)

    def _parse_hex_dict(self, s: str) -> Dict[int, int]:
        """解析类似 {0x1000:0xFF} 的字符串为字典"""
        result = {}
        matches = re.findall(r"(0x[0-9a-fA-F]+)\s*:\s*(0x[0-9a-fA-F]+|-?\d+)", s)
        for addr_str, val_str in matches:
            addr = int(addr_str, 16)
            if val_str.startswith("0x"):
                val = int(val_str, 16)
            else:
                val = int(val_str)
            result[addr] = val
        return result

    def _apply_field_default(self, if_name: str, field: dict):
        """将字段的默认值应用到 i2c_mem"""
        try:
            default_val = int(field["default"], 0)
        except (ValueError, TypeError):
            default_val = 0

        masks = field["masks"]
        shifts = field["shifts"]

        for addr, mask in masks.items():
            shift = shifts.get(addr, 0)

            # 计算该字段对该字节的贡献
            if shift < 0:
                byte_contrib = (default_val >> (-shift)) & mask
            else:
                byte_contrib = (default_val << shift) & mask

            # 转换为 (addr1, addr2) 格式
            addr1 = (addr >> 8) & 0xFF
            addr2 = addr & 0xFF

            # 合并到现有值
            key = (addr1, addr2)
            current_val = self.i2c_mem.get(key, 0)
            self.i2c_mem[key] = (current_val & ~mask) | byte_contrib

            # 同时存储到 default_bytes 用于参考
            if (if_name, addr) not in self.default_bytes:
                self.default_bytes[(if_name, addr)] = 0
            self.default_bytes[(if_name, addr)] = self.i2c_mem[key]

    def read_reg(self, addr1: int, addr2: int) -> int:
        """
        读取寄存器当前值

        Args:
            addr1: 高字节地址 (Page)
            addr2: 低字节地址 (Offset)

        Returns:
            int: 当前字节值 (0-255)
        """
        return self.i2c_mem.get((addr1, addr2), 0)

    def write_reg(self, addr1: int, addr2: int, value: int):
        """
        直接写入整个字节

        Args:
            addr1: 高字节地址 (Page)
            addr2: 低字节地址 (Offset)
            value: 要写入的值 (0-255)
        """
        value = value & 0xFF
        self.i2c_mem[(addr1, addr2)] = value
        self.write_log.append((addr1, addr2, value))

    def write_bits(self, addr1: int, addr2: int, mask: int, value: int):
        """
        读-修改-写（用于 bit 操作）

        先读取当前值，按 mask 清除对应位，然后设置新值

        Args:
            addr1: 高字节地址 (Page)
            addr2: 低字节地址 (Offset)
            mask: 位掩码，指示要修改的位
            value: 新值（已对齐到正确位置）
        """
        old_val = self.read_reg(addr1, addr2)
        new_val = (old_val & ~mask) | (value & mask)
        self.write_reg(addr1, addr2, new_val)

    def reg_write(self, if_name: str, reg_name: str, value: int):
        """
        通过寄存器名称写入（用于 AutoClass 调用）

        Args:
            if_name: 接口名称（如 "Misc_Inst"）
            reg_name: 寄存器名称（如 "i2c_main_rst"）
            value: 要写入的值
        """
        key = (if_name, reg_name)
        if key not in self.reg_map:
            raise ValueError(f"Unknown register: {if_name}.{reg_name}")

        field = self.reg_map[key]

        for addr, mask in field["masks"].items():
            shifts = field["shifts"]
            shift = shifts.get(addr, 0)

            # 计算 mask 的最低有效位位置
            mask_lsb_pos = (mask & -mask).bit_length() - 1

            # 计算要写入的位：将 value 左移到 mask 的 LSB 位置
            # mask 表示该字段在字节中的位位置（如 0x80 表示 bit 7）
            if shift < 0:
                # 负 shift：字段跨字节，需要特殊处理
                # 先右移处理字段值的高位部分，再左移到字节位置
                bits_to_write = ((value >> (-shift)) << mask_lsb_pos) & mask
            else:
                # 正 shift 或零：直接左移到正确位置
                bits_to_write = ((value << shift) << mask_lsb_pos) & mask

            # 转换为 (addr1, addr2)
            addr1 = (addr >> 8) & 0xFF
            addr2 = addr & 0xFF

            # 使用 write_bits 进行读-修改-写
            self.write_bits(addr1, addr2, mask, bits_to_write)

    def reg_read(self, if_name: str, reg_name: str) -> int:
        """
        通过寄存器名称读取（用于 AutoClass 调用）

        Args:
            if_name: 接口名称（如 "Misc_Inst"）
            reg_name: 寄存器名称（如 "i2c_main_rst"）

        Returns:
            int: 寄存器的当前值
        """
        key = (if_name, reg_name)
        if key not in self.reg_map:
            raise ValueError(f"Unknown register: {if_name}.{reg_name}")

        field = self.reg_map[key]

        # 假设寄存器只在一个地址上（简化处理）
        result = 0
        for addr, mask in field["masks"].items():
            shifts = field["shifts"]
            shift = shifts.get(addr, 0)

            addr1 = (addr >> 8) & 0xFF
            addr2 = addr & 0xFF

            byte_val = self.read_reg(addr1, addr2)
            field_val = byte_val & mask

            if shift < 0:
                field_val = field_val << (-shift)
            else:
                field_val = field_val >> shift

            result |= field_val

        return result

    def get_write_log(self) -> List[Tuple[int, int, int]]:
        """获取写入记录"""
        return self.write_log.copy()

    def clear_write_log(self):
        """清空写入记录"""
        self.write_log.clear()

    def dump_mem(self, start: int = 0, end: int = 0xFFFF):
        """打印指定范围的 I2C 内存内容（用于调试）"""
        print(f"[MockDriver] I2C Memory dump 0x{start:04X}-0x{end:04X}:")
        for (addr1, addr2), value in sorted(self.i2c_mem.items()):
            addr = (addr1 << 8) | addr2
            if start <= addr <= end:
                print(f"  0x{addr:04X} = 0x{value:02X}")

    def get_reg_info(self, if_name: str, reg_name: str) -> Optional[dict]:
        """获取寄存器信息"""
        return self.reg_map.get((if_name, reg_name))
