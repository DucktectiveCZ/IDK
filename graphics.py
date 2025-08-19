from typing import NamedTuple
from dataclasses import dataclass


@dataclass
class Coord:
    x: float
    y: float

    def into_tuple(self) -> tuple[float, float]:
        return self.x, self.y

@dataclass
class Size:
    width: float
    height: float

    def into_tuple(self) -> tuple[float, float]:
        return self.width, self.height


@dataclass
class AbsoluteCoord:
    x: int
    y: int

    def into_tuple(self) -> tuple[int, int]:
        return self.x, self.y


class Color(NamedTuple):
    r: int
    g: int
    b: int


@dataclass
class Rectangle:
    pos: Coord
    size: Size

    def collides_with(self, other: "Rectangle") -> bool:
        return not (
            self.pos.x + self.size.width <= other.pos.x or
            other.pos.x + other.size.width <= self.pos.x or
            self.pos.y + self.size.height <= other.pos.y or
            other.pos.y + other.size.height <= self.pos.y
        )

    def contains_point(self, point: Coord | AbsoluteCoord) -> bool:
        return (
            self.pos.x <= point.x <= self.pos.x + self.size.width and
            self.pos.y <= point.y <= self.pos.y + self.size.height
        )
