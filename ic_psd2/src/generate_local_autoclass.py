#!/usr/bin/env python3
import sys
import os

# 确保可以导入 ic_psd3 中的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ic_psd3.src.psd_bridge.unified_generator import AutoClassGenerator


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 script_for_psd2.py <xml_file> <output_auto_class_path>")
        sys.exit(1)

    xml_file = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(xml_file):
        print(f"Error: XML file not found: {xml_file}")
        sys.exit(1)

    generator = AutoClassGenerator(xml_file)
    generator.generate_auto_class(output_path)
    print(f"✓ Generated AutoClass for PSD2 at: {output_path}")


if __name__ == "__main__":
    main()
