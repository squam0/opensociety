"""Free city-building game."""

# Built in modules
import time
from typing import Tuple

# Third-party modules
import pygame
from pygame.locals import *

# Local modules
import GameState
from GameState import *
import City
from City import *


# Values to be used if values not defined in XML
DEFAULT_WIDTH = 1600
DEFAULT_HEIGHT = 900


class GameMain:
    """Handles states, input, drawing, and control flow of game"""

    def __init__(self):
        self._running = True
        self.display_surf = None

    # <editor-fold desc="Main loop methods">

    def on_init(self) -> None:
        """Initialize pygame and game context variables"""

        pygame.init()
        pygame.font.init()

        # Set display-related variables
        self.size = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.center = ([i/2 for i in self.size])
        self.display_surf = pygame.display.set_mode(self.size,
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.time_start = time.perf_counter()
        self.city = None

        # Set start state
        self.game_states = []
        self.push_state(GameStateStart(self))
        self._running = True

    def on_event(self, event) -> None:
        """Handle event from pygame event queue"""

        if event.type == pygame.QUIT:
            self._running = False # Break main loop
        else:
            self.peek_state().handle_input(event)

    def on_loop(self) -> None:
        """Method to be executed once each time the game loop repeats."""

        # Calculate elapsed time
        time_end = time.perf_counter()
        dt = time_end - self.time_start
        self.time_start = time_end

        self.mouse_pos = pygame.mouse.get_pos() # Store mouse position

        # Update and draw
        if self.peek_state != None:
            self.peek_state().update(dt)
            self.peek_state().draw()
        pygame.display.flip()

    def on_cleanup(self) -> None:
        """Exit game using pygame's built-in cleanup functions."""

        pygame.font.quit()
        pygame.quit()

    def on_execute(self) -> None:
        """
        Initialize game, go into main loop, perform cleanup when main loop
        breaks
        """

        if self.on_init() == False:
            self._running = False

        # Main loop
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()

        # Cleanup and exit
        self.on_cleanup()

    #</editor-fold>

    # <editor-fold desc="State methods">

    def push_state(self, state: GameState) -> None:
        """Push state onto state stack"""

        self.game_states.append(state)
        pass

    def pop_state(self) -> None:
        """Pop state from state stack"""

        self.game_state = self.game_state[:-1]
        pass

    def change_state(self, state: GameState) -> None:
        """Pop from state stack if not empty, then push state onto stack"""

        if self.game_states != []:
            self.pop_state()
        self.push_state(state)
        pass

    def peek_state(self) -> GameState:
        "Return state on top of stack (None if stack is empty)"

        if (self.game_states == []): return None
        return self.game_states[-1]

    # </editor-fold>


# Run
if __name__ == "__main__":
    game = GameMain()
    game.on_execute()
