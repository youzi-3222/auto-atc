"""
航路。
"""

from hashlib import md5


class Route:
    """
    航路。
    """

    name: str
    """航路名称。"""
    waypoints: list[str]
    """航路点列表。"""

    def __init__(self, name: str, waypoints: list[str]) -> None:
        self.name = name
        self.waypoints = waypoints

    def __hash__(self) -> int:
        return int(md5(f"{self.name}{self.waypoints}".encode("utf-8")).hexdigest(), 16)
