"""
管制指令。
"""

from dataclasses import dataclass
from typing import Optional

from src.atc.core.speech import Speech

from .aircraft.flight_info import FlightInfo


@dataclass
class Instruction:
    """
    对特定航班的管制指令。
    """

    flight: FlightInfo
    """航班信息。"""
    speed_old_kt: int
    """旧的速度，节。"""
    alt_old_ft: int
    """旧的高度，英尺。"""
    use_m: bool
    """是否使用米作为高度单位。"""
    heading: Optional[int]
    """航向。"""
    turn_left: Optional[bool]
    """是否左转。"""
    vector_to: Optional[list[str]]
    """直飞航路点。"""
    speed_kt: Optional[int]
    """速度，节。"""
    alt_ft: Optional[int]
    """放行高度，英尺。"""
    clear_app_rwy: Optional[str]
    """允许进近的跑道编号。"""
    go_around: bool = False
    """是否为复飞指令，默认为 False。"""

    def __post_init__(self) -> None:
        assert (self.heading is None) == (
            self.turn_left is None
        ), "航向与转向方向必须同时存在"
        assert (
            self.heading is None or self.vector_to is None
        ), "航向与直飞航路点不能同时存在"
        assert not (
            self.go_around and self.clear_app_rwy is not None
        ), "复飞指令不能允许进近"
        if self.speed_kt == self.speed_old_kt:
            self.speed_kt = None
        if self.alt_ft == self.alt_old_ft:
            self.alt_ft = None

    def _ft2m(self, ft: int) -> int:
        """
        将英尺转换为米。
        """
        return int(ft * 0.3048)

    @property
    def text(self) -> str:
        """
        读取能被直接输出的文本。
        """
        return self._text_zh() if self.flight.chinese else self._text_en()

    def _text_zh(self):
        result = [self.flight.flight_no]
        if self.go_around:
            result.append("复飞")
        if self.heading is not None:
            assert self.turn_left is not None
            result.append(
                f"{'左转' if self.turn_left else '右转'}航向 {self.heading:03d}"
            )
        if self.vector_to is not None:
            result.append(f"直飞 {' '.join(self.vector_to)}")
        if self.speed_kt is not None:
            result.append(
                f"{'减速' if self.speed_old_kt > self.speed_kt else '加速'} {self.speed_kt}"
            )
        if self.alt_ft is not None:
            result.append(
                f"{'下' if self.alt_old_ft > self.alt_ft else '上'}高度 "
                f"{round(self._ft2m(self.alt_ft) if self.use_m else self.alt_ft, -2)} "
                f"{'米' if self.use_m else '英尺'}"
            )
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
            result.append(
                f"{'reduce' if self.speed_old_kt > self.speed_kt else 'increase'} "
                f"speed {self.speed_kt}"
            )
        if self.alt_ft is not None:
            result.append(
                f"{'descend' if self.alt_old_ft > self.alt_ft else 'climb'} to "
                f"{self._ft2m(self.alt_ft) if self.use_m else self.alt_ft} "
                f"{'meters' if self.use_m else 'feet'}"
            )
        if self.clear_app_rwy is not None:
            result.append(f"cleared ILS runway {self.clear_app_rwy}")
        return ", ".join(result) + "."

    @property
    def speech(self) -> str:
        """
        读取能被直接朗读的语音。
        """
        return self._speech_zh() if self.flight.chinese else self._speech_en()

    def _speech_zh(self) -> str:
        result = [
            self.flight.airline_callsign + Speech.explain_zh(self.flight.raw_flight_no)
        ]
        if self.go_around:
            result.append("复飞")
        if self.heading is not None:
            assert self.turn_left is not None
            result.append(
                f"{'左转' if self.turn_left else '右转'}航向"
                f"{Speech.explain_zh(str(self.heading).zfill(3))}"
            )
        if self.vector_to is not None:
            result.append(f"直飞 {' '.join(self.vector_to)}")
        if self.speed_kt is not None:
            result.append(
                f"{'减速' if self.speed_old_kt > self.speed_kt else '加速'}"
                f"{Speech.explain_zh(self.speed_kt)}"
            )
        if self.alt_ft is not None:
            alt = str(
                round((self._ft2m(self.alt_ft) if self.use_m else self.alt_ft) / 100)
            ).zfill(2)
            result.append(
                f"{'下' if self.alt_old_ft > self.alt_ft else '上'}高度{Speech.explain_zh(alt)}"
            )
        if self.clear_app_rwy is not None:
            result.append(f"ILS 进近跑道 {Speech.explain_rwy_zh(self.clear_app_rwy)}")
        return "，".join(result) + "。"

    def _speech_en(self) -> str:
        result = [
            self.flight.airline_callsign
            + " "
            + Speech.explain_en(self.flight.raw_flight_no)
        ]
        if self.go_around:
            result.append("go around")
        if self.heading is not None:
            assert self.turn_left is not None
            result.append(
                ("turn left heading" if self.turn_left else "turn right heading")
                + f" {Speech.explain_en(str(self.heading).zfill(3))}"
            )
        if self.vector_to is not None:
            result.append(f"vector to {' '.join(self.vector_to)}")
        if self.speed_kt is not None:
            result.append(
                f"{'reduce' if self.speed_old_kt > self.speed_kt else 'increase'} "
                f"speed {Speech.explain_en(self.speed_kt)}"
            )
        if self.alt_ft is not None:
            alt = round((self._ft2m(self.alt_ft) if self.use_m else self.alt_ft) / 100)
            result.append(
                f"{'descend' if self.alt_old_ft > self.alt_ft else 'climb'} to "
                f"{Speech.explain_en(alt)}"
            )
        if self.clear_app_rwy is not None:
            result.append(
                f"cleared ILS runway {Speech.explain_rwy_en(self.clear_app_rwy)}"
            )
        return ", ".join(result) + "."
