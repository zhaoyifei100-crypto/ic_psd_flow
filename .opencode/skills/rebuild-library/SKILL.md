---
name: rebuild-library
description: 重新生成 ic_psd3/library，从 XML 和 AVES 脚本生成 auto_class 和 aves_class
license: MIT
compatibility: opencode
metadata:
  author: yfzhao
  version: 2.0.0
---

## 功能概述

从芯片 XML 寄存器描述和 AVES 脚本生成两个 Python 类文件：
1. **auto_class.py** - 用于设计师在 IDE 中快速查找和自动补全寄存器
2. **aves_class.py** - 从 AVES 脚本生成的 Python 基础类，支持 DeviceManager

**工作流程**：清空 library → 解析 XML → 解析 AVES → 生成两个类

---

## 工作流程

### 步骤 1：确认输入文件

收集必要的输入信息。通常使用默认路径，但用户可以指定自己的路径。

**默认路径：**
- XML 文件：`ic_psd3/import/GSU1K1_NTO.xml`
- AVES 脚本：`ic_psd3/import/gsu1001_2025_nto_scripts.txt`

**向用户提问：**
```
1️⃣ XML 寄存器定义文件路径？
   （默认：ic_psd3/import/GSU1K1_NTO.xml）
   按 Enter 使用默认值，或输入自己的路径

2️⃣ AVES 脚本文件路径？
   （默认：ic_psd3/import/gsu1001_2025_nto_scripts.txt）
   按 Enter 使用默认值，或输入自己的路径
```

### 步骤 2：清空 library 目录

执行清理：
```bash
cd ic_psd3
rm -rf library/*
```

向用户说明：
```
✅ 已清空 ic_psd3/library/ 目录，准备重新生成...
```

### 步骤 3：生成 auto_class.py 和 reg_define.py

使用 unified_generator 处理 XML 文件，生成两个文件：

```bash
cd ic_psd3
python -m src.psd_bridge.unified_generator <XML_FILE_PATH>
```

执行后，检查输出：
- 生成文件 1：`ic_psd3/library/auto_class.py` - IDE 自动补全类
- 生成文件 2：`ic_psd3/library/reg_define.py` - PAGE 地址常量定义

向用户说明：
```
✅ auto_class.py 生成成功

- 用途：IDE 自动补全，快速查找寄存器
- 结构：嵌套类 AutoClass.PAGE.register
- 大小：约 2.3 MB（包含所有寄存器定义）

示例用法：
  from library.auto_class import AutoClass
  AutoClass.PAGE0.REG_NAME.r()      # 读寄存器
  AutoClass.PAGE0.REG_NAME.w(0xFF)  # 写寄存器

✅ reg_define.py 生成成功

- 用途：PAGE 地址常量定义
- 内容：所有 38 个 PAGE 的 I2C 地址（如 AG=0x06）
- 大小：约 3 KB

示例用法：
  from library.reg_define import AG, AnaPll, CdrDp1
  device.read_reg(AG, 0x00)  # 使用常量读寄存器
```

### 步骤 4：生成 aves_class.py

使用 aves_converter 处理 AVES 脚本：

```bash
cd ic_psd3
python -m src.psd_bridge.aves_converter <AVES_FILE_PATH>
```

执行后，检查输出：
- 生成文件：`ic_psd3/library/aves_class.py`
- 显示统计信息：转换的命令数等

向用户说明：
```
✅ aves_class.py 生成成功

- 用途：AVES 脚本转换为 Python，支持 DeviceManager
- 结构：AVESChipConfig 类，包含初始化方法
- 集成：与 hw_bridge DeviceManager 无缝配合

示例用法：
  from library.aves_class import AVESChipConfig
  config = AVESChipConfig(device_manager)
  config.initialize()
```

### 步骤 5：完成总结

显示生成结果：

```bash
ls -lh ic_psd3/library/*.py
```

最终总结：
```
✅ library 重新生成完成！

生成的文件：
  📄 auto_class.py     (2.3 MB  - IDE 自动补全)
  📄 reg_define.py     (3 KB    - PAGE 地址常量)
  📄 aves_class.py     (241 KB  - AVES 配置脚本)

验证方法：
  1. import library.auto_class - 检查 IDE 补全
  2. import library.reg_define - 检查 PAGE 常量
  3. import library.aves_class - 检查语法正确性

后续步骤：
  - 使用 auto_class.py 在 IDE 中编写配置脚本
  - 使用 reg_define.py 中的常量访问寄存器
  - 使用 aves_class.py 运行 AVES 初始化流程
```

