import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Config:
    def __init__(self, filepath: Path):
        self._config = self._load_config(filepath)
        if "data_dir" in self._config:
            path = Path(self._config["data_dir"])
            if not path.is_absolute():
                path = BASE_DIR / path
            self._config["data_dir"] = path


    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    @staticmethod
    def _load_config(filepath: Path) -> dict:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]


GlobalConfig = Config(BASE_DIR / "config/config.json")
