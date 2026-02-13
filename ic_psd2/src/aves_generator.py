#!/usr/bin/env python3
"""
AVES Generator for PSD2
--------------------------------------
从 MD 函数定义生成 Python 模板，并将用户填写的 Python 代码转换为 AVES 脚本。

功能：
1. 解析 MD 文件生成 Python 模板
2. 静态解析 Python 代码（AST），提取寄存器写入操作
3. 合并同一字节的位域写入，补全默认值，生成 AVES 脚本

作者：Agent
"""

import os
import re
import json
import ast
from typing import List, Dict, Any, Tuple, Optional


class AVESGenerator:
    def __init__(self, xml_state_path: str):
        self.xml_state_path = xml_state_path
        self.reg_map = {}  # (interface, caption) -> field_data
        self.default_bytes = {}  # (interface, addr) -> default_val
        self._load_xml_state()

    def _load_xml_state(self):
        """加载 xml_state.json 并建立映射"""
        if not os.path.exists(self.xml_state_path):
            raise FileNotFoundError(f"State file not found: {self.xml_state_path}")

        with open(self.xml_state_path, "r", encoding="utf-8") as f:
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

                # 处理 mask 和 shift 字符串 -> dict
                mask_str = field.get("mask", "{}").replace("'", '"')
                shift_str = field.get("shift", "{}").replace("'", '"')

                # 简单的正则表达式解析，因为 json.loads 可能由于 hex key 失败
                mask_dict = self._parse_hex_dict(mask_str)
                shift_dict = self._parse_hex_dict(shift_str)

                field_info = {
                    "interface": if_name,
                    "caption": caption,
                    "default": field.get("defaultvalue", "0x0"),
                    "masks": mask_dict,
                    "shifts": shift_dict,
                    "name": field.get("name", ""),
                }
                self.reg_map[(if_name, caption)] = field_info

                # 预填充默认值到字节映射
                self._apply_field_default(if_name, field_info)

    def _parse_hex_dict(self, s: str) -> Dict[int, int]:
        """解析类似 {0x1000:0xFF} 的字符串为字典"""
        result = {}
        # 匹配 0xXXXX:0xXX 或 0xXXXX:数字
        matches = re.findall(r"(0x[0-9a-fA-F]+)\s*:\s*(0x[0-9a-fA-F]+|-?\d+)", s)
        for addr_str, val_str in matches:
            addr = int(addr_str, 16)
            if val_str.startswith("0x"):
                val = int(val_str, 16)
            else:
                val = int(val_str)
            result[addr] = val
        return result

    def _apply_field_default(self, if_name: str, field: Dict):
        """将字段的默认值应用到 default_bytes 映射中"""
        try:
            default_val = int(field["default"], 0)
        except (ValueError, TypeError):
            default_val = 0

        masks = field["masks"]
        shifts = field["shifts"]

        for addr, mask in masks.items():
            shift = shifts.get(addr, 0)
            if (if_name, addr) not in self.default_bytes:
                self.default_bytes[(if_name, addr)] = 0

            # 这里的逻辑：(default_val >> abs(shift)) & mask 或者 (default_val << shift) & mask
            # 根据 chip_builder 的逻辑：
            # 如果 shift 是负数（如 -8），表示这个字节是高位字节
            # ByteVal = (TotalVal >> -shift) & mask
            if shift < 0:
                byte_contrib = (default_val >> (-shift)) & mask
            else:
                byte_contrib = (default_val << shift) & mask

            self.default_bytes[(if_name, addr)] |= byte_contrib

    def generate_template(self, md_path: str, output_path: str):
        """根据 MD 生成 Python 模板"""
        if not os.path.exists(md_path):
            raise FileNotFoundError(f"MD file not found: {md_path}")

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取 Header (支持 # 或 func 关键词)
        functions = re.findall(
            r"^(?:#|func)\s*(.+?)\n(.*?)(?=\n(?:#|func)|\Z)",
            content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )

        lines = [
            "from .auto_class import AutoClass",
            "",
            "# AVES 脚本生成模板",
            "# 请在函数内使用 AutoClass.<PAGE>.<REG>.w(val) 编写逻辑",
            "",
        ]

        for name, desc in functions:
            name = name.strip()
            # 清理函数名，确保是合法的 Python 标识符
            name = re.sub(r"[^a-zA-Z0-9_]+", "_", name).strip("_")
            desc = desc.strip().replace("\n", "\n    ")
            lines.append(f"def {name}():")
            lines.append(f'    """\n    {desc}\n    """')
            lines.append("    pass")
            lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✓ Template generated: {output_path}")

    def build_aves(self, py_path: str, output_path: str):
        """解析 Python 代码并生成 AVES"""
        with open(py_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        aves_blocks = []
        func_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_count += 1
                aves_blocks.append(self._process_function(node))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(aves_blocks))
        print(f"✓ AVES script generated: {output_path} (Total {func_count} functions)")

    def _process_function(self, func_node: ast.FunctionDef) -> str:
        """处理单个 Python 函数，返回 AVES 代码块"""
        func_name = func_node.name
        # 简单模拟索引，或者可以从描述中解析
        func_index = f"{len(func_name) % 99:02d}-01"  # 临时方案

        # 记录该函数内的写入操作: (interface, addr) -> current_val
        # 初始化为全局默认值
        local_bytes = self.default_bytes.copy()
        touched_addrs = set()  # 记录哪些地址被用户显式修改过

        for stmt in func_node.body:
            # 寻找 AutoClass.PAGE.REG.w(val) 或 AutoClass.PAGE.SUB.REG.w(val)
            # 递归遍历 AST 查找所有的 Call 节点
            writes = self._find_reg_writes(stmt)

            for if_name, reg_caption, val in writes:
                # 应用写入
                if (if_name, reg_caption) in self.reg_map:
                    field = self.reg_map[(if_name, reg_caption)]
                    for addr, mask in field["masks"].items():
                        shift = field["shifts"].get(addr, 0)

                        if (if_name, addr) not in local_bytes:
                            local_bytes[(if_name, addr)] = 0

                        # 计算要写入该字节的值
                        # mask 表示该字段在字节中的位位置 (如 0x80 表示 bit 7)
                        # 需要将 value 左移到 mask 的最低有效位位置
                        mask_lsb_pos = (
                            mask & -mask
                        ).bit_length() - 1  # 找到 mask 的最低有效位位置
                        bits_to_write = (val << mask_lsb_pos) & mask

                        # 更新字节值：清除旧位，设置新位
                        local_bytes[(if_name, addr)] = (
                            local_bytes[(if_name, addr)] & ~mask
                        ) | bits_to_write
                        touched_addrs.add((if_name, addr))

        # 生成 AVES 文本
        lines = [f":{func_index} {func_name}:"]

        # 按地址排序输出
        sorted_addrs = sorted(list(touched_addrs))
        for if_name, addr in sorted_addrs:
            val = local_bytes[(if_name, addr)]
            # 寻找涉及该地址的所有字段名作为注释
            involved_fields = [
                f["caption"]
                for (inf, cap), f in self.reg_map.items()
                if inf == if_name and addr in f["masks"]
            ]
            comment = ", ".join(involved_fields[:3])  # 最多显示3个

            # AVES 格式: B0 ADDR(4字节) DATA(2字节)
            # 注意：B0 是硬编码的设备地址，ADDR 是 16位子地址，DATA 是 8位数据
            lines.append(f"B0 {addr:04X} {val:02X}  ; {comment}")

        lines.append("End")
        return "\n".join(lines)

    def _find_reg_writes(self, node: ast.AST) -> List[Tuple[str, str, int]]:
        """递归查找所有的寄存器写入操作

        返回: List of (interface_name, register_caption, value)
        """
        results = []

        # 检查当前节点是否是 Call 节点
        if isinstance(node, ast.Call):
            # 检查是否是 .w() 调用
            if isinstance(node.func, ast.Attribute) and node.func.attr == "w":
                # 解析调用链: AutoClass.XXX.YYY.w(val)
                call_chain = self._parse_call_chain(node.func.value)

                if call_chain and call_chain[0] == "AutoClass" and len(call_chain) >= 3:
                    # call_chain = ['AutoClass', 'Interface', 'Reg'] 或 ['AutoClass', 'Interface', 'Sub', 'Reg']
                    if_name = call_chain[1]
                    reg_caption = call_chain[-1]  # 最后一个元素是寄存器名

                    # 获取参数值
                    if len(node.args) == 1:
                        arg = node.args[0]
                        if isinstance(arg, ast.Constant):
                            val = arg.value
                        elif isinstance(arg, ast.Num):  # 兼容旧版本 Python
                            val = arg.n
                        else:
                            val = None  # 忽略动态计算

                        if val is not None:
                            results.append((if_name, reg_caption, val))

        # 递归遍历子节点
        for child in ast.iter_child_nodes(node):
            results.extend(self._find_reg_writes(child))

        return results

    def _parse_call_chain(self, node: ast.AST) -> List[str]:
        """解析属性调用链，如 AutoClass.Misc_Inst.i2c_rst.w

        返回: ['AutoClass', 'Misc_Inst', 'i2c_rst']
        """
        chain = []
        current = node

        while isinstance(current, ast.Attribute):
            chain.insert(0, current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            chain.insert(0, current.id)

        return chain


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="AVES Generator")
    parser.add_argument(
        "--state", default="output/xml_state.json", help="Path to xml_state.json"
    )
    parser.add_argument("--md", help="Path to function definition MD")
    parser.add_argument("--template", help="Output path for Python template")
    parser.add_argument("--py", help="Path to filled Python code")
    parser.add_argument("--aves", help="Output path for AVES script")

    args = parser.parse_args()

    if not os.path.exists(args.state):
        # 尝试默认路径
        default_state = "ic_psd2/output/xml_state.json"
        if os.path.exists(default_state):
            args.state = default_state

    generator = AVESGenerator(args.state)

    if args.md and args.template:
        generator.generate_template(args.md, args.template)
    elif args.py and args.aves:
        generator.build_aves(args.py, args.aves)
    else:
        parser.print_help()
