import pygame
from pygame.locals import *

import GameMain
import City
from City import *
import Renderer
from Renderer import *

EYE_POS_CHANGE = 1


class GameState:

    """Base class for derived game state classes."""

    def __init__(self, game: GameMain) -> None:
        self.game = game

    def draw(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def handle_input(self, event: pygame.event) -> None:
        pass


class GameStateStart(GameState):

    """Initial game state at launch."""

    def __init__(self, game: GameMain) -> None:
        super().__init__(game)
        game.renderer = Renderer(game, None, None)

    def draw(self) -> None:
        """Render title screen and main menu interface."""

        # Placeholder title screen. Get rid of this later
        self.game.renderer.draw_text(text="City Builder", font_face="sans",
            font_size=30, antialias=False, color=(255, 255, 255),
            offset=(45, 15))

        self.game.renderer.draw_text(text="Press <Space> to start",
            font_face="sans", font_size=18, antialias=False,
            color=(255, 255, 255), offset=(45, 90))

    def handle_input(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.renderer.draw_text(text="Loading...",
                    font_face="sans",  font_size=18, antialias=False,
                    color=(255, 255, 255), offset=(90, 180))

                # TODO: Change this later
                self.game.push_state(GameStateEditor(self.game, City.City(100,
                    "New City", self.game.renderer.tile_size)))


class GameStateEditor(GameState):

    """State while playing the game."""

    def __init__(self, game: GameMain, city: City) -> None:
        super().__init__(game)
        self.city = city
        game.city = self.city
        game.city_size = self.city.size
        self.eye_pos = (
            [int(i / self.game.renderer.tile_size) for i in self.game.center])

        game.renderer = Renderer(game, self.city, self.eye_pos)
        self.iso_eye_pos = (
            [int(i) for i in game.renderer.cart2iso(self.eye_pos)])

    def update(self, dt: float) -> None:
        self.city.update_all_tiles(dt)

    def draw(self) -> None:
        """Draw tiles of city and user interface"""
        self.game.renderer.draw_visible_tiles(self.iso_eye_pos)
        self.game.renderer.draw_interface()
        pass

    def handle_input(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            # Move eye position if arrow keys are pressed
            if event.key == pygame.K_LEFT:
                self.iso_eye_pos[0] -= EYE_POS_CHANGE

            elif event.key == pygame.K_RIGHT:
                self.iso_eye_pos[0] += EYE_POS_CHANGE

            elif event.key == pygame.K_DOWN:
                self.iso_eye_pos[1] += EYE_POS_CHANGE

            elif event.key == pygame.K_UP:
                self.iso_eye_pos[1] -= EYE_POS_CHANGE
