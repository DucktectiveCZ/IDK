from __future__ import annotations
from pygame import Surface
from pygame.key import ScancodeWrapper
from dataclasses import dataclass
from config import Config


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

    @property
    def next_scene(self) -> Scene | None:
        return self._game.scene

    @next_scene.setter
    def next_scene(self, value: Scene) -> None:
        self._game.next_scene = value
