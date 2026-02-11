#!/usr/bin/env python3
"""
chip_cli.py - Chip XML Builder 命令行接口

简化版 CLI，供习惯命令行的用户使用。Skill 内部也使用此接口。

用法:
    python scripts/chip_cli.py init --chip-name GSU1K1 --modules-dir ./models/
    python scripts/chip_cli.py build
    python scripts/chip_cli.py status
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from scripts.skill_helper import (
    get_state,
    init_project,
    check_config,
    build_project,
    export_format,
    reset_project,
)


def print_status():
    """打印当前状态"""
    state = get_state()

    status_map = {
        "empty": "未初始化",
        "init": "已生成配置模板，等待编辑",
        "ready": "配置就绪，可以构建",
        "building": "正在构建中",
        "done": "已完成构建",
        "error": "状态错误",
        "unknown": "未知状态",
    }

    print(f"当前状态: {status_map.get(state, state)}")

    if state in ["ready", "done"]:
        from scripts.skill_helper import STATE_FILE

        if STATE_FILE.exists():
            import json

            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                print(f"芯片名称: {data.get('chip_name', 'N/A')}")
                print(f"输出目录: {data.get('output_dir', './output')}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Chip XML Builder - 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化项目
  python scripts/chip_cli.py init --chip-name GSU1K1 --modules-dir ./models/
  
  # 检查配置
  python scripts/chip_cli.py check
  
  # 执行构建
  python scripts/chip_cli.py build
  
  # 查看状态
  python scripts/chip_cli.py status
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化项目")
    init_parser.add_argument("--chip-name", "-c", required=True, help="芯片名称")
    init_parser.add_argument("--modules-dir", "-m", required=True, help="模块 XML 目录")
    init_parser.add_argument("--output-dir", "-o", default="./output", help="输出目录")

    # check 命令
    subparsers.add_parser("check", help="检查配置有效性")

    # build 命令
    build_parser = subparsers.add_parser("build", help="执行构建")
    build_parser.add_argument(
        "--force", "-f", action="store_true", help="强制构建（跳过检查）"
    )

    # status 命令
    subparsers.add_parser("status", help="查看当前状态")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出其他格式")
    export_parser.add_argument(
        "--format", choices=["json", "excel"], default="json", help="导出格式"
    )

    # reset 命令
    subparsers.add_parser("reset", help="重置项目")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "status":
        print_status()
        return 0

    elif args.command == "init":
        success, msg = init_project(args.chip_name, args.modules_dir, args.output_dir)
        print(msg)
        return 0 if success else 1

    elif args.command == "check":
        success, msg = check_config()
        print(msg)
        return 0 if success else 1

    elif args.command == "build":
        if not args.force:
            # 先检查配置
            success, msg = check_config()
            if not success:
                print(f"配置检查未通过：\n{msg}")
                print("\n使用 --force 强制构建（不推荐）")
                return 1

        success, msg = build_project()
        print(msg)
        return 0 if success else 1

    elif args.command == "export":
        success, msg = export_format(args.format)
        print(msg)
        return 0 if success else 1

    elif args.command == "reset":
        success, msg = reset_project()
        print(msg)
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
