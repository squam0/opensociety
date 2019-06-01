from typing import Tuple

import pygame
from pygame.locals import *

import City
import GameMain


class Renderer:

    def __init__(self, game: GameMain, city: City, eye_pos: Tuple):
        self.game = game
        self.display_surf = self.game.display_surf
        self.city = city
        self.tile_size = 20
        self.iso_size = (self.tile_size * 2, self.tile_size)
        self.size = self.display_surf.get_size()
        self.tile_margin = (int(self.size[0]/2 / self.tile_size),
            int(self.size[1]/2 / self.tile_size))

        self.iso_tile_margin = ([int(i) for i in self.cart2iso(self.tile_margin)])
        self.mouse_tile_pos = [0, 0]
        self.highlighted_tile_pos = [0, 0]

    def draw_text(self, text: str, font_face: str, font_size: int,
            antialias: bool, color: Tuple, offset: Tuple) -> None:
        """
        Render text on the screen.

        Keyword arguments:
        text ---------- String of characters to render
        font_face ----- Font face in which the characters will be rendered
        font_size ----- Size, in pixels, of font
        antialias ----- Whether or not to use pygame's built-in font smoothing
        color --------- Tuple of the format (RED, GREEN, BLUE) where RED, GREEN
                        and BLUE are integers from 0 to 255 each representing
                        the intensity of its respective color component
        offset -------- Tuple of the format (X, Y) where X and Y are integers
                        representing offset from the top and left side of the
                        screen, respectively, in pixels
        """

        text_font = pygame.font.SysFont(font_face, font_size)
        text_surface = text_font.render(text, antialias, color)
        self.display_surf.blit(text_surface, offset)
        pygame.display.flip()

    def draw_background(self) -> None:
        self.display_surf.fill([0, 0, 0])

    def highlight_tile_at_mouse_pos(self, color: Tuple=(100,0,0)) -> None:
        """
        Highlight the tile the cursor is currently over.
        If the cursor has moved, un-highlight the previously highlighted tile.
        """
        tile = self.city.get_tile(self.mouse_tile_pos)
        if tile is not None:
            self.city.get_tile(self.mouse_tile_pos).draw(
                self.display_surf,
                (self.mouse_tile_pos[0] * self.iso_size[0],
                    self.mouse_tile_pos[1] * self.iso_size[1]),
                highlighted=True)

    def cart2iso(self, cart_coords: Tuple) -> Tuple:
        """Convert cartesian coordinates to isometric coordinates."""
        iso_coords = (
            cart_coords[0] - cart_coords[1],
            (cart_coords[0] + cart_coords[1]) /2
        )
        return iso_coords

    def iso2cart(self, iso_coords: Tuple) -> Tuple:
        """Convert cartesian coordinates to isometric coordinates."""
        cart_coords = (
            (iso_coords[0] + iso_coords[1]*2) / 2,
            -iso_coords[0] + (iso_coords[0] + iso_coords[1]*2) / 2
        )
        return cart_coords

    def cart_surface_to_iso(cart_surface: pygame.Surface) -> pygame.Surface:
        pass

    def draw_visible_tiles(self, eye_pos: Tuple) -> None:
        """Draw all tiles visible from current eye position

        eye_pos -- Tuple representing the position in the tile array that
                        is at the center of the screen
        """
        self.draw_background() # Draw background

        # Calculate indices of tiles to draw
        ul_tile = [eye_pos[0] - self.tile_margin[0],
            eye_pos[1] - self.iso_tile_margin[1]]

        lr_tile = [eye_pos[0] + self.tile_margin[0],
            eye_pos[1] + self.iso_tile_margin[1]]

        # Boundary checking
        for i in range(len(ul_tile)):
            if ul_tile[i] < 0:
                ul_tile[i] = 0
        for i in range(len(lr_tile)):
            if lr_tile[i] >= self.city.size:
                lr_tile[i] = self.city.size - 1

        draw_pos = [0, 0]
        self.ul_tile = tuple(ul_tile)
        self.lr_tile = tuple(lr_tile)

        # Calculate which tile the cursor is over
        iso_mouse_pos = ((2*self.game.mouse_pos[0] - self.iso_size[0]/2)/2,
            self.game.mouse_pos[1])
        print(iso_mouse_pos)

        for i in range(len(self.game.mouse_pos)):
            self.mouse_tile_pos[i] = int(iso_mouse_pos[i] / self.iso_size[i]
                + eye_pos[i] - self.iso_tile_margin[i]))

        self.highlight_tile_at_mouse_pos()

        for tile_row in self.city.tiles[self.ul_tile[0]:self.lr_tile[0]]:
            for tile in tile_row[self.ul_tile[1]:self.lr_tile[1]]:
                tile.draw(self.display_surf, self.cart2iso(tuple(draw_pos)),
                    highlighted=False)
                draw_pos[1] += self.tile_size

            draw_pos[1] = 0
            draw_pos[0] += self.tile_size

    def draw_interface(self) -> None:
        pass
