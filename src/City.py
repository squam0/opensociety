from typing import Tuple

import pygame
from pygame.locals import *

from Tile import Tile
import ImageInfo

class City:

    """
    Class to store data for the city as a whole, which is represented within
    the game as a matrix of tiles and some associated stats.
    """

    def __init__(self, size=25, name="New City", tile_size=10):
        self.population = 0
        self.size = size
        self.name = name
        self.center = (size/2, size/2)
        self.money = 50000
        self.highlighted_tile_pos = None

        # Initialize tiles matrix
        tile_image = pygame.image.load(
            ImageInfo.image_dict["terrain"]["grass"]).convert()

        self.tiles = [[] for i in range(size)]

        for i in range(size):
            self.tiles[i] = [Tile(tile_image, tile_size) for j in range(size)]

    def update_all_tiles(self, dt: float) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[i][j].update(dt)

    def get_tile(self, position: tuple) -> Tile:
        try:
            return self.tiles[position[0]][position[1]]
        except IndexError:
            return None
