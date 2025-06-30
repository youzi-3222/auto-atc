"""
航班相关信息。
"""

from dataclasses import dataclass

from src.atc.core.scene.aircraft.airline import AIRLINE
from src.atc.core.scene.aircraft.wake import Wake


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
