#!/usr/bin/env python3
"""
skill_helper.py - Chip XML Builder Skill 辅助脚本

处理多轮对话的状态管理和流程控制。

用法:
    python skill_helper.py state                    # 获取当前状态
    python skill_helper.py init <chip_name> <modules_dir> [output_dir]
    python skill_helper.py check                    # 检查配置
    python skill_helper.py build                    # 执行构建
    python skill_helper.py export --format json     # 导出其他格式
    python skill_helper.py reset                    # 重置项目
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from py_testenv import ChipXMLBuilder

# 常量定义
WORK_DIR = Path(".chip-builder")
STATE_FILE = WORK_DIR / "state.json"
CONFIG_FILE = WORK_DIR / "config.yaml"


def get_state():
    """获取当前项目状态"""
    if not WORK_DIR.exists():
        return "empty"

    if not STATE_FILE.exists():
        if CONFIG_FILE.exists():
            return "ready"
        return "init"

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
            return state.get("step", "unknown")
    except Exception:
        return "error"


def init_project(chip_name, modules_dir, output_dir="./output"):
    """初始化项目，生成配置模板"""
    try:
        # 创建工作目录
        WORK_DIR.mkdir(exist_ok=True)

        # 初始化 builder
        builder = ChipXMLBuilder()
        builder.set_chip_info(
            name=chip_name,
            version="1.0.0",
            author="",
            description=f"{chip_name} Register Map",
            i2c_address="0xB0",
            wordsize=8,
            raddr_wordsize=16,
        )

        # 生成配置模板
        builder.init_config(str(CONFIG_FILE))

        # 保存状态
        state = {
            "step": "init",
            "chip_name": chip_name,
            "modules_dir": modules_dir,
            "output_dir": output_dir,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        return True, f"初始化成功！配置模板：{CONFIG_FILE}"

    except Exception as e:
        return False, f"初始化失败：{e}"


def check_config():
    """检查配置有效性"""
    if not CONFIG_FILE.exists():
        return False, "配置文件不存在，请先运行 init"

    try:
        builder = ChipXMLBuilder()
        builder.load_config(str(CONFIG_FILE))

        # 获取信息
        info = builder.get_info()

        # 检查模块是否存在
        errors = []
        modules_dict = builder.modules  # 直接访问 modules 字典
        for module_name, parser in modules_dict.items():
            xml_path = parser.xml_path if hasattr(parser, "xml_path") else str(parser)
            if not os.path.exists(xml_path):
                errors.append(f"模块 XML 不存在：{xml_path}")

        if errors:
            return False, "\n".join(errors)

        # 检查地址冲突
        conflicts = builder.check_address_conflict()
        if conflicts:
            conflict_msgs = []
            for c in conflicts:
                conflict_msgs.append(
                    f"地址冲突：{c[0]} ({c[2]:04X}-{c[2] + c[4]:04X}) 与 "
                    f"{c[1]} ({c[3]:04X}-{c[3] + c[4]:04X})"
                )
            return False, "\n".join(conflict_msgs)

        # 更新状态
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            state["step"] = "ready"
            state["updated_at"] = datetime.now().isoformat()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

        # 生成摘要
        chip_info = builder.chip_info
        summary = f"""配置检查通过

芯片信息：
- 名称：{getattr(chip_info, "name", "N/A")}
- 版本：{getattr(chip_info, "version", "N/A")}
- I2C 地址：{getattr(chip_info, "i2c_address", "N/A")}

