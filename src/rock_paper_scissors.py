"""
    This module is the entry point for the game, responsible for setting up the game window, handling different
    game screens, and managing the main game loop.
"""
import pygame
from src.utils import constants
from src.entities.menu_screen import MenuScreen
from src.entities.game_over_screen import GameOverScreen
from src.entities.game_screen import GameScreen


class RockPaperScissors:
    """
    The main game class responsible for initializing, managing, and running the Rock Paper Scissors game.
    """

    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()
        self.running = True
        self.current_screen = "menu"
        self.screen = pygame.display.set_mode(
            (constants.RESOLUTION, constants.RESOLUTION)
        )
        pygame.display.set_caption("Rock Paper Scissors")
        icon = pygame.image.load("assets/sprites/logo.png")
        pygame.display.set_icon(icon)

    def run_game(self):
        """
        Run the main game loop.

        This method manages the flow of the game by creating and running different game screens:
        - MenuScreen: Allows the player to set game options like speed and group size.
        - GameScreen: The main game screen where the Rock Paper Scissors battle takes place.
        - GameOverScreen: Displays the game result when it's over.
        """
        while self.running:
            match self.current_screen:
                case "menu":
                    menu = MenuScreen(self.screen)
                    self.loop_screen(menu)
                    speed = menu.get_speed()
                    group_size = menu.get_group_size()
                case "game":
                    game = GameScreen(self.screen, speed, group_size)
                    self.loop_screen(game)
                    winner = game.get_winner()
                case "game_over":
                    game_over = GameOverScreen(self.screen, winner)
                    self.loop_screen(game_over)

    def loop_screen(self, looped_screen):
        """
        Run a specific game screen loop.

        Args:
            looped_screen: An instance of a game screen class (MenuScreen, GameScreen, or GameOverScreen).
        """
        screen_running = True
        while screen_running:
            looped_screen.main_loop()
            self.current_screen = looped_screen.get_current_screen()
            screen_running = looped_screen.get_is_running()
