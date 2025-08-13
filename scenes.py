from abc import ABC
from entities import Entity
from context import Context


class Scene(ABC):
    # The name of the scene
    name: str
    # The entities in the scene
    children: list[Entity]

    def __init__(self):
        pass

    # Updates the scene
    def update(self, context: Context) -> None:
        for entity in self.children:
            entity.update(context)

    # Renders the scene onto `context.screen`
    def render(self, context: Context) -> None:
        for entity in self.children:
            entity.render(context)

    # Called when the scene is shown
    def activated(self, context: Context) -> None:
        for entity in self.children:
            entity.activated(context)

    # Called when the scene is hidden and another scene is shown
    def deactivated(self, context: Context) -> None:
        for entity in self.children:
            entity.deactivated(context)


class MenuScene(Scene):
    children = []
    name = 'Menu'
