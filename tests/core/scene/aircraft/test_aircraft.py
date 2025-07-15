import math
import time
from datetime import datetime, timedelta

import pytest
from pygame import Vector2

from atc.const import RESOLUTION
from atc.core.scene.aircraft import Aircraft
from atc.core.scene.aircraft.flight_info import FlightInfo
from atc.core.scene.aircraft.wake import Wake
from atc.core.scene.instruction import Instruction
from atc.core.scene.waypoint import WayPoint


@pytest.fixture
def mock_flight():
    """Fixture for creating a mock FlightInfo object"""
    return FlightInfo(
        ssr_code="3421",
        airline="3U",
        raw_flight_no="8633",
        arrival=False,
        rwy="02R",
        aircraft_type="A32N",
        wake=Wake.MEDIUM,
    )


@pytest.fixture
def aircraft(mock_flight: FlightInfo):
    """Fixture for creating a test aircraft"""
    return Aircraft(
        flight=mock_flight,
        pos=Vector2(100, 100),
        waypoint=["WPT1", "WPT2"],
        alt_ft=10000,
        speed_kt=250,
    )


def test_initialization(aircraft: Aircraft, mock_flight: FlightInfo):
    """Test that aircraft initializes with correct values"""
    assert aircraft.pos == Vector2(100, 100)
    assert aircraft.alt_ft == 10000
    assert aircraft.speed_kt == 250
    assert len(aircraft.waypoint) == 2
    assert aircraft.flight == mock_flight
    assert aircraft.heading == aircraft.target_heading
    assert aircraft.target_alt_ft == aircraft.alt_ft
    assert aircraft.target_speed_kt == aircraft.speed_kt
    assert not aircraft.clear_app


def test_properties(aircraft: Aircraft):
    """Test property accessors"""
    assert aircraft.airline_callsign == "四川"
    assert aircraft.chinese is True
    print(aircraft.heading)
    expected_geo = (aircraft.heading - 90) * 3.141592653589793 / 180
    assert pytest.approx(aircraft.heading_geo) == expected_geo


def test_instruct_heading(aircraft: Aircraft):
    """Test heading instruction"""
    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        heading=180,
        turn_left=True,
    )
    aircraft.instruct(instruction)
    assert aircraft.target_heading == 180
    assert aircraft.waypoint == []  # waypoints should be cleared


def test_instruct_turn_direction(aircraft: Aircraft):
    """Test turn direction instruction"""
    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        heading=180,
        turn_left=True,
    )
    aircraft.instruct(instruction)
    assert aircraft.turn_left is True

    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        heading=90,
        turn_left=False,
    )
    aircraft.instruct(instruction)
    assert aircraft.turn_left is False


def test_instruct_vector_to(aircraft: Aircraft):
    """Test vector_to instruction"""
    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        vector_to=["WPT1"],
    )
    aircraft.instruct(instruction)
    assert len(aircraft.waypoint) == 1
    assert isinstance(aircraft.waypoint[0], WayPoint)
    assert aircraft.waypoint[0].pos == Vector2(RESOLUTION[0] * 0.5, RESOLUTION[1] * 0.5)


def test_instruct_speed(aircraft: Aircraft):
    """Test speed instruction"""
    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        speed_kt=300,
    )
    aircraft.instruct(instruction)
    assert aircraft.target_speed_kt == 300


def test_instruct_altitude(aircraft: Aircraft):
    """Test altitude instruction"""
    instruction = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        alt_ft=15000,
    )
    aircraft.instruct(instruction)
    assert aircraft.target_alt_ft == 15000


def test_instruct_clear_app(aircraft: Aircraft):
    """Test clear approach instruction"""
    inst1 = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        clear_app=True,
    )
    aircraft.instruct(inst1)
    assert aircraft.clear_app is True

    inst2 = Instruction(
        flight=aircraft.flight,
        speed_old_kt=aircraft.speed_kt,
        alt_old_ft=aircraft.alt_ft,
        use_m=False,
        go_around=True,
    )
    aircraft.instruct(inst2)
    assert aircraft.clear_app is False


def test_update_position(aircraft: Aircraft, monkeypatch):
    """Test position update based on heading and speed"""
    # Set fixed heading and speed for predictable results
    aircraft.heading = 0  # North
    aircraft.speed_kt = 100
    aircraft.turn_left = True

    aircraft.update(timedelta(seconds=1))
    print(aircraft.pos)

    # Expected movement: north at 100 knots for 1 second
    # 100 kt = 100 * 0.1 nm/pixel * 1 sec = 10 pixels north (negative y in pygame)
    assert pytest.approx(aircraft.pos.x, abs=1) == 100
    assert pytest.approx(aircraft.pos.y, abs=1) == 90
