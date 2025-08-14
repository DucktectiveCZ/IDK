from abc import ABC, abstractmethod
from context import Context
from pygame import Surface, Rect
from typing import NamedTuple, Self
import pygame


class Color(NamedTuple):
    r: int
    g: int
    b: int


class Brush(ABC):
    @abstractmethod
    def render(self, context: Context, dimensions: Rect) -> None:
        pass


class TextureBrush(Brush):
    _surface: Surface
    _cached: Surface | None

    def __init__(self, surface: Surface) -> None:
        self._surface = surface
        self._cached = None

    @staticmethod
    def from_file(path: str) -> Self:
        surface = pygame.image.load(path).convert_alpha()
        return TextureBrush(surface)

    def render(self, context: Context, dimensions: Rect) -> None:
        if (self._cached is None
                or self._cached.get_width() != dimensions.width
                or self._cached.get_height() != dimensions.height):
            self._cached = pygame.transform.scale(
                self._surface,
                (dimensions.width, dimensions.height)
            )

        context.screen.blit(self._cached, dimensions.topleft)


class ColorBrush(Brush):
    _color: Color

    def __init__(self, color: Color) -> None:
        self._color = color

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int):
        return cls(Color(r, g, b))

    def render(self, context: Context, dimensions: Rect) -> None:
        pygame.draw.rect(context.screen, self._color, dimensions)
