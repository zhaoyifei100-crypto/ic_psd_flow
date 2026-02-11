---
name: chip-xml-builder
description: 通过多轮对话帮助用户生成芯片级 XML 寄存器定义文件
license: MIT
compatibility: opencode
metadata:
  author: yfzhao
  version: 1.0.0
---

## 功能概述

帮助芯片验证工程师通过自然语言对话生成完整的芯片级寄存器定义 XML 文件。

支持：多模块 XML 合并、单模块多实例、地址映射、冲突检测、Excel 配置。

## 工作流程

这是一个状态驱动的多轮对话工具。

### 状态检查

**第 0 步：检查当前状态**

```bash
python scripts/skill_helper.py state
```

返回值：
- `empty` - 未初始化
- `init` - 已生成配置模板
- `ready` - 配置就绪
- `done` - 已完成

### 步骤 1：初始化项目（状态 = empty）

收集信息：
1. 芯片名称（如 GSU1K1）
2. 模块 XML 目录（如 ./models/）
3. 输出目录（默认 ./output）

执行：
```bash
python scripts/skill_helper.py init <chip_name> <modules_dir> [output_dir]
```

向用户说明：
- 已生成配置模板：`.chip-builder/config.xlsx`
- 填写 ChipInfo、Modules、Instances 三个表
- 编辑完成后说"继续"

### 步骤 2：检查配置（状态 = init）

用户说"继续"后：
```bash
python scripts/skill_helper.py check
```

如有效，显示摘要并询问是否构建。  
如无效，显示错误并等待修复。

### 步骤 3：执行构建

用户确认后：
```bash
python scripts/skill_helper.py build
```

成功则显示生成的文件路径。  
失败则显示错误详情。

### 步骤 4：后续操作

- 导出 JSON：`python scripts/skill_helper.py export --format json`
- 重新开始：`python scripts/skill_helper.py reset`

## 示例对话

**用户：** 帮我生成 chip xml

**AI：** 我来帮你。先检查状态...
[运行 state]

你是第一次使用。请告诉我：
1. 芯片名称？
2. 模块 XML 目录？

**用户：** GSU1K1, ./modules/

**AI：** 初始化中...
[运行 init GSU1K1 ./modules/]

✅ 已生成配置模板：`.chip-builder/config.xlsx`

请填写：
- ChipInfo 表：芯片信息
- Modules 表：添加模块路径
- Instances 表：定义实例映射

编辑后说"继续"。

**用户：** 继续

**AI：** 检查配置...
[运行 check]

✅ 配置有效！开始构建吗？

**用户：** 开始

**AI：** 构建中...
[运行 build]

✅ 构建成功！
- ./output/GSU1K1_Chip.xml
- ./output/GSU1K1_AddressMap.xlsx

## 命令参考

```bash
python scripts/skill_helper.py state      # 查看状态
python scripts/skill_helper.py init ...   # 初始化
python scripts/skill_helper.py check      # 检查配置
python scripts/skill_helper.py build      # 执行构建
python scripts/skill_helper.py reset      # 重置项目
```

## 注意事项

1. 配置文件必须放在 `.chip-builder/config.xlsx`
2. 模块 XML 路径可以是相对路径或绝对路径
3. 构建前会自动检测地址冲突
4. 重复构建会覆盖之前的输出

**版本**: 1.0.0 | **作者**: yfzhao
