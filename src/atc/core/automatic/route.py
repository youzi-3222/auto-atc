"""
自动航路管理。
"""

from src.atc.core.automatic.base import IAutoManagement
from src.atc.core.scene import Scene


class AutoRoute(IAutoManagement):
    """
    自动航路管理。包括：

    * 单个航路上飞机间隔的管理
    * 多个航路汇聚到同一条航路时，飞机间隔的管理

    常用于标准进近程序。这种管理应当尽早完成，保证航班能充裕地拉开间距。
    """

    scene: Scene
    """场景。"""

    def __init__(self, scene: Scene) -> None:
        raise NotImplementedError

    def manage(self):
        raise NotImplementedError

    def _manage_single(self):
        raise NotImplementedError
