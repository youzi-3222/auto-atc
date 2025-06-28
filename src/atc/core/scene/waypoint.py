"""
航路点。
"""

from pygame import Vector2

from src.atc.config import _WayPoint
from src.atc.const import RESOLUTION


class WayPoint:
    """
    航路点。
    """

    pos: Vector2
    """位置。"""
    name: str
    """航路点名称。"""

    def __init__(self, wp: _WayPoint) -> None:
        pos = wp["position"]
        if len(pos) != 2:
            raise ValueError(
                f"Waypoint position must be a list of 2 elements, got {pos}"
            )
        if not (0 <= pos[0] <= 1 and 0 <= pos[1] <= 1):
            raise ValueError(f"Waypoint position must be between 0 and 1, got {pos}")
        self.name = wp["name"]
        self.pos = Vector2(
            pos[0] * RESOLUTION[0],
            pos[1] * RESOLUTION[1],
        )

    def __repr__(self) -> str:
        return f"WayPoint({self.pos}, {self.name!r})"

    def __str__(self) -> str:
        return f"WayPoint({self.pos}, {self.name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WayPoint):
            return False
        return self.pos == other.pos and self.name == other.name
