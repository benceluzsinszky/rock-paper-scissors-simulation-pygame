"""
This module defines a single `ScoreBar` class, which is used to create the score bar
for one of the contender groups in the game.
The score bar is represented as a colored rectangle drawn on the bottom of the screen.
"""
import pygame
from src.utils import constants


class ScoreBar:
    """
    A class for creating a score bar in the game.
    """

    def __init__(self, screen, color):
        """
        Initialize a `ScoreBar` object with the specified attributes.

        Args:
            screen (pygame.Surface): The Pygame surface representing the game screen.
            color (tuple): The RGB color value for the score bar.
        """
        self.screen = screen
        self.color = color
        self.bottom = constants.RESOLUTION
        self.top = self.bottom - 25

    def draw(self, start, end):
        """
         Draw the score bar on the game screen.

        Args:
            start (int): The starting x-coordinate of the score bar.
            end (int): The ending x-coordinate of the score bar.

        The score bar is represented as a colored rectangle on the game screen, extending
        horizontally from `start` to `end` coordinates at the bottom of the screen.
        """
        pygame.draw.rect(self.screen, self.color, [start, self.top, end, self.bottom])
