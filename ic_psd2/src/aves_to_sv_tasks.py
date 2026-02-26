#!/usr/bin/env python3
"""
Convert AVES scripts to SystemVerilog tasks for local TB.

Input:  generated_aves.txt
Output: aves_tasks.sv (interface with tasks)
"""

import argparse
import os
import re
from typing import Dict, List, Tuple


FUNC_HEADER_RE = re.compile(r"^:\d{2}-\d{2}\s+([A-Za-z0-9_]+)\s*:")
B0_RE = re.compile(r"^B0\s+([0-9A-Fa-f]{4})\s+([0-9A-Fa-f]{2})")


def parse_aves(aves_path: str) -> Dict[str, List[Tuple[int, int, int]]]:
    """Parse AVES file into function write sequences.

    Args:
        aves_path: Path to generated_aves.txt.

    Returns:
        Mapping of function name -> list of (page, reg, value).
    """
    functions: Dict[str, List[Tuple[int, int, int]]] = {}
    current_func = None

    with open(aves_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            match = FUNC_HEADER_RE.match(line)
            if match:
                current_func = match.group(1)
                functions.setdefault(current_func, [])
                continue
            if line.startswith("End"):
                current_func = None
                continue
            if current_func is None:
                continue
            if line.startswith(";"):
                continue
            m_b0 = B0_RE.match(line)
            if not m_b0:
                continue
            addr = int(m_b0.group(1), 16)
            value = int(m_b0.group(2), 16)
            page = (addr >> 8) & 0xFF
            reg = addr & 0xFF
            functions[current_func].append((page, reg, value))

    return functions


def render_sv_interface(
    functions: Dict[str, List[Tuple[int, int, int]]],
    interface_name: str,
) -> str:
    """Render SystemVerilog interface with tasks.

    Args:
        functions: Mapping of function name -> write list.
        interface_name: Name for the generated interface.

    Returns:
        SystemVerilog source as string.
    """
    lines = []
    lines.append("`ifndef AVES_TASKS_SV")
    lines.append("`define AVES_TASKS_SV")
    lines.append("")
    lines.append(f"interface {interface_name};")
    lines.append("    parameter time AVES_WRCLK_HALF = 5;")
    lines.append("    parameter time AVES_WR_DELAY = 1;")
    lines.append("")
    lines.append("    logic wrclock;")
    lines.append("    logic wrEn;")
    lines.append("    logic [7:0] regAddr;")
    lines.append("    logic [7:0] dataIn;")
    lines.append("")
    lines.append("    task automatic init_signals();")
    lines.append("        wrclock = 1'b0;")
    lines.append("        wrEn = 1'b0;")
    lines.append("        regAddr = 8'h00;")
    lines.append("        dataIn = 8'h00;")
    lines.append("    endtask")
    lines.append("")
    lines.append("    task automatic i2c_mem_write(")
    lines.append("        input [7:0] addr,")
    lines.append("        input [7:0] data,")
    lines.append("        input time wrclk_half = AVES_WRCLK_HALF,")
    lines.append("        input time wr_delay = AVES_WR_DELAY")
    lines.append("    );")
    lines.append("        regAddr = addr;")
    lines.append("        dataIn = data;")
    lines.append("        wrEn = 1'b1;")
    lines.append("        wrclock = 1'b0;")
    lines.append("        #(wrclk_half);")
    lines.append("        wrclock = 1'b1;")
    lines.append("        #(wrclk_half);")
    lines.append("        wrclock = 1'b0;")
    lines.append("        wrEn = 1'b0;")
    lines.append("        #(wr_delay);")
    lines.append("    endtask")
    lines.append("")

    for func_name, writes in functions.items():
        lines.append(f"    task automatic {func_name}();")
        if not writes:
            lines.append("        // No writes for this function")
        else:
            last_page = None
            for page, reg, value in writes:
                if last_page != page:
                    lines.append(f"        // page 0x{page:02X}")
                    last_page = page
                lines.append(f"        i2c_mem_write(8'h{reg:02X}, 8'h{value:02X});")
        lines.append("    endtask")
        lines.append("")

    lines.append(f"endinterface : {interface_name}")
    lines.append("")
    lines.append("`endif")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert AVES scripts to SystemVerilog tasks"
    )
    parser.add_argument(
        "--aves",
        default="ic_psd2/output/generated_aves.txt",
        help="Path to AVES script (default: ic_psd2/output/generated_aves.txt)",
    )
    parser.add_argument(
        "--out",
        default="ic_psd2/output/aves_tasks.sv",
        help="Output SystemVerilog path (default: ic_psd2/output/aves_tasks.sv)",
    )
    parser.add_argument(
        "--ifname",
        default="aves_i2c_mem_if",
        help="Interface name (default: aves_i2c_mem_if)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.aves):
        raise FileNotFoundError(f"AVES file not found: {args.aves}")

    functions = parse_aves(args.aves)
    sv_text = render_sv_interface(functions, args.ifname)

    out_dir = os.path.dirname(args.out)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(sv_text)

    print(f"✓ SV tasks generated: {args.out}")
    print(f"  Total functions: {len(functions)}")


if __name__ == "__main__":
    main()
