import pytest
from src.atc.core.scene.instruction import Instruction


# Mock FlightInfo with only flight_no attribute
class MockFlightInfo:
    def __init__(self, flight_no):
        self.flight_no = flight_no


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "flight": MockFlightInfo("ABC123"),
                "heading": 270,
                "turn_left": True,
                "vector_to": None,
                "speed_kt": 180,
                "height_ft": 3000,
                "clear_app_rwy": "18L",
            },
            "ABC123，左转航向 270，速度 180，高度 3000，跑道 18L 可以进近。",
        ),
        (
            {
                "flight": MockFlightInfo("DEF456"),
                "heading": 90,
                "turn_left": False,
                "vector_to": None,
                "speed_kt": None,
                "height_ft": None,
                "clear_app_rwy": None,
            },
            "DEF456，右转航向 090。",
        ),
        (
            {
                "flight": MockFlightInfo("GHI789"),
                "heading": None,
                "turn_left": None,
                "vector_to": ["WPT3"],
                "speed_kt": 200,
                "height_ft": None,
                "clear_app_rwy": "36R",
            },
            "GHI789，直飞 WPT3，速度 200，跑道 36R 可以进近。",
        ),
        (
            {
                "flight": MockFlightInfo("JKL012"),
                "heading": None,
                "turn_left": None,
                "vector_to": None,
                "speed_kt": None,
                "height_ft": None,
                "clear_app_rwy": None,
            },
            "JKL012。",
        ),
        (
            {
                "flight": MockFlightInfo("MNO345"),
                "heading": None,
                "turn_left": None,
                "vector_to": ["WPT4"],
                "speed_kt": None,
                "height_ft": 5000,
                "clear_app_rwy": None,
            },
            "MNO345，直飞 WPT4，高度 5000。",
        ),
    ],
)
def test_instruction_text(kwargs, expected):
    instr = Instruction(**kwargs)
    assert instr.text == expected
