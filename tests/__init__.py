import warnings

import atc

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pygame")

atc.config = {
    "nm_per_pixel": 0.1,
    "waypoint": {
        "WPT1": {"name": "WPT1", "position": [0.5, 0.5], "usage": 1},
        "WPT2": {"name": "WPT2", "position": [0.6, 0.6], "usage": 1},
    },
}
