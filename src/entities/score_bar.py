import pygame
from src.utils import constants


class ScoreBar():
    def __init__(self, screen, color):
        self.screen = screen
        self.color = color
        self.bottom = constants.RESOLUTION
        self.top = self.bottom - 25

    def draw(self, start, end):
        pygame.draw.rect(self.screen,
                         self.color,
                         [start,
                          self.top,
                          end,
                          self.bottom])
