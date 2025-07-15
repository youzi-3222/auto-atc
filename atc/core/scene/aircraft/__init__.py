"""
航班。
"""

import math
from datetime import datetime, timedelta

from pygame import Vector2

from atc import config
from atc.core.scene.instruction import Instruction
from atc.core.scene.waypoint import WayPoint

from .aircraft_state import AircraftState
from .aircraft_type import AIRCRAFT_TYPE
from .airline import AIRLINE
from .flight_info import FlightInfo
from .wake import Wake


class Aircraft:
    """
    航班。
    """

    pos: Vector2
    """位置。"""
    heading: int
    """航向。"""
    target_heading: int
    """目标航向。"""
    turn_left: bool
    """是否左转。"""
    alt_ft: int
    """高度，英尺。"""
    target_alt_ft: int
    """目标高度，英尺。"""
    speed_kt: int
    """速度，节。"""
    target_speed_kt: int
    """目标速度，节。"""
    climb_rate: int
    """爬升率，英尺 / 分钟。"""
    waypoint: list[WayPoint]
    """计划经过的航路点列表。"""
    clear_app: bool = False
    """是否可以进近。"""

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
        return math.radians(self.heading - 90)

    def __init__(
        self,
        flight: FlightInfo,
        pos: Vector2,
        waypoint: list[str],
        alt_ft: int,
        speed_kt: int,
    ) -> None:
        # rwy_list = []
        # for r in [Rwy(r) for r in rwy]:
        #     rwy_list.append(r.num)
        #     rwy_list.append(r.num_rev)
        # self.flight = FlightInfo.random(arrival, rwy_list)
        self.flight = flight
        self.pos = pos
        self.waypoint = [WayPoint(w) for w in waypoint]
        self.alt_ft = alt_ft
        self.speed_kt = speed_kt

        self.turn_left = False
        delta = self.waypoint[0].pos - self.pos
        self.heading = round(math.degrees(math.atan2(delta.x, -delta.y)) % 360)
        self.target_heading = self.heading
        self.target_alt_ft = self.alt_ft
        self.target_speed_kt = self.speed_kt
        self.climb_rate = 0

        self.last_update_time = datetime.now()

    def instruct(self, inst: Instruction) -> None:
        """
        向航班下达管制指令。
        """
        if inst.heading is not None:
            self.target_heading = inst.heading
            self.waypoint = []  # 都直飞航向了，自然不会用导航点导航
        if inst.turn_left is not None:
            self.turn_left = inst.turn_left
        if inst.vector_to is not None:
            self.waypoint = [WayPoint(config["waypoint"][x]) for x in inst.vector_to]
        if inst.speed_kt is not None:
            self.target_speed_kt = inst.speed_kt
        if inst.alt_ft is not None:
            self.target_alt_ft = inst.alt_ft
        if inst.clear_app:
            self.clear_app = True
        if inst.go_around:
            self.clear_app = False

    def update(self, delta_time: timedelta) -> None:
        """
        根据提供的 `delta_time`，更新航班状态。会修改航班对象。
        """
        dt = delta_time.total_seconds()

        # 计算目标高度差
        alt_diff = self.target_alt_ft - self.alt_ft

        # 确定最大爬升率限制
        max_rate = 2500 if self.target_alt_ft >= 4000 else 1200

        # 计算理想爬升率（与高度差成正比，在接近目标时减小）
        desired_rate = max(-max_rate, min(max_rate, alt_diff * 0.5))

        # 限制爬升率变化加速度（不超过 200 ft / min / s）
        max_rate_change = 200 * dt  # 最大允许变化量
        rate_change = desired_rate - self.climb_rate
        rate_change = max(-max_rate_change, min(max_rate_change, rate_change))
        self.climb_rate += round(rate_change)

        # 计算高度变化
        delta_alt = self.climb_rate * dt / 60

        # 更新高度
        self.alt_ft = round(self.alt_ft + delta_alt)

        # 确保不会超过目标高度（防止因惯性过冲）
        if (alt_diff > 0 and self.alt_ft > self.target_alt_ft) or (
            alt_diff < 0 and self.alt_ft < self.target_alt_ft
        ):
            self.alt_ft = self.target_alt_ft
            self.climb_rate = 0  # 到达目标高度后停止爬升 / 下降

        # 更新速度
        delta_speed = 5 * dt
        if self.speed_kt < self.target_speed_kt:
            self.speed_kt = round(
                min(self.speed_kt + delta_speed, self.target_speed_kt)
            )
        else:
            self.speed_kt = round(
                max(self.speed_kt - delta_speed, self.target_speed_kt)
            )

        # 更新航向
        delta_heading = 3 * dt

        if abs(self.target_heading - self.heading) <= delta_heading:
            self.heading = self.target_heading
        else:
            self.heading = round(
                (self.heading + (-1 if self.turn_left else 1) * delta_heading) % 360
            )

        # 更新位置
        self.pos += (
            Vector2(math.cos(self.heading_geo), math.sin(self.heading_geo))
            * self.speed_kt
            * config["nm_per_pixel"]
            * dt
        )

        # 如果有航路点，更新目标航向
        if self.waypoint:
            delta = self.waypoint[0].pos - self.pos
            if delta.length_squared() > 100:  # 到达航路点的阈值
                self.target_heading = round(
                    math.degrees(math.atan2(delta.x, -delta.y)) % 360
                )
            else:
                self.waypoint.pop(0)  # 移除已到达的航路点
                if self.waypoint:
                    delta = self.waypoint[0].pos - self.pos
                    self.target_heading = round(
                        math.degrees(math.atan2(delta.x, -delta.y)) % 360
                    )


__all__ = [
    "Aircraft",
    "AIRLINE",
    "AIRCRAFT_TYPE",
    "AircraftState",
    "FlightInfo",
    "Wake",
]
