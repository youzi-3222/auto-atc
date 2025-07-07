"""
自动管理。
"""

from atc.core.scene import Scene

from .base import IAutoManagement


class Automatic(Scene):
    """
    自动管理的场景。
    """

    auto: list[IAutoManagement]
    """自动管理。"""

    def run_tick(self):
        super().run_tick()
        raise NotImplementedError

    def _run_auto(self):
        raise NotImplementedError
