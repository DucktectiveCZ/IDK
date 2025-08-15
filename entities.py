from abc import ABC
from context import Context
from pygame import Rect
import pygame
from typing import Callable
from graphics import Brush


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
    dimensions: Rect
    callback: Callable[[Context], None]
    brush: Brush
    _is_pressed: bool

    def __init__(
            self,
            dimensions: Rect,
            brush: Brush,
            callback: Callable[[Context], None],
    ) -> None:
        self.dimensions = dimensions
        self.brush = brush
        self.callback = callback

    def update(self, context: Context) -> None:
        # Store the mouse x and y as mx and my
        mx, my = context.mouse_pos

        # Check if the mouse is pressed and colliding with the button
        if not context.left_mouse_down:
            self._is_pressed = False
            return

        if not self._is_pressed and self.dimensions.collidepoint(mx, my):
            self._is_pressed = True
            self.callback(context)

    def render(self, context: Context) -> None:
        # We render the brush
        self.brush.render(context, self.dimensions)


# An entity that can be controlled using w/a/s/d and rendered as a red circle
class Player(Entity):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # This gets called every frame. It's for the entity's logic
    def update(self, context: Context) -> None:
        # W/A/S/D control
        if context.keys[pygame.K_w]:
            self.x -= 5
        if context.keys[pygame.K_s]:
            self.x += 5
        if context.keys[pygame.K_a]:
            self.y -= 5
        if context.keys[pygame.K_d]:
            self.y += 5

    # This draws the entity onto the screen (`context.screen`).
    def render(self, context: Context) -> None:
        # This is just the color red
        RED = (255, 0, 0)
        # We just draw a red circle with the radius 50
        # at the position `self.x` and `self.y`.
        pygame.draw.circle(context.screen, RED, (self.y, self.x), 50)

    # This gets called when the entity is spawned.
    # We don't need that for this entity, so we just make it do nothing
    def activated(self, context: Context) -> None:
        pass

    # This gets called when the entity is despawned.
    # We don't need that for this entity, so we just make it do nothing
    def deactivated(self, context: Context) -> None:
        pass
