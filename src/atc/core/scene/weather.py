"""
天气。
"""

# https://aviationweather.gov/data/metar/?decoded=1&ids=ZGGG&taf=1
# https://aviationweather.gov/api/data/metar?ids=ZSPD&hours=0&order=id%2C-obs&format=json&fltcat=true
# https://aviationweather.gov/data/api/#api

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from threading import Thread

import requests


class CloudType(Enum):
    """
    云层类型。
    """

    CAVOK = "CAVOK"
    """无云。"""
    FEW = "FEW"
    """少量云。"""
    SCT = "SCT"
    """散布云。"""
    BKN = "BKN"
    """破碎云。"""
    OVC = "OVC"
    """覆盖云。"""


@dataclass
class Cloud:
    """
    云层。
    """

    cloud_type: CloudType
    """云层类型。"""
    height_ft: int
    """云层高度，英尺。"""

    def __post_init__(self):
        assert isinstance(self.cloud_type, CloudType), "云层类型必须是 CloudType 枚举"
        assert (
            isinstance(self.height_ft, int) and self.height_ft >= 0
        ), "云层高度必须是非负整数"

    def height_level(self) -> int:
        """
        获取云层所在高度层。
        """
        return round(self.height_ft / 100)

    def __str__(self) -> str:
        return f"{self.cloud_type.value}{self.height_ft}"


class Weather:
    """
    天气。

    会创建一个线程，以定时刷新天气信息。
    """

    icao: str
    """机场 ICAO 代码。"""
    raw: str
    """原始 METAR 气象报文。"""
    time: datetime
    """报文时间。"""
    temp_c: int
    """气温，摄氏度。"""
    dewpoint_c: int
    """露点温度，摄氏度。"""
    qnh_hpa: int
    """修正海平面气压，百帕。"""
    wind_dir: int
    """风向，角度制。"""
    wind_speed_kt: int
    """风速，节。"""
    cloud: list[Cloud]
    """云层列表。"""
    name: str
    """机场全称。"""

    refresh_time: datetime
    """刷新时间。"""
    refresh_thread: Thread
    """刷新线程。"""

    running: bool = True
    """是否正在运行。"""

    def __init__(self, icao: str) -> None:
        self.icao = icao
        self._get_from_web()

    def _get_from_web(self):
        json_resp = requests.get(
            f"https://aviationweather.gov/api/data/metar?ids={self.icao}"
            "&format=json&fltcat=true",
            timeout=20,
        )
        assert json_resp.ok, f"获取天气信息失败（{json_resp.status_code}）"
        json_raw = json_resp.json()
        assert isinstance(json_raw, list), "未获取到有效的天气信息"
        assert len(json_raw) > 0, "未获取到有效的天气信息"
        json_raw = json_raw[0]
        assert isinstance(json_raw, dict), "未获取到有效的天气信息"

        self.raw = json_raw["rawOb"]

        self.time = datetime.strptime(json_raw["reportTime"], "%Y-%m-%d %H:%M:%S")

        self.temp_c = json_raw["temp"]
        assert isinstance(self.temp_c, int), "气温数据格式错误"

        self.dewpoint_c = json_raw["dewp"]
        assert isinstance(self.dewpoint_c, int), "露点温度数据格式错误"

        self.qnh_hpa = json_raw["altim"]
        assert isinstance(self.qnh_hpa, int), "气压数据格式错误"

        self.wind_dir = json_raw["wdir"]
        assert isinstance(self.wind_dir, int), "风向数据格式错误"
        assert 0 <= self.wind_dir <= 360, f"风向数据格式错误：收到 {self.wind_dir}"

        self.wind_speed_kt = json_raw["wspd"]
        assert isinstance(self.wind_speed_kt, int), "风速数据格式错误"

        assert isinstance(cloud_list := json_raw["clouds"], list), "云层数据格式错误"
        self.cloud = []
        for cloud in cloud_list:
            assert isinstance(cloud, dict), "云层数据格式错误"
            assert "cover" in cloud and "base" in cloud, "云层数据格式错误"
            self.cloud.append(Cloud(CloudType(cloud["cover"]), cloud["base"]))

        self.name = json_raw["name"]
