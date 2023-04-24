import pygame
import sys


class Game():

    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()