"""
Mock Executor for PSD2 AVES Generation
--------------------------------------
使用 MockDriver 实际执行 Python 代码并生成 AVES 脚本

工作流程：
1. 初始化 MockDriver，从 xml_state.json 加载默认值
2. 绑定 AutoClass 到 MockDriver
3. 执行用户编写的 aves_template.py
4. 从 MockDriver 的 write_log 生成 AVES 脚本

作者：AI Assistant
"""

import os
import sys
import json
import argparse
from typing import List, Tuple, Optional

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mock_driver import MockDriver


class MockExecutor:
    """
    Mock 执行器

    负责：
    - 初始化 MockDriver
    - 构建 AutoClass 绑定
    - 执行用户代码
    - 生成 AVES 脚本
    """

    def __init__(self, xml_state_path: str):
        """
        初始化执行器

        Args:
            xml_state_path: xml_state.json 文件路径
        """
        self.xml_state_path = xml_state_path
        self.driver = MockDriver()
        self.driver.init_from_xml_state(xml_state_path)

    def build_autoclass(self) -> type:
        """
        构建 AutoClass 类，绑定到 MockDriver

        根据 xml_state.json 中的寄存器定义，动态生成嵌套类结构。
        每个寄存器的 .r() 和 .w(val) 方法都会调用 MockDriver。

        Returns:
            AutoClass 类
        """
        # 构建接口和寄存器的层级结构
        interface_regs = {}  # {if_name: [reg_name, ...]}

        for (if_name, reg_name), field_info in self.driver.reg_map.items():
            if if_name not in interface_regs:
                interface_regs[if_name] = []
            interface_regs[if_name].append((reg_name, field_info))

        # 动态创建 AutoClass
        class AutoClass:
            """AutoClass 根类，由 MockExecutor 动态生成"""

            pass

        # 为每个接口创建子类
        for if_name, regs in interface_regs.items():
            # 创建接口类
            interface_class = type(
                if_name,
                (),
                {
                    "__doc__": f"Interface: {if_name}",
                },
            )

            # 为每个寄存器创建子类
            for reg_name, field_info in regs:
                masks = field_info["masks"]
                shifts = field_info["shifts"]

                # 创建寄存器类
                def make_reg_class(if_name, reg_name, masks, shifts):
                    class RegClass:
                        _if_name = if_name
                        _reg_name = reg_name
                        _masks = masks
                        _shifts = shifts
                        _driver = self.driver

                        @classmethod
                        def w(cls, value: int):
                            """写入寄存器"""
                            cls._driver.reg_write(cls._if_name, cls._reg_name, value)

                        @classmethod
                        def r(cls) -> int:
                            """读取寄存器"""
                            return cls._driver.reg_read(cls._if_name, cls._reg_name)

                        @classmethod
                        def write_bits(cls, mask: int, value: int):
                            """
                            位写入（读-修改-写）

                            注意：这是低级别接口，一般使用 .w() 即可
                            """
                            # 找到对应的地址
                            for addr, field_mask in cls._masks.items():
                                addr1 = (addr >> 8) & 0xFF
                                addr2 = addr & 0xFF
                                # 将 mask 和 value 对齐到字节位置
                                mask_lsb_pos = (
                                    field_mask & -field_mask
                                ).bit_length() - 1
                                byte_mask = mask << mask_lsb_pos
                                byte_value = (value & mask) << mask_lsb_pos
                                cls._driver.write_bits(
                                    addr1, addr2, byte_mask, byte_value
                                )

                    RegClass.__name__ = reg_name
                    RegClass.__qualname__ = f"AutoClass.{if_name}.{reg_name}"
                    return RegClass

                reg_class = make_reg_class(if_name, reg_name, masks, shifts)
                setattr(interface_class, reg_name, reg_class)

            # 将接口类附加到 AutoClass
            setattr(AutoClass, if_name, interface_class())

        return AutoClass

    def execute_script(self, script_path: str) -> List[Tuple[int, int, int]]:
        """
        执行用户脚本

        Args:
            script_path: Python 脚本路径

        Returns:
            List[Tuple[int, int, int]]: 写入日志 [(addr1, addr2, value), ...]
        """
        # 清空之前的写入记录
        self.driver.clear_write_log()

        # 构建 AutoClass
        AutoClass = self.build_autoclass()

        # 读取并预处理脚本（移除相对导入）
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # 移除相对导入语句（如 "from .auto_class import AutoClass"）
        import re

        script_content = re.sub(
            r"^from\s+\.\S+\s+import\s+.*$", "", script_content, flags=re.MULTILINE
        )
        script_content = re.sub(
            r"^import\s+\.\S+.*$", "", script_content, flags=re.MULTILINE
        )

        # 准备执行环境
        exec_globals = {
            "AutoClass": AutoClass,
            "__name__": "__aves_script__",
            "__file__": script_path,
        }

        # 执行脚本
        exec(script_content, exec_globals)

        # 返回写入记录
        return self.driver.get_write_log()

    def generate_aves(
        self, script_path: str, output_path: str, func_index_start: int = 1
    ):
        """
        生成 AVES 脚本

        Args:
            script_path: 用户 Python 脚本路径
            output_path: AVES 输出路径
            func_index_start: 起始函数索引（默认 1，对应 01-01）
        """
        # 执行脚本获取写入记录
        write_log = self.execute_script(script_path)

        # 如果没有写入记录，输出警告
        if not write_log:
            print(f"⚠️  Warning: No I2C operations captured from {script_path}")
            # 仍然创建一个空的 AVES 文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("; No I2C operations generated\n")
            return output_path

        # 生成 AVES 脚本
        lines = []
        func_index = func_index_start

        # 简单策略：每个地址变化或连续操作都生成一个 B0 行
        # 注意：write_log 已经按执行顺序记录了所有操作

        # 按顺序输出所有写入
        lines.append(f":01-{func_index:02d} auto_generated:")

        for addr1, addr2, value in write_log:
            addr = (addr1 << 8) | addr2
            lines.append(f"B0 {addr:04X} {value:02X}")

        lines.append("End")

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✓ AVES script generated: {output_path}")
        print(f"  Total I2C operations: {len(write_log)}")

        return output_path

    def _get_addr_comments(self, addr1: int, addr2: int) -> str:
        """
        获取地址的注释信息

        查找该地址涉及的所有寄存器字段
        """
        comments = []
        addr_full = (addr1 << 8) | addr2

        for (if_name, reg_name), field_info in self.driver.reg_map.items():
            masks = field_info.get("masks", {})
            for addr, mask in masks.items():
                if addr == addr_full:
                    # 找到匹配的地址
                    comments.append(reg_name)
                    break

        return ", ".join(comments[:3]) if comments else ""

    def _extract_autoclass_calls(self, script_content: str, func_name: str) -> list:
        """
        从函数体中提取 AutoClass 调用行

        Args:
            script_content: 脚本内容
            func_name: 函数名

        Returns:
            list: AutoClass 调用代码行列表
        """
        import ast
        import re

        tree = ast.parse(script_content)

        # 找到目标函数
        target_func = None
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                target_func = node
                break

        if not target_func:
            return []

        # 获取源代码行
        lines = script_content.split("\n")
        autoclass_calls = []

        # 匹配 AutoClass 调用模式
        pattern = re.compile(r"AutoClass\.\w+\.\w+\.(w|r)\([^)]*\)")

        for node in ast.walk(target_func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # 获取该节点在源代码中的行号
                    if hasattr(node, "lineno"):
                        line_no = node.lineno - 1  # 转换为 0-based 索引
                        if 0 <= line_no < len(lines):
                            line_content = lines[line_no].strip()
                            # 检查是否包含 AutoClass 调用
                            if "AutoClass." in line_content and pattern.search(
                                line_content
                            ):
                                # 提取 AutoClass 部分
                                match = pattern.search(line_content)
                                if match:
                                    call_str = match.group(0)
                                    autoclass_calls.append(call_str)

        return autoclass_calls

    def generate_aves_per_function(
        self, script_path: str, output_path: str, func_index_start: int = 1
    ):
        """
        按函数生成 AVES 脚本（支持多个独立函数）

        特性：
        - 不合并同一地址的连续写入
        - 在每个函数前添加 AutoClass 调用作为注释

        Args:
            script_path: 用户 Python 脚本路径
            output_path: AVES 输出路径
            func_index_start: 起始函数索引（默认 1，对应 01-01）
        """
        import ast

        # 解析脚本获取函数定义
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        tree = ast.parse(script_content)

        # 找到所有顶层函数
        functions = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        if not functions:
            # 没有函数定义，使用默认方式
            return self.generate_aves(script_path, output_path, func_index_start)

        # 为每个函数生成独立的 AVES 块
        lines = []
        sub_index = 1

        for func_name in functions:
            # 清空写入记录
            self.driver.clear_write_log()

            # 构建 AutoClass
            AutoClass = self.build_autoclass()

            # 预处理脚本内容（移除相对导入）
            import re

            processed_content = re.sub(
                r"^from\s+\.\S+\s+import\s+.*$", "", script_content, flags=re.MULTILINE
            )
            processed_content = re.sub(
                r"^import\s+\.\S+.*$", "", processed_content, flags=re.MULTILINE
            )

            # 执行单个函数
            exec_globals = {
                "AutoClass": AutoClass,
                "__name__": "__aves_script__",
                "__file__": script_path,
            }
            exec(processed_content, exec_globals)

            # 调用函数
            if func_name in exec_globals:
                exec_globals[func_name]()

            # 获取写入记录
            write_log = self.driver.get_write_log()

            # 提取该函数的 AutoClass 调用
            autoclass_calls = self._extract_autoclass_calls(script_content, func_name)

            if write_log:
                lines.append(f":{func_index_start:02d}-{sub_index:02d} {func_name}:")

                # 添加 AutoClass 调用作为注释
                if autoclass_calls:
                    lines.append("; AutoClass commands:")
                    for call in autoclass_calls:
                        lines.append(f";   {call}")

                # 输出所有写入（不合并，无行内注释）
                for addr1, addr2, value in write_log:
                    addr = (addr1 << 8) | addr2
                    lines.append(f"B0 {addr:04X} {value:02X};")
                lines.append("End")
                lines.append("")  # 空行分隔
                sub_index += 1

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✓ AVES script generated: {output_path}")
        print(f"  Total functions: {len(functions)}")

        return output_path


def main():
    parser = argparse.ArgumentParser(description="Mock Executor for AVES Generation")
    parser.add_argument(
        "--state",
        default="output/xml_state.json",
        help="Path to xml_state.json (default: output/xml_state.json)",
    )
    parser.add_argument(
        "--py",
        required=True,
        help="Path to Python script to execute",
    )
    parser.add_argument(
        "--aves",
        required=True,
        help="Path for AVES output",
    )
    parser.add_argument(
        "--per-func",
        action="store_true",
        help="Generate separate AVES block for each function",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=1,
        help="Starting function index (default: 1, generates 01-01, 01-02, ...)",
    )

    args = parser.parse_args()

    # 调整默认路径
    state_path = args.state
    if not os.path.exists(state_path):
        alt_path = os.path.join("ic_psd2", state_path)
        if os.path.exists(alt_path):
            state_path = alt_path

    if not os.path.exists(state_path):
        print(f"Error: xml_state.json not found: {state_path}")
        sys.exit(1)

    if not os.path.exists(args.py):
        print(f"Error: Python script not found: {args.py}")
        sys.exit(1)

    # 创建执行器
    executor = MockExecutor(state_path)

    # 生成 AVES
    if args.per_func:
        executor.generate_aves_per_function(args.py, args.aves, args.index)
    else:
        executor.generate_aves(args.py, args.aves, args.index)


if __name__ == "__main__":
    main()
