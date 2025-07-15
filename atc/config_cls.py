"""
配置。
"""

from enum import Enum
from typing import TypedDict


class RwyUsage(Enum):
    """
    跑道用途。
    """

    CLSD = 0
    ARRIVAL = 1
    DEPARTURE = 2
    BOTH = 3


class _Rwy(TypedDict):
    """
    跑道配置。
    """

    direction: int
    suffix: str
    position: list[float]


class WayPointUsage(Enum):
    """
    航路点用途。
    """

    NONE = 0
    ARRIVAL = 1
    DEPARTURE = 2


class _WayPoint(TypedDict):
    """
    航路点配置。
    """

    name: str
    position: list[float]
    usage: WayPointUsage


class Config(TypedDict):
    """
    配置文件。
    """

    icao: str
    rwy: list[_Rwy]
    rwy_usage: dict[str, RwyUsage]
    waypoint: dict[str, _WayPoint]
    std_arr: dict[str, list[str]]
    std_dep: dict[str, list[str]]
    arr_freq: float
    dep_freq: float
    nm_per_pixel: float
