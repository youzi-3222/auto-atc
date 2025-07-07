"""
自动管理的基类。
"""

from abc import ABC, abstractmethod

from atc.core.scene import Scene


class IAutoManagement(ABC):
    """
    自动管理的基类。
    """

    scene: Scene

    @abstractmethod
    def __init__(self, scene: Scene) -> None:
        raise NotImplementedError

    @abstractmethod
    def manage(self):
        """
        对目标进行管理。
        """
        raise NotImplementedError
