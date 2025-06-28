"""
显示。
"""

import math
from typing import Union

import pygame
from pygame import Vector2

from src.atc.core.automatic import Automatic
from src.atc.const import MAX_FPS, RESOLUTION, RWY_COLOR, RWY_LOC_LENGTH


class MainWindow:
    """
    程序主窗口。
    """

    screen: pygame.Surface
    clock: pygame.time.Clock
    running: bool

    font: pygame.font.Font

    scene: Automatic
    """场景。"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("微软雅黑", 24)
        raise NotImplementedError("自动管理")

    def write(
        self, text: str, pos: pygame.Vector2, color: Union[pygame.Color, str] = "white"
    ):
        """
        写文字。
        """
        self.screen.blit(self.font.render(text, True, color), pos)

    def render(self):
        """
        运行、渲染一帧并显示。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.screen.fill("black")
        self._render_rwy()
        self._render_waypoint()

        pygame.display.flip()
        self.clock.tick(MAX_FPS)

    def _render_rwy(self):
        raise NotImplementedError("跑道允许降落时才渲染定位线")
        for rwy in self.scene.rwy:
            pygame.draw.line(self.screen, RWY_COLOR, rwy.pos1, rwy.pos2, width=5)
            pygame.draw.line(
                self.screen,
                RWY_COLOR,
                rwy.pos1,
                rwy.pos1
                - Vector2(
                    RWY_LOC_LENGTH * math.cos(rwy.direction_geo),
                    RWY_LOC_LENGTH * math.sin(rwy.direction_geo),
                ),
                width=1,
            )
            pygame.draw.line(
                self.screen,
                RWY_COLOR,
                rwy.pos2,
                rwy.pos2
                + Vector2(
                    RWY_LOC_LENGTH * math.cos(rwy.direction_geo),
                    RWY_LOC_LENGTH * math.sin(rwy.direction_geo),
                ),
                width=1,
            )
            self.write(rwy.num, rwy.pos1)
            self.write(rwy.num_rev, rwy.pos2)

    def _render_waypoint(self):
        for waypoint in self.scene.waypoint:
            pygame.draw.circle(self.screen, "white", waypoint.pos, radius=3)
            self.write(waypoint.name, waypoint.pos + Vector2(5, 0))
