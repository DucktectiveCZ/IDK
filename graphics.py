from typing import NamedTuple
from dataclasses import dataclass


@dataclass
class Coord:
    x: float
    y: float

    def into_tuple(self) -> tuple[float, float]:
        return self.x, self.y


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
