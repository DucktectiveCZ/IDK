import pygame
from pygame import Surface
from pygame.time import Clock
from scenes import Scene
import config
import logging
from context import Context


class Game:
    screen: Surface
    clock: Clock
    scene: Scene | None
    running: bool

    def __init__(self, app_name: str, default_scene: Scene):
        self.config = config.load(app_name)
        self._init(
            self.config.fps,
            self.config.win_width,
            self.config.win_height,
            app_name,
            default_scene,
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
        return Context(
            screen=self.screen,
            config=self.config,
            keys=pygame.key.get_pressed(),
        )

    def _init(
            self,
            fps: int,
            width: int,
            height: int,
            title: str,
            initial_scene: Scene
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
        self.set_scene(initial_scene)

    def _update(self) -> None:
        # Handle events like quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Update the scene
        if self.scene:
            self.scene.update(self.context())

    def _render(self) -> None:
        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Render the scene
        if self.scene:
            self.scene.render(self.context())

        # Show the changes
        pygame.display.flip()
