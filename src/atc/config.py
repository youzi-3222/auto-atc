"""
配置。
"""

import json
from enum import Enum
from typing import TypedDict

from src.atc.const import CONFIG_PATH


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


class _Config(TypedDict):
    """
    配置文件。
    """

    icao: str
    rwy: list[_Rwy]
    rwy_usage: dict[str, RwyUsage]
    waypoint: list[_WayPoint]
    std_arr: dict[str, list[str]]
    std_dep: dict[str, list[str]]
    arr_freq: float
    dep_freq: float


with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config: _Config = json.load(f)
