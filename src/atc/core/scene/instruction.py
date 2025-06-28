"""
管制指令。
"""

from dataclasses import dataclass
from typing import Optional

from .aircraft.flight_info import FlightInfo


@dataclass
class Instruction:
    """
    对特定航班的管制指令。
    """

    flight: FlightInfo
    """航班信息。"""
    heading: Optional[int]
    """航向。"""
    turn_left: Optional[bool]
    """是否左转。"""
    vector_to: Optional[list[str]]
    """直飞航路点。"""
    speed_kt: Optional[int]
    """速度，节。"""
    height_ft: Optional[int]
    """放行高度，节。"""
    clear_app_rwy: Optional[str]
    """允许进近的跑道编号。"""
    go_around: bool = False
    """是否为复飞指令，默认为 False。"""

    def __post_init__(self) -> None:
        assert (self.heading is None) == (
            self.turn_left is None
        ), "航向与转向方向必须同时存在"
        assert (
            self.heading is not None or self.vector_to is not None
        ), "航向与直飞航路点不能同时存在"
        assert not (
            self.go_around and self.clear_app_rwy is not None
        ), "复飞指令不能允许进近"

    @property
    def text(self) -> str:
        """
        读取能被直接输出的文本。
        """
        return self._text_ch() if self.flight.chinese else self._text_en()

    def _text_ch(self):
        result = [self.flight.flight_no]
        if self.go_around:
            result.append("复飞")
        if self.heading is not None:
            assert self.turn_left is not None
            result.append(f"{'左转' if self.turn_left else '右转'}航向 {self.heading}")
        if self.vector_to is not None:
            result.append(f"直飞 {' '.join(self.vector_to)}")
        if self.speed_kt is not None:
            result.append(f"速度 {self.speed_kt}")
        if self.height_ft is not None:
            result.append(f"高度 {self.height_ft}")
        if self.clear_app_rwy is not None:
            result.append(f"ILS 进近跑道 {self.clear_app_rwy}")
        return "，".join(result) + "。"

    def _text_en(self):
        result = [self.flight.flight_no]
        if self.go_around:
            result.append("go around")
        if self.heading is not None:
            assert self.turn_left is not None
            result.append(
                ("turn left heading" if self.turn_left else "turn right heading")
                + f" {self.heading:03d}"
            )
        if self.vector_to is not None:
            result.append(f"vector to {' '.join(self.vector_to)}")
        if self.speed_kt is not None:
            result.append(f"speed {self.speed_kt}")
        if self.height_ft is not None:
            result.append(f"altitude {self.height_ft}")
        if self.clear_app_rwy is not None:
            result.append(f"cleared ILS runway {self.clear_app_rwy}")
        return ", ".join(result) + "."

    @property
    def spoken(self) -> str:
        """
        读取能被直接朗读的语音。
        """
        return self._spoken_ch() if self.flight.chinese else self._spoken_en()

    def _spoken_ch(self):
        pass

    def _spoken_en(self):
        pass
