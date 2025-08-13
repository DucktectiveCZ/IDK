from abc import ABC, abstractmethod
from context import Context


class Entity(ABC):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{{ x={self.x}, y={self.y}}}"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # Renders the entity
    @abstractmethod
    def render(self, context: Context) -> None:
        ...

    # Updates the entity onto `context.screen`
    @abstractmethod
    def update(self, context: Context) -> None:
        ...

    # Called when the parent scene is shown
    @abstractmethod
    def activated(self, context: Context) -> None:
        ...

    # Called when the parent scene is hidden
    @abstractmethod
    def deactivated(self, context: Context) -> None:
        ...
