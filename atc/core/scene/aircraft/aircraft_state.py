"""
航班状态。
"""

from dataclasses import dataclass

from pygame import Vector2


@dataclass
class AircraftState:
    """
    航班状态。
    """

    pos: Vector2
    """位置。"""
    heading: int
    """航向。"""
    alt_ft: int
    """高度，英尺。"""
    climb_rate: int
    """爬升率，英尺 / 分钟。"""
    speed_kt: int
    """速度，节。"""
