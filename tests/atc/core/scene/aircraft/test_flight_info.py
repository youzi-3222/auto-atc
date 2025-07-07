import pytest

from atc.core.scene.aircraft.flight_info import FlightInfo
from atc.core.scene.aircraft.wake import Wake


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "ssr_code": 3427,
                "airline": "CZ",
                "raw_flight_no": "328",
                "arrival": True,
                "rwy": "20R",
                "aircraft_type": "A380",
                "wake": Wake.HEAVY,
            },
            "CZ328",
        ),
        (
            {
                "ssr_code": 7700,
                "airline": "AI",
                "raw_flight_no": "171",
                "arrival": False,
                "rwy": "23",
                "aircraft_type": "B789",
                "wake": Wake.HEAVY,
            },
            "AI171",
        ),
    ],
)
def test_flight_info_flight_no(kwargs, expected):
    flight_info = FlightInfo(**kwargs)
    assert flight_info.flight_no == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "ssr_code": 3427,
                "airline": "CZ",
                "raw_flight_no": "328",
                "arrival": True,
                "rwy": "20R",
                "aircraft_type": "A380",
                "wake": Wake.HEAVY,
            },
            "南航",
        ),
        (
            {
                "ssr_code": 7700,
                "airline": "AI",
                "raw_flight_no": "171",
                "arrival": False,
                "rwy": "23",
                "aircraft_type": "B789",
                "wake": Wake.HEAVY,
            },
            "Air India",
        ),
    ],
)
def test_flight_info_airline_callsign(kwargs, expected):
    flight_info = FlightInfo(**kwargs)
    assert flight_info.airline_callsign == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {
                "ssr_code": "3427",
                "airline": "CZ",
                "raw_flight_no": "328",
                "arrival": True,
                "rwy": "20R",
                "aircraft_type": "A380",
                "wake": Wake.HEAVY,
            },
            True,
        ),
        (
            {
                "ssr_code": "7700",
                "airline": "AI",
                "raw_flight_no": "171",
                "arrival": False,
                "rwy": "23",
                "aircraft_type": "B789",
                "wake": Wake.HEAVY,
            },
            False,
        ),
    ],
)
def test_flight_info_chinese(kwargs, expected):
    flight_info = FlightInfo(**kwargs)
    assert flight_info.chinese == expected
