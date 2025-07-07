from atc.core.scene.aircraft.flight_info import FlightInfo
from atc.core.scene.aircraft.wake import Wake
from atc.core.scene.instruction import Instruction

print(
    Instruction(
        **{
            "flight": FlightInfo("7700", "3U", "8633", True, "02R", "A319", Wake.LIGHT),
            "speed_old_kt": 230,
            "alt_old_ft": 4000,
            "use_m": True,
            "heading": None,
            "turn_left": None,
            "vector_to": ["MIKOS"],
            "speed_kt": 230,
            "alt_ft": 4000,
            "clear_app_rwy": None,
        }
    ).speech
)
