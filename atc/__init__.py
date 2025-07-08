"""
空中交通管制的模拟库。
"""

import json
from pathlib import Path
import warnings

from .config import Config

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pygame")

_config_path = Path("./static/config.json")


def set_config_path(path: str) -> None:
    """
    设置配置文件路径。
    """
    global _config_path
    _config_path = Path(path)
    if not _config_path.exists():
        raise FileNotFoundError(f"配置文件 {_config_path} 不存在。")
    if not _config_path.is_file():
        raise IsADirectoryError(f"配置文件 {_config_path} 不是一个文件。")


with _config_path.open("r", encoding="utf-8") as f:
    config: Config = json.load(f)
