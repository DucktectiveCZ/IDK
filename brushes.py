from context import Context
import pygame
from pygame import Rect, Surface
from abc import ABC, abstractmethod
from typing import Self
from graphics import Color


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

class TextBrush(Brush):
    font: pygame.font.Font
    text: str
    foreground: Color
    background: Color | None

    def __init__(self, font: pygame.font.Font, text: str, foreground: Color, background: Color | None) -> None:
        self.font = font
        self.text = text
        self.foreground = foreground
        self.background = background

    def render(self, context: Context, dimensions: Rect) -> None:
        surface = self.font.render(self.text, False, self.foreground, self.background)
        context.screen.blit(surface, dimensions)