模块列表（{len(modules_dict)} 个）：
"""
        for name, parser in modules_dict.items():
            xml_path = parser.xml_path if hasattr(parser, "xml_path") else str(parser)
            summary += f"- {name} → {xml_path}\n"

        summary += f"\n实例映射（{len(builder.instances)} 个）：\n"
        for inst in builder.instances[:10]:  # 只显示前10个
            summary += f"- {inst.name} ({inst.module_name}) @ 0x{inst.base_addr:04X}\n"

        if len(builder.instances) > 10:
            summary += f"... 还有 {len(builder.instances) - 10} 个实例\n"

        return True, summary

    except Exception as e:
        return False, f"配置检查失败：{e}"


def build_project():
    """执行构建"""
    if not CONFIG_FILE.exists():
        return False, "配置文件不存在"

    try:
        # 读取状态获取输出目录
        output_dir = "./output"
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                output_dir = state.get("output_dir", "./output")

        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # 加载配置
        builder = ChipXMLBuilder()
        builder.load_config(str(CONFIG_FILE))

        # 检查冲突
        conflicts = builder.check_address_conflict()
        if conflicts:
            return False, f"存在地址冲突，请先修复配置"

        # 更新状态为 building
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            state["step"] = "building"
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

        # 执行构建
        builder.build()

        # 获取芯片名称
        info = builder.get_info()
        chip_name = info.get("chip_name", "chip")

        # 导出文件
        xml_file = output_path / f"{chip_name}_Chip.xml"
        excel_file = output_path / f"{chip_name}_AddressMap.xlsx"

        builder.export_xml(str(xml_file))
        builder.export_excel(str(excel_file))

        # 更新状态为 done
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            state["step"] = "done"
            state["output_files"] = {"xml": str(xml_file), "excel": str(excel_file)}
            state["build_time"] = datetime.now().isoformat()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

        # 统计信息
        stats = f"""构建成功！

生成文件：
- {xml_file} （芯片级寄存器定义）
- {excel_file} （地址映射表）

构建统计：
- 模块数：{len(builder.modules)}
- 实例数：{len(builder.instances)}
"""

        return True, stats

    except Exception as e:
        # 恢复状态
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            state["step"] = "ready"
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

        return False, f"构建失败：{e}"


def export_format(format_type):
    """导出其他格式"""
    if not CONFIG_FILE.exists():
        return False, "配置文件不存在"

    try:
        builder = ChipXMLBuilder()
        builder.load_config(str(CONFIG_FILE))

        # 读取输出目录
        output_dir = "./output"
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                output_dir = state.get("output_dir", "./output")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        info = builder.get_info()
        chip_name = info.get("chip_name", "chip")

        if format_type == "json":
            json_file = output_path / f"{chip_name}.json"
            builder.export_json(str(json_file))
            return True, f"已导出 JSON：{json_file}"

        elif format_type == "excel":
            excel_file = output_path / f"{chip_name}_Registers.xlsx"
            builder.export_excel(str(excel_file))
            return True, f"已导出 Excel：{excel_file}"

        else:
            return False, f"不支持的格式：{format_type}"

    except Exception as e:
        return False, f"导出失败：{e}"


def reset_project():
    """重置项目"""
    try:
        import shutil

        if WORK_DIR.exists():
            shutil.rmtree(WORK_DIR)
            return True, "项目已重置，可以重新开始"
        else:
            return True, "没有需要重置的项目"
    except Exception as e:
        return False, f"重置失败：{e}"


def main():
    parser = argparse.ArgumentParser(description="Chip XML Builder Skill 辅助脚本")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # state 命令
    subparsers.add_parser("state", help="获取当前状态")

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化项目")
    init_parser.add_argument("chip_name", help="芯片名称")
    init_parser.add_argument("modules_dir", help="模块 XML 目录")
    init_parser.add_argument(
        "output_dir", nargs="?", default="./output", help="输出目录"
    )

    # check 命令
    subparsers.add_parser("check", help="检查配置")

    # build 命令
    subparsers.add_parser("build", help="执行构建")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出其他格式")
    export_parser.add_argument("--format", choices=["json", "excel"], required=True)

    # reset 命令
    subparsers.add_parser("reset", help="重置项目")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "state":
        state = get_state()
        print(state)

    elif args.command == "init":
        success, msg = init_project(args.chip_name, args.modules_dir, args.output_dir)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "check":
        success, msg = check_config()
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "build":
        success, msg = build_project()
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "export":
        success, msg = export_format(args.format)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "reset":
        success, msg = reset_project()
        print(msg)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
