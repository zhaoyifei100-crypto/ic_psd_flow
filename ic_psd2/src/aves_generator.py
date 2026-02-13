#!/usr/bin/env python3
"""
AVES Template Generator for PSD2
--------------------------------------
从 MD 函数定义生成 Python 模板

注意：实际的 AVES 生成请使用 mock_executor.py

作者：Agent
"""

import os
import re
from typing import Dict


class AVESGenerator:
    """AVES 模板生成器 - 仅用于从 MD 生成 Python 模板"""

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
            "# 然后使用 mock_executor.py 生成 AVES 脚本",
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AVES Template Generator")
    parser.add_argument("--md", required=True, help="Path to function definition MD")
    parser.add_argument(
        "--template", required=True, help="Output path for Python template"
    )

    args = parser.parse_args()

    generator = AVESGenerator()
    generator.generate_template(args.md, args.template)
