import pygame


class Character():
    """
    Class that creats a Rock/Papaer/Scissor character.
    """
    def __init__(self, game) -> None:
        self.screen = game.screen
        self.image = pygame.image.load("")