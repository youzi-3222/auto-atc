"""
预测式控制。
"""

from src.atc.core.automatic.base import IAutoManagement
from src.atc.core.scene import Scene


class AutoPredictive(IAutoManagement):
    """
    预测式控制，即通过预测航班将来的位置状态，推断是否存在危险，完成调度。
    """

    def __init__(self, scene: Scene) -> None:
        raise NotImplementedError

    def manage(self):
        raise NotImplementedError
