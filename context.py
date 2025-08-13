from pygame import Surface
from pygame.key import ScancodeWrapper
from dataclasses import dataclass
from config import Config


@dataclass
class Context:
    screen: Surface
    config: Config
    keys: ScancodeWrapper
