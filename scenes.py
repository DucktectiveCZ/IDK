from abc import ABC, abstractmethod
from entities import Entity, Button, Player, Timer, Image
from context import Context
import pygame
from pygame import Rect
from brushes import TextBrush, TextureBrush
import colors

from graphics import Coord, Rectangle, Size


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
            Image(
                Rectangle(Coord(-1.0, -1.0), Size(1.0, 1.0)),
                TextureBrush.from_file("./assets/pink_background.jpg"),
            ),
            Button(
                Rectangle(Coord(0.0, 0.0), Size(0.1, 0.1)),
                TextureBrush.from_file("./assets/play_button.png"),
                TextBrush(
                    pygame.font.Font("./assets/PixelifySans.ttf", 20),
                    "",
                    colors.PURPLE,
                    None
                ),
                self.play_button_callback
            )
        ]

    def play_button_callback(self, context: Context) -> None:
        context.next_scene = GameScene()


# A scene where we can play.
class GameScene(Scene):
    # This is the name of the scene
    name = 'Game'
    # These are the entities inside of the scene
    children: list[Entity]

    def __init__(self) -> None:
        self.children = [
            Player(pos=Coord(0.0, 0.0), speed=0.05),
        ]
