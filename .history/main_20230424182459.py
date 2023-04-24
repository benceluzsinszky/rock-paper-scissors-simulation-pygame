import pygame
import sys


class Game():

    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Rock Paper Scissors")

        self.screen = pygame.display.set_mode((500, 500))

    def run_game(self):

        self.update_screen()
        self.clock.tick(60)
        ...

    def update_screen(self):
        ...

    def check_events(self):
        