---

## 示例对话

**用户：** 重新生成 library

**AI：** 我来帮你重新生成 ic_psd3/library。

首先需要确认两个输入文件的位置：

1. **XML 寄存器定义文件** - 芯片寄存器描述
   （通常：ic_psd3/import/GSU1K1_NTO.xml）

2. **AVES 脚本文件** - AVES 初始化脚本
   （通常：ic_psd3/import/gsu1001_2025_nto_scripts.txt）

请确认这两个文件的路径。

**用户：** ic_psd3/import/GSU1K1_NTO.xml 和 ic_psd3/import/gsu1001_2025_nto_scripts.txt

**AI：** 
[执行步骤 2 - 清空 library]
✅ library 目录已清空

[执行步骤 3 - 生成 auto_class.py 和 reg_define.py]
正在处理 XML 文件...
✅ auto_class.py 生成成功
  - 38 个 PAGE
  - 7,136 个寄存器
  - 文件大小：2.3 MB

✅ reg_define.py 生成成功
  - 38 个 PAGE 常量定义
  - 文件大小：3 KB

[执行步骤 4 - 生成 aves_class.py]
正在处理 AVES 脚本...
✅ aves_class.py 生成成功
  - 转换了 245 条初始化命令
  - 文件大小：125 KB

[执行步骤 5 - 显示总结]
✅ library 重新生成完成！

生成的文件：
  📄 auto_class.py     (2.3 MB)
  📄 reg_define.py     (3 KB)
  📄 aves_class.py     (125 KB)

现在你可以：
1. 在 IDE 中使用 auto_class.py 进行自动补全
2. 使用 reg_define.py 中的常量访问寄存器
3. 运行 aves_class.py 中的 AVESChipConfig 类

---

## 命令参考

### unified_generator - 生成 auto_class.py 和 reg_define.py

```bash
# 仅生成 AutoClass 和 reg_define（XML -> auto_class.py + reg_define.py）
python -m src.psd_bridge.unified_generator <XML_FILE>

# 示例
python -m src.psd_bridge.unified_generator ic_psd3/import/GSU1K1_NTO.xml
```

**参数：**
- `<XML_FILE>` - XML 寄存器定义文件路径

**输出：**
- `ic_psd3/library/auto_class.py` - IDE 补全类
- `ic_psd3/library/reg_define.py` - PAGE 地址常量定义

---

### aves_converter - 生成 aves_class.py

```bash
# AVES 脚本转换（AVES -> aves_class.py）
python -m src.psd_bridge.aves_converter <AVES_FILE>

# 示例
python -m src.psd_bridge.aves_converter ic_psd3/import/gsu1001_2025_nto_scripts.txt
```

**参数：**
- `<AVES_FILE>` - AVES 脚本文件路径

**输出：**
- `ic_psd3/library/aves_class.py` - AVES 转换的 Python 类

---

## 常见问题

**Q: 如果 XML 或 AVES 文件不存在怎么办？**

A: 会显示错误信息并停止。请检查文件路径是否正确。

---

**Q: 生成的文件格式是什么？**

A: 都是标准 Python 文件（.py），可直接导入使用。

---

**Q: 需要多久生成？**

A: 通常 < 5 秒（取决于文件大小）

---

**Q: 可以手动修改生成的文件吗？**

A: 可以，但下次重新生成会被覆盖。建议在生成后进行修改。

---

## 后续操作

### 使用 auto_class.py

```python
from library.auto_class import AutoClass

# 在 IDE 中输入会自动补全
AutoClass.PAGE0.REG_NAME.r()      # 读寄存器
AutoClass.PAGE0.REG_NAME.w(0xFF)  # 写寄存器
```

### 使用 reg_define.py

```python
from library.reg_define import AG, AnaPll, CdrDp1, Misc

# 使用常量访问寄存器
device.read_reg(AG, 0x00)       # 读 AG page
device.write_reg(AnaPll, 0x10)  # 写 AnaPll page
```

### 使用 aves_class.py

```python
from library.aves_class import AVESChipConfig
from src.hw_bridge.device_manager import DeviceManager

# 创建设备管理器
dm = DeviceManager(config_file="config.yaml")

# 使用 AVES 配置
config = AVESChipConfig(dm)
config.initialize()
```

---

**版本**: 2.0.0 | **作者**: yfzhao | **最后更新**: 2026-02-12
