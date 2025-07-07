from atc.core.scene.aircraft.aircraft_type import AIRCRAFT_TYPE


def test_aircraft_type():
    assert len(AIRCRAFT_TYPE) > 0
    assert all(len(x) == 4 for x in AIRCRAFT_TYPE)
