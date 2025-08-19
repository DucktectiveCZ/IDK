from abc import ABC
import colors
from context import Context
import pygame
from typing import Callable, cast
from brushes import Brush
from graphics import AbsoluteCoord, Coord, Rectangle


class Entity(ABC):
    # Renders the entity
    def render(self, context: Context) -> None:
        pass

    # Updates the entity onto `context.screen`
    def update(self, context: Context) -> None:
        pass

    # Called when the parent scene is shown
    def activated(self, context: Context) -> None:
        pass

    # Called when the parent scene is hidden
    def deactivated(self, context: Context) -> None:
        pass


# Invokes a callback every N ticks
class Timer(Entity):
    delay: int
    callback: Callable[[Context], None]
    _ticks: int

    def __init__(
            self,
            delay: int,
            callback: Callable[[Context], None],
    ) -> None:
        self.delay = delay
        self.callback = callback
        self._ticks = 0

    def update(self, context: Context) -> None:
        if self._ticks >= self.delay:
            self._ticks = 0
            self.callback(context)


# A button. What else do you need to know. Its a button. It does button stuff.
class Button(Entity):
    dimensions: Rectangle
    callback: Callable[[Context], None]
    background: Brush
    foreground: Brush
    _is_pressed: bool

    def __init__(
            self,
            dimensions: Rectangle,
            background: Brush,
            foreground: Brush,
            callback: Callable[[Context], None],
    ) -> None:
        self.dimensions = dimensions
        self.background = background
        self.foreground = foreground
        self.callback = callback

    def update(self, context: Context) -> None:
        # Store the mouse x and y as mx and my
        mx, my = context.normalized_mouse_pos.into_tuple()

        # Check if the mouse is pressed and colliding with the button
        if not context.left_mouse_down:
            self._is_pressed = False
            return

        if not self._is_pressed and self.dimensions.contains_point(Coord(mx, my)):
            self._is_pressed = True
            self.callback(context)

    def render(self, context: Context) -> None:
        # We render the brush
        self.background.render(context, cast(pygame.Rect, context.denormalize(self.dimensions)))
        self.foreground.render(context, cast(pygame.Rect, context.denormalize(self.dimensions)))


# An entity that can be controlled using w/a/s/d and rendered as a red circle
class Player(Entity):
    pos: Coord
    speed: float

    def __init__(self, pos: Coord, speed: float) -> None:
        self.pos = pos
        self.speed = speed

    # This gets called every frame. It's for the entity's logic
    def update(self, context: Context) -> None:
        # W/A/S/D control
        if context.keys[pygame.K_w]:
            self.pos.y += self.speed
        if context.keys[pygame.K_s]:
            self.pos.y -= self.speed
        if context.keys[pygame.K_a]:
            self.pos.x -= self.speed
        if context.keys[pygame.K_d]:
            self.pos.x += self.speed

    # This draws the entity onto the screen (`context.screen`).
    def render(self, context: Context) -> None:
        # We just draw a red circle with the radius 50
        # at the position `self.x` and `self.y`.
        pygame.draw.circle(context.screen, colors.RED, cast(AbsoluteCoord, context.denormalize(self.pos)).into_tuple(), 50)


class Image(Entity):
    dimensions: Rectangle
    brush: Brush

    def __init__(self, dimensions: Rectangle, brush: Brush) -> None:
        self.dimensions = dimensions
        self.brush = brush

    def render(self, context: Context) -> None:
        self.brush.render(context, cast(pygame.Rect, context.denormalize(self.dimensions)))
