"""
This module defines the `GameOverScreen` class, which represents the screen after the game has finished.
It extends the `TextScreen` class.
"""
from src.entities.text_screen import TextScreen


class GameOverScreen(TextScreen):
    """
    A class for managing the game over screen in the simulation.
    """

    def __init__(self, screen, winner):
        """
        Initialize a `GameOverScreen` object with the provided parameters.

        Args:
            screen (pygame.Surface): The Pygame surface representing the game screen.
            winner (str): The winner of the game (rock, paper, or scissors).
        """
        super().__init__(screen)
        self.current_screen = "game_over"
        self.winner = winner.upper()

    def sub_loop(self):
        """
        Manage the game over screen's content and interactions.

        This method is responsible for coordinating the game over screen's operations, including
        displaying the winner's name, handling restart and menu buttons, and responding to mouse interactions.
        """
        self.blit_text(f"{self.winner} WON", 200, font_size=24)
        restart_rect = self.blit_text("Restart", 300)
        menu_rect = self.blit_text("Main menu", 350)

        self.mouse_interaction(restart_rect, "Restart", self.restart_button)
        self.mouse_interaction(menu_rect, "Main menu", self.menu_button)

    def menu_button(self):
        """
        Transition to the main menu screen when the "Main menu" button is clicked.
        """
        self.current_screen = "menu"
        self.stop()

    def restart_button(self):
        """
        Restart the game with the previous speed and group size settings when the "Restart" button is clicked.
        """
        self.current_screen = "game"
        self.stop()
