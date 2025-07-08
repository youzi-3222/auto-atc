"""
航班。
"""

import math
from datetime import datetime, timedelta
from typing import Union, overload

from pygame import Vector2
from sympy import Symbol

from atc.config import _Rwy
from atc.core.scene.instruction import Instruction
from atc.core.scene.route import Route
from atc.core.scene.rwy import Rwy
from atc.core.scene.waypoint import WayPoint

from .airline import AIRLINE
from .flight_info import FlightInfo


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
    climb_rate: int
    """爬升率，英尺 / 分钟。"""
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
        """航空公司的呼号。"""
        return self.flight.airline_callsign

    @property
    def chinese(self) -> bool:
        """是否可以使用中文管制。"""
        return self.flight.chinese

    @property
    def heading_geo(self) -> float:
        """航向角，弧度制。"""
        return math.radians(self.heading)

    def __init__(
        self,
        flight: FlightInfo,
        pos: Vector2,
        waypoint: list[WayPoint],
        height_ft: int,
        speed_kt: int,
    ) -> None:
        # rwy_list = []
        # for r in [Rwy(r) for r in rwy]:
        #     rwy_list.append(r.num)
        #     rwy_list.append(r.num_rev)
        # self.flight = FlightInfo.random(arrival, rwy_list)
        self.flight = flight
        self.pos = pos
        self.waypoint = waypoint
        self.height_ft = height_ft
        self.speed_kt = speed_kt

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
