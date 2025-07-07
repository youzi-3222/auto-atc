"""
航班相关信息。
"""

import random
from dataclasses import dataclass

from atc.core.scene.aircraft.aircraft_type import AIRCRAFT_TYPE
from atc.core.scene.aircraft.airline import AIRLINE
from atc.core.scene.aircraft.wake import Wake


@dataclass
class FlightInfo:
    """
    只读的航班信息，这些信息在航班过程中不会改变。
    """

    ssr_code: str
    """SSR 代码（应答机编码）。"""
    airline: str
    """航空公司二字代码。"""
    raw_flight_no: str
    """不带航司的航班号。"""
    arrival: bool
    """是否为进场飞机。"""
    rwy: str
    """起降跑道。"""
    aircraft_type: str
    """飞机类型。"""
    wake: Wake
    """尾流类型。"""

    @property
    def flight_no(self) -> str:
        """航班号（航空公司二字代码 + 航班号数字）。"""
        return f"{self.airline}{self.raw_flight_no}"

    @property
    def airline_callsign(self) -> str:
        """航空公司的呼号。"""
        return AIRLINE.get(self.airline, self.airline)

    @property
    def chinese(self) -> bool:
        """是否可以使用中文管制。"""
        return not self.airline_callsign.isascii()

    @staticmethod
    def random(arrival: bool, rwys: list[str]):
        """
        生成一个随机的航班信息。
        """
        ssr_code = oct(random.randint(0o0, 0o6777))[2:].zfill(4)
        airline = random.choice(list(AIRLINE.keys()))
        raw_flight_no = str(random.randint(100, 9999)).zfill(4)
        rwy = random.choice(rwys)
        aircraft_type = random.choice(AIRCRAFT_TYPE)
        wake = random.choices(
            [Wake.LIGHT, Wake.MEDIUM, Wake.HEAVY], weights=[0.5, 0.3, 0.2]
        )[0]
        return FlightInfo(
            ssr_code, airline, raw_flight_no, arrival, rwy, aircraft_type, wake
        )
