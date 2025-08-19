import pygame
from pygame import Surface
from pygame.time import Clock
from graphics import AbsoluteCoord
from scenes import Scene
import config
import logging
from context import Context
from typing import Type


class Game:
    screen: Surface
    clock: Clock
    scene: Scene | None
    running: bool
    next_scene: Scene | None

    def __init__(self, app_name: str, default_scene_cls: Type[Scene]) -> None:
        self.config = config.load(app_name)
        self.next_scene = None
        self._init(
            self.config.fps,
            self.config.win_width,
            self.config.win_height,
            app_name,
            default_scene_cls,
        )

    def start(self) -> None:
        logging.debug('Starting the game loop...')
        while self.running:
            self._update()
            self._render()
            self.clock.tick(self.config.fps)

    def set_scene(self, scene: Scene) -> None:
        logging.debug(f"Switching to scene '{scene.name}'")
        if self.scene:
            self.scene.deactivated(self.context())

        self.scene = scene
        self.scene.activated(self.context())

    def context(self) -> Context:
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        return Context(
            screen=self.screen,
            config=self.config,
            keys=pygame.key.get_pressed(),
            mouse_pos=pygame.mouse.get_pos(),
            left_mouse_down=lmb,
            middle_mouse_down=mmb,
            right_mouse_down=rmb,
            _game=self,
            _current_scene=self.scene,
        )

    def _init(
            self,
            fps: int,
            width: int,
            height: int,
            title: str,
            initial_scene_cls: Type[Scene],
    ) -> None:
        assert fps > 0
        assert width > 0
        assert height > 0

        pygame.init()

        # pygame init
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        # state
        self.running = True

        self.scene = None
        self.set_scene(initial_scene_cls())

    def _update(self) -> None:
        # Handle events like quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Update the scene
        if self.scene:
            self.scene.update(self.context())

        if self.next_scene:
            self.set_scene(self.next_scene)
            self.next_scene = None

    def _render(self) -> None:
        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Render the scene
        if self.scene:
            self.scene.render(self.context())

        # Show the changes
        pygame.display.flip()
