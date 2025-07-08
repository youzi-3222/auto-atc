"""
场景。
"""

from datetime import datetime, timedelta

from atc.config import _Rwy, _WayPoint

from .aircraft import Aircraft
from .route import Route
from .rwy import Rwy
from .waypoint import WayPoint
from .weather import Weather


class Scene:
    """
    场景。
    """

    rwy: list[Rwy]
    """跑道列表。"""
    waypoint: list[WayPoint]
    """航路点列表。"""
    route: list[Route]
    """航路列表。"""
    arr_freq: float
    """进场航班生成频率，单位为每分钟航班数。"""
    dep_freq: float
    """离场航班生成频率，单位为每分钟航班数。"""

    aircraft: dict[str, Aircraft]
    """航班号及对应航班列表。"""
    last_arr: datetime
    """上一次生成进场航班的时刻。"""
    last_dep: datetime
    """上一次生成离场航班的时刻。"""
    weather: Weather
    """天气。"""

    def __init__(
        self,
        rwy: list[_Rwy],
        waypoint: list[_WayPoint],
        arr_freq: float,
        dep_freq: float,
    ) -> None:
        self.rwy = [Rwy(r) for r in rwy]
        self.waypoint = [WayPoint(w) for w in waypoint]
        raise NotImplementedError

    def run_tick(self):
        """
        运行一帧。
        """
        raise NotImplementedError

    def _generate_aircraft(self):
        """
        生成新航班。
        """
        if datetime.now() - self.last_arr > timedelta(seconds=60 / self.arr_freq):
            aircraft = Aircraft()
            self.aircraft[aircraft.flight.flight_no] = aircraft
            self.last_arr = datetime.now()
        raise NotImplementedError
