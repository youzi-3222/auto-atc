from src.atc.core.scene.aircraft.wake import Wake


def test_wake_enum():
    assert Wake.HEAVY.value == "H"
    assert Wake.MEDIUM.value == "M"
    assert Wake.LIGHT.value == "L"
