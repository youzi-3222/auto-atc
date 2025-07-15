"""
跑道。
"""

import math

from pygame import Vector2

from atc.config_cls import _Rwy
from atc.const import RESOLUTION, RWY_LENGTH


class Rwy:
    """
    跑道。
    """

    pos1: Vector2
    """起点位置。"""
    num: str
    """跑道编号。"""
    num_rev: str
    """对向跑道编号。"""
    direction: int
    """磁方位角。"""
    suffix: str
    """后缀。"""

    @property
    def direction_geo(self) -> float:
        """几何角度，弧度制。"""
        return math.radians(self.direction - 90)

    @property
    def pos2(self) -> Vector2:
        """终点位置。"""
        return Vector2(
            self.pos1[0] + RWY_LENGTH * math.cos(self.direction_geo),
            self.pos1[1] + RWY_LENGTH * math.sin(self.direction_geo),
        )

    @property
    def suffix_zh(self) -> str:
        """中文的后缀，即 “左”、“右” 或 “中”。"""
        return {"L": "左", "R": "右", "C": "中"}.get(self.suffix, "")

    def __init__(self, rwy: _Rwy) -> None:
        self.pos1 = Vector2(
            rwy["position"][0] * RESOLUTION[0],
            rwy["position"][1] * RESOLUTION[1],
        )
        self.num, self.num_rev = self._get_rwy_num(rwy)
        self.direction = rwy["direction"]
        self.suffix = rwy["suffix"]

    def _get_rwy_num(self, rwy: _Rwy):
        """
        获取跑道两端编号。
        """
        # 屎山别喷哈哈哈哈哈
        direction = round(rwy["direction"] / 10)
        return (
            str(direction) + rwy["suffix"],
            str(direction + (18 if direction <= 18 else -18))
            + rwy["suffix"].replace("L", "_").replace("R", "L").replace("_", "R"),
        )
