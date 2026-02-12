# Lab Instruments 使用指南

本项目提供了统一的实验室仪器管理接口，支持通过直接导入驱动或使用 `InstrumentManager` 配置化管理。

## 📁 目录结构

- `ic_psd3/src/lab_instruments/`
    - `instruments/`: 存放具体的仪器驱动文件（e.g., `e3631a.py`）
    - `instrument_manager.py`: 仪器管理器，支持从 YAML 加载配置
    - `config.yaml`: 默认的仪器配置文件

---

## 🚀 在 Testcase 中使用

### debug使用，简单直接导入
如果你只需要使用特定的仪器，可以直接从 `lab_instruments` 导入：

```python
from lab_instruments import E3631a, TemperatureController

# 初始化电源
vsource = E3631a(gpib=6, setMaxLimit=True)
vsource.setVoltage('P6V', 5.0)
vsource.outputEnable()

# 初始化温箱
temp_ctrl = TemperatureController('192.168.6.211', 3000)
temp_ctrl.temper_ctr(53)
```

### 推荐使用 InstrumentManager (配置驱动)
当你需要管理多个仪器，或者希望在不同实验室环境（Lab A/B）之间快速切换而无需修改代码时，建议使用管理器。

#### 配置 `config.yaml`
```yaml
instruments:
  vsource_main:
    type: E3631a
    params:
      gpib: 6
      setMaxLimit: true
  
  temp_controller:
    type: TemperatureController
    params:
      ip_address: '192.168.6.211'
      port: 3000
```

#### 在代码中使用
```python
from lab_instruments import InstrumentManager

# 从配置文件初始化所有仪器
manager = InstrumentManager.from_yaml('path/to/config.yaml')

# 通过名称获取仪器实例
vsource = manager['vsource_main']
temp_ctrl = manager['temp_controller']

# 直接调用方法
if vsource:
    vsource.setVoltage('P6V', 3.3)
```

---

## 🛠 如何添加新仪器

1.  **编写驱动**：在 `lab_instruments/instruments/` 目录下新建 Python 文件（例如 `my_scope.py`）。
2.  **注册导出**：在 `lab_instruments/__init__.py` 中添加导入行：
    ```python
    from .instruments.my_scope import MyScope
    ```
3.  **配置管理 (可选)**：如果需要通过 `InstrumentManager` 调用，在 `instrument_manager.py` 的 `TYPE_MAP` 中添加映射：
    ```python
    TYPE_MAP = {
        "MyScope": MyScope,
        # ...
    }
    ```

---

## ⚠️ 注意事项
- **物理连接**：初始化仪器时，程序会尝试建立物理连接（GPIB/TCP），请确保硬件已连接并在线。
- **依赖项**：部分仪器依赖 `pyvisa` 和相应的驱动库（如 NI-VISA）。
