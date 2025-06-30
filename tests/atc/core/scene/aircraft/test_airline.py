import pytest

from src.atc.core.scene.aircraft.airline import AIRLINE


@pytest.mark.parametrize(
    "airline,expected",
    [
        ("IR", "Iran Air"),
        ("NW", "Northwest"),
        ("BA", "British"),
    ],
)
def test_airline_code_to_callsign(airline, expected):
    assert AIRLINE[airline] == expected
