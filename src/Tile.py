from typing import Tuple

import Building

import pygame
from pygame.locals import *


class Tile:
    """A single tile within the city's grid of tiles"""

    def __init__(self, image_surf, size):
        self.size = size

        # Change these later
        self.elevation = 0
        self.slant = 0
        self.zone = {
            "type": None,
            "density": None
        }

        self.crime_rate = 0
        self.flammability = 0
        self.pollution = {
            "air": 0,
            "water": 0,
            "garbage": 0
        }

        # Convert square image into isometric rhombus
        # TODO: refactor this into a Renderer function
        self.image = image_surf
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, -45)
        self.image.set_colorkey((37, 82, 16), pygame.RLEACCEL)
        self.image = pygame.transform.scale(self.image, (self.size*2, self.size))

    def catch_fire(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, display_surf: pygame.Surface, draw_position: Tuple,
            highlighted=False) -> None:
        # Draw base image of tile
        display_surf.blit(self.image, draw_position,
            special_flags=pygame.BLEND_ADD)

        # Highlight tile at mouse cursor position
        if highlighted == True:
            highlight_surface = pygame.Surface((self.size, self.size))
            highlight_surface.fill((0, 0, 10, 10))
            display_surf.blit(highlight_surface, draw_position,
                special_flags=pygame.BLEND_ADD)


class Road(Tile):
    def __init__(self):
        Tile.__init__(self)
        self.traffic_level = 0

class Rail(Tile):
    pass

class TreeArea(Tile):
    pass

class BuildingComponent(Tile):
    def __init__(self, parent_building: Building):
        self.parent_building = parent_building

class HighwayComponent(BuildingComponent):
    pass

class SeaportComponent(BuildingComponent):
    pass

class AirportComponent(BuildingComponent):
    pass

class LandfillComponent(BuildingComponent):
    pass
