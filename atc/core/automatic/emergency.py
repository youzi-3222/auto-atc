"""
自动紧急情况管理。
"""

from atc.core.automatic.base import IAutoManagement
from atc.core.scene import Scene


class Emergency(IAutoManagement):
    """
    自动紧急情况管理。
    """

    scene: Scene

    def __init__(self, scene: Scene) -> None:
        raise NotImplementedError

    def manage(self):
        """
        对目标进行管理。
        """
        raise NotImplementedError
