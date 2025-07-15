import pytest

from atc.core.scene.aircraft.flight_info import FlightInfo
from atc.core.scene.aircraft.wake import Wake
from atc.core.scene.instruction import Instruction


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "flight": FlightInfo(
                    "6760", "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": 175,
                "turn_left": True,
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
                "clear_app": True,
            },
            "Iran Air six fife fife, turn left heading one seven fife, reduce speed one eight zero, descend to tree zero, cleared ILS runway one eight left.",
        ),
        (
            {
                "flight": FlightInfo(
                    "3674", "AF", "296Q", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": None,
                "turn_left": None,
                "vector_to": None,
                "speed_kt": 250,
                "alt_ft": 3000,
                "clear_app": False,
            },
            "Air France two niner six quebec, descend to tree zero.",
        ),
        (
            {
                "flight": FlightInfo(
                    "7700", "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 6000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": None,
                "alt_ft": 4000,
                "clear_app": False,
            },
            "四川八六三三，直飞 MIKOS，下高度幺两。",
        ),
        (
            {
                "flight": FlightInfo(
                    "7700", "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 4000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": 230,
                "alt_ft": 4000,
                "clear_app": False,
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
                    "6760", "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": 175,
                "turn_left": True,
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
                "clear_app": True,
            },
            "IR655, turn left heading 175, reduce speed 180, descend to 3000 feet, cleared ILS runway 18L.",
        ),
        (
            {
                "flight": FlightInfo(
                    "3674", "AF", "296Q", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": None,
                "turn_left": None,
                "vector_to": None,
                "speed_kt": 250,
                "alt_ft": 4000,
                "clear_app": False,
            },
            "AF296Q, descend to 4000 feet.",
        ),
        (
            {
                "flight": FlightInfo(
                    "7700", "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 6000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": None,
                "alt_ft": 4000,
                "clear_app": False,
            },
            "3U8633，直飞 MIKOS，下高度 1200 米。",
        ),
        (
            {
                "flight": FlightInfo(
                    "7700", "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 230,
                "alt_old_ft": 4000,
                "use_m": True,
                "heading": None,
                "turn_left": None,
                "vector_to": ["MIKOS"],
                "speed_kt": 230,
                "alt_ft": 4000,
            },
            "3U8633，直飞 MIKOS。",
        ),
    ],
)
def test_instruction_text(kwargs, expected):
    instr = Instruction(**kwargs)
    assert instr.text == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "flight": FlightInfo(
                    "6760", "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": 175,
                "turn_left": None,  # AssertionError expected
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
            },
            "航向与转向方向必须同时存在",
        ),
        (
            {
                "flight": FlightInfo(
                    "3674", "AF", "296Q", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": False,
                "heading": None,
                "turn_left": True,  # AssertionError expected
                "vector_to": None,
                "speed_kt": 180,
                "alt_ft": 3000,
            },
            "航向与转向方向必须同时存在",
        ),
        (
            {
                "flight": FlightInfo(
                    "3435", "3U", "8633", True, "02R", "A319", Wake.LIGHT
                ),
                "speed_old_kt": 250,
                "alt_old_ft": 5000,
                "use_m": True,
                "heading": 360,
                "turn_left": True,
                "vector_to": ["MIKOS"],
                "speed_kt": 180,
                "alt_ft": 3000,
                "clear_app": True,
            },
            "航向与直飞航路点不能同时存在",
        ),
        (
            {
                "flight": FlightInfo(
                    "6760", "IR", "655", True, "18L", "A30B", Wake.LIGHT
                ),
                "speed_old_kt": 180,
                "alt_old_ft": 500,
                "use_m": False,
                "heading": None,
                "turn_left": None,
                "vector_to": None,
                "speed_kt": 250,
                "alt_ft": 3000,
                "clear_app": True,
                "go_around": True,  # AssertionError expected
            },
            "复飞指令不能允许进近",
        ),
    ],
)
def test_instruction_failed(kwargs, expected):
    with pytest.raises(AssertionError, match=expected):
        Instruction(**kwargs)
