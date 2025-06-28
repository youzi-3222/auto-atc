"""
场景。
"""

from datetime import datetime, timedelta

from src.atc.config import config

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
    aircraft: dict[str, Aircraft]
    """航班号及对应航班列表。"""
    last_arr: datetime
    """上一次生成进场航班的时刻。"""
    last_dep: datetime
    """上一次生成离场航班的时刻。"""
    weather: Weather
    """天气。"""

    def __init__(self) -> None:
        self.rwy = [Rwy(rwy) for rwy in config["rwy"]]
        self.waypoint = [WayPoint(wp) for wp in config["waypoint"]]
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
        if datetime.now() - self.last_arr > timedelta(seconds=60 / config["arr_freq"]):
            aircraft = Aircraft()
            self.aircraft[aircraft.flight.flight_no] = aircraft
            self.last_arr = datetime.now()
        raise NotImplementedError
