import pytest

from src.atc.core.scene.aircraft.flight_info import FlightInfo
from src.atc.core.scene.aircraft.wake import Wake
from src.atc.core.scene.instruction import Instruction


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "flight": FlightInfo(
                    6760, "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": 175,
                "turn_left": True,
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
                "clear_app_rwy": "18L",
            },
            "IR655, turn left heading one seven fife, reduce speed one eight zero, descend to tree zero, cleared ILS runway one eight left.",
        ),
        (
            {
                "flight": FlightInfo(
                    7700, "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 6000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": None,
                "alt_ft": 4000,
                "clear_app_rwy": None,
            },
            "四川八六三三，直飞 MIKOS，下高度幺两。",
        ),
        (
            {
                "flight": FlightInfo(
                    7700, "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 4000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": 230,
                "alt_ft": 4000,
                "clear_app_rwy": None,
            },
            "四川八六三三，直飞 MIKOS。",
        ),
    ],
)
def test_instruction_speech(kwargs, expected):
    instr = Instruction(**kwargs)
    assert instr.speech == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "flight": FlightInfo(
                    6760, "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": 175,
                "turn_left": True,
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
                "clear_app_rwy": "18L",
            },
            "IR655, turn left heading 175, reduce speed 180, descend to 3000 feet, cleared ILS runway 18L.",
        ),
        (
            {
                "flight": FlightInfo(
                    7700, "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 6000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": None,
                "alt_ft": 4000,
                "clear_app_rwy": None,
            },
            "3U8633，直飞 MIKOS，下高度 1200 米。",
        ),
        (
            {
                "flight": FlightInfo(
                    7700, "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 4000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": 230,
                "alt_ft": 4000,
                "clear_app_rwy": None,
            },
            "3U8633，直飞 MIKOS。",
        ),
    ],
)
def test_instruction_text(kwargs, expected):
    instr = Instruction(**kwargs)
    assert instr.text == expected
