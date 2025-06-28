"""
天气。
"""

# https://aviationweather.gov/data/metar/?decoded=1&ids=ZGGG&taf=1
# https://aviationweather.gov/api/data/metar?ids=ZSPD&hours=0&order=id%2C-obs&format=json&fltcat=true
# https://aviationweather.gov/data/api/#api

from datetime import datetime
from threading import Thread


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
    """温度，摄氏度。"""
    dewpoint_c: int
    """露点温度，摄氏度。"""
    qnh_hpa: int
    """修正海平面气压，百帕。"""
    wind_dir: int
    """风向，角度制。"""
    wind_speed_kt: int
    """风速，节。"""
    visibility_mi: int
    """能见度，英里。"""

    refresh_time: datetime
    """刷新时间。"""
    refresh_thread: Thread
    """刷新线程。"""

    running: bool = True
    """是否正在运行。"""

    def __init__(self, icao: str) -> None:
        self.icao = icao
        raise NotImplementedError

    def __init_thread__(self):
        self.refresh_thread = Thread(target=self._refresh_thread)
        self.refresh_thread.start()

    def end_thread(self):
        """
        结束线程。
        """
        self.running = False
        if self.refresh_thread:
            self.refresh_thread.join()

    def _refresh_thread(self):
        raise NotImplementedError

    def _get_from_web(self):
        raise NotImplementedError
