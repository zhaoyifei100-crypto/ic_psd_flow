---
name: chip-xml-builder
description: 通过配置文件驱动生成芯片级 XML 寄存器定义文件
license: MIT
compatibility: opencode
metadata:
  author: yfzhao
  version: 2.0.0
---

## 功能概述

帮助芯片验证工程师通过 YAML 配置文件生成完整的芯片级寄存器定义 XML 文件。
支持：多模块 XML 合并、单模块多实例、地址映射、冲突检测。

## 工作流程

这是一个由配置文件驱动的工具。所有中间文件和输出结果应统一存放在 `output/` 目录下。

### 步骤 1：准备配置文件

1. 在 `output/` 目录下创建或生成配置文件，命名格式为 `xml_config.yaml`。
2. 确保 `xml_config.yaml` 指向正确的子模块 XML 路径（通常在 `models/` 目录下）。

### 步骤 2：执行构建

执行：
```bash
# 在 ic_psd2 目录下运行
python3 src/chip_builder.py output/xml_config.yaml ./output
```

向用户说明：
- 结果文件（XML 和 Excel）已生成在 `output/` 中。
- 中间状态或配置快照会自动生成在 `output/xml_state.json`。

## 文件命名规范 (output/ 目录)

| 文件名 | 用途 |
| :--- | :--- |
| `xml_config.yaml` | XML 构建器的输入配置 |
| `xml_state.json` | XML 构建过程产生的状态/元数据 |
| `[ChipName]_Chip.xml` | 生成的芯片级 XML |
| `[ChipName]_AddressMap.xlsx` | 生成的地址映射表 |

## 示例配置文件 (output/xml_config.yaml)

```yaml
chip_info:
  name: "GSU1K1"
  version: "1.0.0"

modules:
  - module_name: "PLL"
    xml_path: "../models/PLL_CTRL.xml"  # 注意相对于执行目录或配置文件的路径

instances:
  - name: "PllInst"
    module_name: "PLL"
    base_addr: "0x1000"
```

## 命令参考

```bash
python3 src/chip_builder.py output/xml_config.yaml ./output
```

## 注意事项

1. 推荐使用 YAML 格式配置。
2. 构建前会自动检测地址冲突。
3. 重复构建会覆盖之前的输出。

**版本**: 2.0.0 | **作者**: yfzhao
