from abc import ABC, abstractmethod
from entities import Entity, Button, Player, Timer
from context import Context
import pygame
from pygame import Rect
from graphics import ColorBrush, TextBrush
import colors
import logging


class Scene(ABC):
    # The name of the scene
    name: str
    # The entities in the scene
    children: list[Entity]

    @abstractmethod
    def __init__(self) -> None:
        pass

    # Updates the scene
    def update(self, context: Context) -> None:
        for child in self.children:
            child.update(context)

    # Renders the scene onto `context.screen`
    def render(self, context: Context) -> None:
        for child in self.children:
            child.render(context)

    # Called when the scene is shown
    def activated(self, context: Context) -> None:
        for child in self.children:
            child.activated(context)

    # Called when the scene is hidden and another scene is shown
    def deactivated(self, context: Context) -> None:
        for child in self.children:
            child.deactivated(context)


# This is the scene that gets displayed when the game starts
class MenuScene(Scene):
    # This is the name of the scene
    name = 'Menu'
    # These are the entities inside of the scene
    children: list[Entity]

    def __init__(self) -> None:
        self.children = [
            Button(
                Rect((0, 0), (100, 100)),
                ColorBrush(colors.WHITE),
                TextBrush(
                    pygame.font.SysFont("Arial", 30), 
                    "duk", 
                    colors.PURPLE,
                    None
                ),
                self.button_callback
            )
        ]

    def button_callback(self, context: Context) -> None:
        logging.info('QUAK')
        context.next_scene = GameScene()


# A scene where we can play.
class GameScene(Scene):
    # This is the name of the scene
    name = 'Game'
    # These are the entities inside of the scene
    children: list[Entity]

    def __init__(self) -> None:
        self.children = [
            Player(0, 0),
        ]
