#!/usr/bin/env python3
"""
Simple Test Runner - 轻量级测试执行器
======================================

由 AGENT 直接生成代码，本文件仅负责：
1. 扫描库并构建索引
2. 执行生成的测试脚本

Usage:
    python runner.py <testspec.md> [--output-dir <dir>] [--dry-run]

Author: AI Assistant
Date: 2026-02-13
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def scan_library(library_dir: str, output_dir: Path) -> Dict:
    """扫描 library 并构建函数索引。"""
    lib_path = Path(library_dir)
    index_path = output_dir / "library_index.json"

    print("[INFO] 扫描库文件...")
    index = {
        "usb_common_class": extract_class_info(lib_path / "usb_common_class.py"),
        "psd3_common_class": extract_class_info(lib_path / "psd3_common_class.py"),
        "aves_class": extract_class_info(lib_path / "aves_class.py"),
        "registers": extract_registers(lib_path / "reg_define.py"),
    }

    # 保存索引到测试目录
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    total = len(index["usb_common_class"]["methods"]) + len(
        index["aves_class"]["methods"]
    )
    print(f"[INFO] 已索引 {total} 个函数")
    return index


def extract_class_info(filepath: Path) -> Dict:
    """从 Python 文件中提取类方法。"""
    info = {"methods": {}}
    if not filepath.exists():
        return info

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 使用方法定义正则
        method_pattern = (
            r'def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*\w+)?\s*:\s*(?:\s*"""([\s\S]*?)""")?'
        )
        for match in re.finditer(method_pattern, content):
            name, args, docstring = match.groups()
            if not name.startswith("_"):
                info["methods"][name] = {
                    "args": args,
                    "docstring": docstring.strip() if docstring else "",
                }
    except Exception as e:
        print(f"[WARN] 扫描失败 {filepath}: {e}")

    return info


def extract_registers(filepath: Path) -> Dict[str, str]:
    """从 reg_define.py 提取寄存器常量。"""
    registers = {}
    if not filepath.exists():
        return registers

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 匹配: NAME = 0xXX
        for match in re.finditer(
            r"^([A-Z][A-Za-z0-9]*)\s*=\s*(0x[0-9A-Fa-f]+)", content, re.M
        ):
            name, value = match.groups()
            registers[name] = value
    except Exception as e:
        print(f"[WARN] 扫描寄存器失败: {e}")

    return registers


def execute_test(script_path: str, output_dir: Path) -> bool:
    """执行测试脚本并返回成功状态。"""
    print(f"[INFO] 执行测试: {script_path}")
    print("-" * 60)

    log_file = output_dir / "exec.log"

    try:
        with open(log_file, "w", encoding="utf-8") as log_f:
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            if process.stdout:
                for line in process.stdout:
                    line = line.rstrip()
                    print(line)
                    log_f.write(line + "\n")
                    log_f.flush()

            process.wait()

        print("-" * 60)
        return process.returncode == 0

    except Exception as e:
        print(f"[ERROR] 执行失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Simple Test Runner")
    parser.add_argument("spec_file", help="测试规格 Markdown 文件")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--library-dir", default="ic_psd3/library")
    parser.add_argument("--dry-run", action="store_true", help="仅生成代码不执行")

    args = parser.parse_args()

    spec_path = Path(args.spec_file)
    if not spec_path.exists():
        print(f"[ERROR] 规格文件不存在: {spec_path}")
        sys.exit(1)

    # 确定输出目录
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path("ic_psd3/tests/generated") / spec_path.stem

    print(f"[INFO] 测试: {spec_path.stem}")
    print(f"[INFO] 输出: {output_dir}\n")

    # 步骤 1: 扫描库
    library_index = scan_library(args.library_dir, output_dir)

    # 步骤 2: 读取规格（由 AGENT 解析）
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()

    # 步骤 3: 由 AGENT 生成代码
    # AGENT 使用 library_index 和 spec_content 直接生成 test_script.py
    script_path = output_dir / "test_script.py"

    if args.dry_run:
        print(f"\n[INFO] 干运行模式 - 库索引已生成: {output_dir}/library_index.json")
        print("[INFO] AGENT 现在可以基于索引和规格生成代码")
        sys.exit(0)

    # 检查代码是否已生成
    if not script_path.exists():
        print(f"[ERROR] 测试脚本不存在: {script_path}")
        print("[INFO] 请先让 AGENT 生成代码，或运行 --dry-run 查看索引")
        sys.exit(1)

    # 步骤 4: 执行测试
    success = execute_test(str(script_path), output_dir)

    # 报告结果
    print()
    print("=" * 60)
    if success:
        print("✓ [PASS] 测试通过")
        print(f"✓ 结果: {output_dir}/summary.json")
    else:
        print("✗ [FAIL] 测试失败")
        print(f"✗ 日志: {output_dir}/exec.log")
    print("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
