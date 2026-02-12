"""
AutoClass Unified Generator
--------------------------------------
整合 xml_parser 和 auto_py_script 功能，生成 IDE 友好的寄存器访问类。

核心功能：
1. generate_auto_class(): 生成 library/auto_class.py，提供 IDE 自动补全
2. replace_autoclass_calls(): 将 AutoClass.PAGE.reg.r()/w(val) 替换为实际 I2C 代码

设计原则：
- AutoClass 作为中间层，仅用于 IDE 补全（方法体为 pass）
- 替换功能生成实际的 I2C 读写代码
- 支持 DeviceManager 架构

作者：AI Assistant
"""

import os
import re
import json
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


class AutoClassGenerator:
    """
    统一的 AutoClass 生成器

    整合 XML 解析和代码生成功能：
    - 解析 XML 提取寄存器信息
    - 生成嵌套类结构用于 IDE 补全
    - 替换 AutoClass 调用为实际 I2C 代码
    """

    def __init__(self, xml_file_path: str, class_instance_name: str = "self.device"):
        """
        初始化生成器

        Args:
            xml_file_path: XML 寄存器定义文件路径
            class_instance_name: 类实例名，用于生成 I2C 代码（如 "self.device"）
        """
        self.xml_file = xml_file_path
        self.class_instance_name = class_instance_name
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()

        # 基础数据
        self.dev_addr_dict = {}
        self.json_data = {}
        self.page_reg_map = {}

        # 解析数据
        self._parse_xml_data()

    def _parse_xml_data(self):
        """解析 XML 并构建内部数据结构"""
        self._parse_device_addresses()
        self._build_json_data()
        self._build_page_reg_map()

    def _parse_device_addresses(self):
        """提取设备地址映射 {page_name: page_address}"""
        file_node = self.root
        if file_node.tag != "file":
            raise ValueError("根节点不是 file，请检查 XML 结构")

        device = file_node.find("device")
        if device is None:
            raise ValueError("XML 文件中未找到 device 节点")

        interfaces = device.findall("interface")
        for interface in interfaces:
            name_node = interface.find("name")
            if name_node is None:
                continue
            page_name = name_node.text
            if not page_name:
                continue

            field = interface.find("field")
            if field is not None:
                address_node = field.find("address")
                if address_node is not None:
                    full_address = address_node.text
                    if full_address:
                        page_address = full_address[:4]
                        self.dev_addr_dict[page_name] = page_address

        # 反向字典
        self.addr_to_key = {int(v, 16): k for k, v in self.dev_addr_dict.items()}

    def _parse_mask_shift(self, mask_shift_str: str) -> List[Tuple[str, str]]:
        """解析 mask 和 shift 字段"""
        if not mask_shift_str or mask_shift_str == "{}":
            return []

        entries = []
        items = mask_shift_str.strip("{}").split(",")
        for item in items:
            if ":" in item:
                addr_part, value_part = item.split(":")
                addr = addr_part.strip()
                value = value_part.strip()
                entries.append((addr, value))
        return entries

    def _get_base_key(self, byte_address: Optional[str]) -> str:
        """根据字节地址获取 PAGE 名称"""
        if not byte_address:
            return "UNKNOWN"
        addr_int = int(byte_address, 16)
        base_addr = addr_int >> 8
        return self.addr_to_key.get(base_addr, f"0x{base_addr:02X}")

    def _build_json_data(self):
        """构建 JSON 格式的寄存器数据"""
        registers = []

        for field in self.root.findall(".//field[@class='Field']"):
            name = field.findtext("name")
            caption = field.findtext("caption") or name
            address = field.findtext("address")
            default_value = field.findtext("defaultvalue")
            size = field.findtext("size")
            description = field.findtext("description") or ""
            datatype = field.findtext("datatype") or ""
            mask = field.findtext("mask") or "{}"
            shift = field.findtext("shift") or "{}"
            byteorder = field.findtext("byteorder") or ""

            # 解析基地址
            base_addr = "0x0000"
            if address:
                match = re.match(r"(0x[0-9A-Fa-f]+)", address)
                base_addr = match.group(1) if match else address.split(".")[0]

            # 解析位域范围
            bit_range = None
            range_match = re.search(r"\[(\d+):(\d+)\]", name) if name else None
            if range_match:
                msb = int(range_match.group(1))
                lsb = int(range_match.group(2))
                bit_range = f"[{msb}:{lsb}]"
                total_bits = msb - lsb + 1
            else:
                total_bits = int(size) if size else 1

            # 解析 mask 和 shift
            mask_entries = self._parse_mask_shift(mask)
            shift_entries = self._parse_mask_shift(shift)

            configs = defaultdict(dict)
            for addr, mask_val in mask_entries:
                configs[addr]["mask"] = mask_val
            for addr, shift_val in shift_entries:
                configs[addr]["shift"] = shift_val

            # 为每个字节配置创建条目
            for byte_addr, byte_config in configs.items():
                mask_val = byte_config.get("mask", "0x00")
                effective_bits = bin(int(mask_val, 16)).count("1")

                register_data = {
                    "register_name": self._clean_reg_name(caption) if caption else "",
                    "base_address": base_addr,
                    "field_name": name,
                    "bit_range": bit_range,
                    "total_bits": total_bits,
                    "default_value": default_value,
                    "data_type": datatype,
                    "description": description,
                    "byte_address": byte_addr,
                    "byte_mask": byte_config.get("mask", ""),
                    "byte_shift": byte_config.get("shift", ""),
                    "effective_bits": effective_bits,
                }
                registers.append(register_data)

        # 按 PAGE 组织
        self.json_data = self._organize_by_page(registers)

    def _clean_reg_name(self, name: str) -> str:
        """清理寄存器名称中的特殊字符"""
        if not name:
            return name
        name = name.replace(" ", "_")
        name = name.replace("/", "_")
        name = name.replace("-", "_")
        name = name.replace("[", "_")
        name = name.replace("]", "_")
        name = name.replace("(", "_")
        name = name.replace(")", "_")
        return name

    def _organize_by_page(self, registers: List[dict]) -> Dict[str, List[dict]]:
        """按 PAGE 组织寄存器数据"""
        organized = {}
        for reg in registers:
            byte_addr = reg.get("byte_address")
            if not byte_addr:
                continue
            page_name = self._get_base_key(byte_addr)
            if page_name not in organized:
                organized[page_name] = []
            organized[page_name].append(reg)
        return organized

    def _build_page_reg_map(self):
        """构建两级哈希表：PAGE -> register_name -> [寄存器信息]"""
        for page, registers in self.json_data.items():
            if page not in self.page_reg_map:
                self.page_reg_map[page] = {}
            for reg in registers:
                reg_name = reg.get("register_name")
                if reg_name:
                    if reg_name not in self.page_reg_map[page]:
                        self.page_reg_map[page][reg_name] = []
                    self.page_reg_map[page][reg_name].append(reg.copy())

    def _get_register_info(self, page: str, reg_name: str) -> Optional[List[dict]]:
        """O(1) 查找寄存器信息"""
        page_dict = self.page_reg_map.get(page)
        if not page_dict:
            return None
        return page_dict.get(reg_name)

    def _to_valid_class_name(self, name: Optional[str]) -> str:
        """转换为有效的 Python 类名"""
        if not name:
            return ""
        valid_name = name.replace(":", "_")
        if valid_name and valid_name[0].isdigit():
            valid_name = f"reg_{valid_name}"
        return valid_name

    # ==================== 功能 1: 生成 AutoClass 文件 ====================

    def generate_auto_class(self, output_path: Optional[str] = None) -> str:
        """
        生成 auto_class.py 文件，提供 IDE 自动补全

        Args:
            output_path: 输出文件路径，默认 library/auto_class.py

        Returns:
            生成的文件路径
        """
        if output_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            output_path = os.path.join(base_dir, "library", "auto_class.py")

        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            # 文件头
            f.write('"""\n')
            f.write("Auto-generated Register Access Class\n")
            f.write("Generated from: {}\n".format(os.path.basename(self.xml_file)))
            f.write("=====================================\n\n")
            f.write("This class provides IDE autocomplete for register access.\n")
            f.write(
                "Use with replace_autoclass_calls() to generate actual I2C code.\n\n"
            )
            f.write("Example:\n")
            f.write("    AutoClass.AG.i2c_audio_format.r()      # Read register\n")
            f.write("    AutoClass.AG.i2c_audio_format.w(0x3)   # Write register\n")
            f.write('"""\n\n')

            # 主类定义
            f.write("class AutoClass:\n")
            f.write('    """\n')
            f.write("    Register access class for IDE autocomplete.\n")
            f.write("    All methods are placeholders (pass).\n")
            f.write(
                "    Use replace_autoclass_calls() to replace with actual I2C code.\n"
            )
            f.write('    """\n\n')

            # 统计信息
            total_pages = len(self.json_data)
            total_regs = sum(len(regs) for regs in self.json_data.values())
            f.write(
                f"    # Total Pages: {total_pages}, Total Registers: {total_regs}\n\n"
            )

            # 为每个 PAGE 生成子类
            for page_name in sorted(self.json_data.keys()):
                registers = self.json_data[page_name]
                f.write(f"    class {page_name}:\n")
                f.write(
                    f'        """Page: {page_name}, Address: {self.dev_addr_dict.get(page_name, "N/A")}"""\n'
                )

                if not registers:
                    f.write("        pass\n\n")
                    continue

                # 去重：一个 register_name 只生成一次
                seen_regs = set()
                for reg in registers:
                    reg_name = reg.get("register_name")
                    if not reg_name or reg_name in seen_regs:
                        continue
                    seen_regs.add(reg_name)

                    class_name = self._to_valid_class_name(reg_name)
                    byte_addr = reg.get("byte_address", "N/A")

                    f.write(f"        class {class_name}:\n")
                    f.write(
                        f'            """Register: {reg_name}, Address: {byte_addr}"""\n'
                    )
                    f.write("            @staticmethod\n")
                    f.write("            def r():\n")
                    f.write('                """Read register value"""\n')
                    f.write("                pass\n\n")
                    f.write("            @staticmethod\n")
                    f.write("            def w(val):\n")
                    f.write('                """Write value to register"""\n')
                    f.write("                pass\n\n")

                f.write("\n")

        # Calculate total unique registers
        total_unique_regs = sum(
            len(
                set(
                    reg.get("register_name") for reg in regs if reg.get("register_name")
                )
            )
            for regs in self.json_data.values()
        )

        print(f"✓ AutoClass generated: {output_path}")
        print(f"  Pages: {total_pages}, Unique Registers: {total_unique_regs}")
        return output_path

    # ==================== 功能 2: 替换 AutoClass 调用 ====================

    def _get_addr12(self, addr_str: str) -> Tuple[str, str]:
        """将 16 位地址拆分为 addr1, addr2"""
        addr_int = int(addr_str, 16)
        addr1 = (addr_int >> 8) & 0xFF
        addr2 = addr_int & 0xFF
        return (f"0x{addr1:02X}", f"0x{addr2:02X}")

    def _get_rshift_str(self, byte_shift: str) -> str:
        """生成位移字符串"""
        shift = int(byte_shift)
        if shift == 0:
            return ""
        elif shift < 0:
            return f" << {-shift}"
        else:
            return f" >> {shift}"

    def _get_read_cmd(self, reg_info: dict) -> str:
        """生成读取命令"""
        addr_str = reg_info.get("byte_address", "0x0000")
        addr1, addr2 = self._get_addr12(addr_str)

        byte_mask = reg_info.get("byte_mask")
        if byte_mask == "0xFF":
            byte_mask_str = ""
        else:
            byte_mask_str = f" & {byte_mask}"

        shift_str = self._get_rshift_str(reg_info.get("byte_shift", "0"))

        cmd = f"({self.class_instance_name}.read_reg({addr1}, {addr2}){byte_mask_str}){shift_str}"
        return cmd

    def _get_read_list(self, page: str, reg_name: str) -> List[str]:
        """生成读取寄存器的代码列表"""
        return_list = []
        reg_info_list = self._get_register_info(page, reg_name)

        if not reg_info_list:
            return_list.append(f"# ERROR: {page}.{reg_name} not found")
            return return_list

        if len(reg_info_list) == 1:
            # 单个寄存器
            reg_info = reg_info_list[0]
            full_cmd = f"rb_{reg_name} = {self._get_read_cmd(reg_info)}"
            return_list.append(full_cmd)
        else:
            # 多个寄存器（跨字节）
            return_list.append(f"rb_{reg_name} = 0")
            for reg_info in reg_info_list:
                full_cmd = f"rb_{reg_name} |= {self._get_read_cmd(reg_info)}"
                return_list.append(full_cmd)

        return return_list

    def _mask_to_lsb_bits(self, mask: str) -> Tuple[int, int]:
        """将掩码转换为 LSB 位置和位数"""
        mask_int = int(mask, 16)
        if mask_int == 0:
            return (0, 0)

        # 计算 LSB 位置
        lsb = (mask_int & -mask_int).bit_length() - 1

        # 计算连续 1 的位数
        shifted = mask_int >> lsb
        bits = 0
        while shifted & 1:
            bits += 1
            shifted >>= 1

        return (lsb, bits)

    def _get_w_val(self, shift: str, mask: str, w_str: str) -> int:
        """计算写入值"""
        if w_str.startswith(("0x", "0X")):
            w_num = int(w_str, 16)
        else:
            w_num = int(w_str)

        shift_num = int(shift)
        mask_num = int(mask, 16)

        if shift_num == 0:
            return w_num & mask_num
        elif shift_num < 0:
            return (w_num >> -shift_num) & mask_num
        else:
            return ((w_num << shift_num) & mask_num) >> shift_num

    def _get_write_cmd(self, reg_info: dict, value_var: str) -> str:
        """生成写入命令"""
        addr_str = reg_info.get("byte_address", "0x0000")
        mask_str = reg_info.get("byte_mask", "0xFF")
        shift_str = reg_info.get("byte_shift", "0")

        addr1, addr2 = self._get_addr12(addr_str)
        lsb, bits = self._mask_to_lsb_bits(mask_str)
        write_val_num = self._get_w_val(shift_str, mask_str, value_var)

        cmd = f"{self.class_instance_name}.write_bits({addr1}, {addr2}, {lsb}, {bits}, {write_val_num})"
        return cmd

    def _get_write_list(self, page: str, reg_name: str, value_var: str) -> List[str]:
        """生成写入寄存器的代码列表"""
        return_list = []
        reg_info_list = self._get_register_info(page, reg_name)

        if not reg_info_list:
            return_list.append(f"# ERROR: {page}.{reg_name} not found")
            return return_list

        # 添加注释
        return_list.append(f"# w {page}:{reg_name} <- {value_var}")

        for reg_info in reg_info_list:
            full_cmd = self._get_write_cmd(reg_info, value_var)
            return_list.append(full_cmd)

        return return_list

    def replace_autoclass_calls(
        self, file_path: str, output_path: Optional[str] = None, backup: bool = True
    ) -> str:
        """
        将文件中的 AutoClass 调用替换为实际 I2C 代码

        匹配模式：
        - AutoClass.PAGE.reg.r()       → 读取代码
        - AutoClass.PAGE.reg.w(val)    → 写入代码

        Args:
            file_path: 输入文件路径
            output_path: 输出文件路径，默认覆盖原文件
            backup: 是否备份原文件

        Returns:
            输出文件路径
        """
        if output_path is None:
            output_path = file_path

        # 备份原文件
        if backup and file_path == output_path:
            backup_path = file_path + ".bak"
            if os.path.exists(file_path):
                shutil.copy2(file_path, backup_path)
                print(f"✓ Backup created: {backup_path}")

        # 读取文件
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 匹配模式：AutoClass.<PAGE>.<reg>.<op>(<args>)
        pattern = re.compile(
            r"AutoClass\.(?P<page>\w+)\.(?P<reg>\w+)\.(?P<op>r|w)\(\s*(?P<args>[^)]*)\)"
        )

        new_lines = []
        replaced_count = {"read": 0, "write": 0}

        for line in lines:
            match = pattern.search(line)
            if match:
                page = match.group("page")
                reg = match.group("reg")
                op = match.group("op")
                args = match.group("args").strip()
                indent_match = re.match(r"\s*", line)
                indent = indent_match.group(0) if indent_match else ""

                if op == "r":
                    cmds = self._get_read_list(page, reg)
                    replaced_count["read"] += 1
                    print(f"[READ] {page}.{reg}")
                else:  # op == 'w'
                    value_var = args if args else "0"
                    cmds = self._get_write_list(page, reg, value_var)
                    replaced_count["write"] += 1
                    print(f"[WRITE] {page}.{reg} <- {value_var}")

                for cmd in cmds:
                    new_lines.append(f"{indent}{cmd}\n")
            else:
                new_lines.append(line)

        # 写回文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        total = replaced_count["read"] + replaced_count["write"]
        print(f"\n✓ Replacement complete: {output_path}")
        print(f"  Read operations: {replaced_count['read']}")
        print(f"  Write operations: {replaced_count['write']}")
        print(f"  Total replaced: {total}")

        return output_path

    # ==================== 功能 3: 生成寄存器定义文件 ====================

    def generate_reg_define(self, output_path: Optional[str] = None) -> str:
        """
        生成 reg_define.py 文件，包含所有 PAGE 的地址定义

        从 XML 中提取 IIC memory 的 pagename 和地址，生成 Python 常量定义文件。
        格式：PAGE_NAME = 0xADDRESS

        Args:
            output_path: 输出文件路径，默认 library/reg_define.py

        Returns:
            生成的文件路径
        """
        if output_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            output_path = os.path.join(base_dir, "library", "reg_define.py")

        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            # 文件头
            f.write('"""\n')
            f.write("Register Definition Constants\n")
            f.write("Generated from: {}\n".format(os.path.basename(self.xml_file)))
            f.write("=====================================\n\n")
            f.write("This file defines I2C memory page addresses extracted from XML.\n")
            f.write("Use these constants to access chip registers.\n\n")
            f.write("Example:\n")
            f.write("    from library.reg_define import *\n")
            f.write("    device.read_reg(AG, 0x00)  # Read from AG page\n")
            f.write('"""\n\n')

            # 按页面名称排序生成定义
            sorted_pages = sorted(self.dev_addr_dict.items())

            if sorted_pages:
                f.write("# I2C Memory Page Addresses\n")
                for page_name, page_address in sorted_pages:
                    f.write(f"{page_name} = {page_address}\n")
                f.write("\n")

                # 添加字典映射便于查询
                f.write("# Page Name to Address Mapping\n")
                f.write("PAGE_MAP = {\n")
                for page_name, page_address in sorted_pages:
                    f.write(f'    "{page_name}": {page_address},\n')
                f.write("}\n\n")

                # 添加反向映射（地址到名称）
                f.write("# Address to Page Name Mapping\n")
                f.write("ADDR_MAP = {\n")
                for page_name, page_address in sorted_pages:
                    f.write(f'    {page_address}: "{page_name}",\n')
                f.write("}\n\n")

                # 统计信息和导出清单
                f.write(f"# Total Pages: {len(sorted_pages)}\n")
                all_exports = sorted([page_name for page_name, _ in sorted_pages])
                all_exports.extend(["PAGE_MAP", "ADDR_MAP"])
                f.write(f"__all__ = {all_exports}\n")

        print(f"✓ Register definitions generated: {output_path}")
        print(f"  Total pages: {len(sorted_pages)}")
        return output_path

    # ==================== 便捷方法 ====================

    def generate_all(
        self,
        auto_class_path: Optional[str] = None,
        target_file: Optional[str] = None,
        reg_define_path: Optional[str] = None,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        """
        一键生成 AutoClass、reg_define 并替换目标文件

        Args:
            auto_class_path: auto_class.py 输出路径
            target_file: 需要替换的文件路径
            reg_define_path: reg_define.py 输出路径

        Returns:
            (auto_class_path, replaced_file_path, reg_define_path)
        """
        auto_path = self.generate_auto_class(auto_class_path)

        replaced_path = None
        if target_file is not None and os.path.exists(target_file):
            replaced_path = self.replace_autoclass_calls(target_file)

        reg_define_file = None
        if reg_define_path is not None:
            reg_define_file = self.generate_reg_define(reg_define_path)

        return (auto_path, replaced_path, reg_define_file)


# ==================== 命令行接口 ====================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python unified_generator.py <xml_file>")
        print("                                [--replace <target_file>]")
        print("                                [--reg-define [output_path]]")
        print("")
        print("Options:")
        print("  --replace <file>      Replace AutoClass calls in target file")
        print("  --reg-define [path]   Generate reg_define.py with page addresses")
        print("")
        print("Examples:")
        print("  # Generate auto_class.py only")
        print("  python unified_generator.py GSU1K1_NTO.xml")
        print("")
        print("  # Generate auto_class.py and reg_define.py")
        print("  python unified_generator.py GSU1K1_NTO.xml --reg-define")
        print("")
        print("  # Generate with custom output paths")
        print("  python unified_generator.py GSU1K1_NTO.xml \\")
        print("    --reg-define library/my_reg_define.py \\")
        print("    --replace my_script.py")
        sys.exit(1)

    xml_file = sys.argv[1]

    if not os.path.exists(xml_file):
        print(f"Error: XML file not found: {xml_file}")
        sys.exit(1)

    # 创建生成器
    generator = AutoClassGenerator(xml_file)

    # 始终生成 auto_class.py
    generator.generate_auto_class()

    # 检查是否有 --replace 参数
    if "--replace" in sys.argv:
        idx = sys.argv.index("--replace")
        if idx + 1 < len(sys.argv):
            target_file = sys.argv[idx + 1]
            generator.replace_autoclass_calls(target_file)
        else:
            print("Error: --replace requires a target file")
            sys.exit(1)

    # 检查是否有 --reg-define 参数
    if "--reg-define" in sys.argv:
        idx = sys.argv.index("--reg-define")
        output_path = None
        # 检查是否提供了输出路径
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("--"):
            output_path = sys.argv[idx + 1]
        generator.generate_reg_define(output_path)
