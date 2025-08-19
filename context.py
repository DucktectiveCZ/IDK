from __future__ import annotations
import pygame
from pygame import Surface
from pygame.key import ScancodeWrapper
from dataclasses import dataclass
from config import Config
from graphics import Coord, AbsoluteCoord


@dataclass
class Context:
    screen: Surface
    config: Config
    keys: ScancodeWrapper
    mouse_pos: tuple[int, int]
    left_mouse_down: bool
    middle_mouse_down: bool
    right_mouse_down: bool
    _game: Game
    _current_scene: Scene

    @property
    def next_scene(self) -> Scene | None:
        return self._game.scene

    @next_scene.setter
    def next_scene(self, value: Scene) -> None:
        self._game.next_scene = value

    @property
    def current_scene(self) -> Scene:
        self._current_scene
        
    @property
    def absolute_mouse_pos(self) -> AbsoluteCoord:
        x, y = self.mouse_pos
        return AbsoluteCoord(x, y)

    @absolute_mouse_pos.setter
    def absolute_mouse_pos(self, value: AbsoluteCoord) -> None:
        pygame.mouse.set_pos(value.into_tuple())

    def normalize_one(self, x: int) -> float:
        return (2 * x) / 2

    def normalize(self, coord: AbsoluteCoord) -> Coord:
        x, y = coord.into_tuple()
        width, height = self.screen.get_size()

        nx = (2 * x) / width - 1
        ny = 1 - (2 * y) / height

        return Coord(nx, ny)

    def denormalize(self, coord: Coord) -> AbsoluteCoord:
        nx, ny = coord.into_tuple()
        width, height = self.screen.get_size()

        x = (nx + 1) * width / 2
        y = (1 - ny) * height / 2

        return AbsoluteCoord(int(x), int(y))

    @property
    def normalized_mouse_pos(self) -> Coord:
        return self.normalize(self.absolute_mouse_pos)
