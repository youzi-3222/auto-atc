"""
航班。
"""

import math
from datetime import datetime, timedelta
from typing import Union, overload

from pygame import Vector2
from sympy import Symbol

from src.atc.core.scene.aircraft.airline import AIRLINE
from src.atc.core.scene.aircraft.flight_info import FlightInfo
from src.atc.core.scene.instruction import Instruction
from src.atc.core.scene.route import Route
from src.atc.core.scene.waypoint import WayPoint


class Aircraft:
    """
    航班。
    """

    pos: Vector2
    """位置。"""
    heading: int
    """航向。"""
    height_ft: int
    """高度，英尺。"""
    allow_height_ft: int
    """放行高度，英尺。"""
    speed_kt: int
    """速度，节。"""
    route: Route
    """航班所在的航路。"""
    waypoint: list[WayPoint]
    """计划经过的航路点列表。"""

    flight: FlightInfo
    """航班信息。"""

    last_update_time: datetime
    """上次更新时间。"""

    @property
    def airline_callsign(self) -> str:
        """航空公司的友好输出（中文简称 / 英文简称）。"""
        return self.flight.airline_callsign

    @property
    def chinese(self) -> bool:
        """是否可以使用中文管制。"""
        return self.flight.chinese

    @property
    def heading_geo(self) -> float:
        """航向角，弧度制。"""
        return math.radians(self.heading)

    def __init__(self, arrival: bool = False) -> None:
        self.arrival = arrival
        raise NotImplementedError

    def __init_random__(self) -> None:
        raise NotImplementedError

    def instruct(self, instruction: Instruction) -> None:
        """
        向航班下达管制指令。
        """
        raise NotImplementedError

    def update(self) -> None:
        """
        根据当前系统时间，更新航班状态。会修改航班对象。
        """
        raise NotImplementedError

    @overload
    def simulate(self, dt: Symbol) -> "Aircraft": ...
    @overload
    def simulate(self, dt: timedelta) -> "Aircraft": ...
    def simulate(self, dt: Union[Symbol, timedelta]) -> "Aircraft":
        """
        用 `dt` 表示经过了 `dt` 秒后的航班状态。

        `dt` 可以是未知数 `Symbol` 或 `timedelta`。

        不会修改航班对象。
        """
        if isinstance(dt, Symbol):
            raise NotImplementedError
        elif isinstance(dt, timedelta):
            raise NotImplementedError

    def _simulate_symbol(self, dt: Symbol) -> "Aircraft":
        raise NotImplementedError
