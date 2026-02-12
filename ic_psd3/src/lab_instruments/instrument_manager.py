import yaml
from .instruments.e3631a import E3631a
from .instruments.e3648a import E3648a
from .instruments.tt5166_tcp_ctr import TemperatureController


class InstrumentManager:
    """
    Manager for laboratory instruments based on a configuration file.
    """

    TYPE_MAP = {
        "E3631a": E3631a,
        "E3648a": E3648a,
        "TemperatureController": TemperatureController,
    }

    def __init__(self, config=None):
        self.instruments = {}
        if config:
            self.load_config(config)

    def load_config(self, config):
        """
        Load configuration from a dictionary or a YAML file path.
        """
        if isinstance(config, str):
            with open(config, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

        instruments_config = config.get("instruments", {})
        for name, info in instruments_config.items():
            inst_type = info.get("type")
            params = info.get("params", {})

            if inst_type in self.TYPE_MAP:
                try:
                    # Note: Physical connection might fail if hardware is not present
                    self.instruments[name] = self.TYPE_MAP[inst_type](**params)
                except Exception as e:
                    print(f"Error initializing instrument '{name}' ({inst_type}): {e}")
            else:
                print(f"Warning: Unknown instrument type '{inst_type}' for '{name}'")

    def __getitem__(self, name):
        return self.instruments.get(name)

    @classmethod
    def from_yaml(cls, yaml_path):
        """
        Factory method to create a manager from a YAML file.
        """
        return cls(config=yaml_path)
