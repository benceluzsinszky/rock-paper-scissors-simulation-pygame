import pygame


class Character():
    """
    Class that creats a Rock/Papaer/Scissor character.
    """
    def __init__(self, game, character=str) -> None:
        self.screen = game.screen
        self.image = pygame.image.load(f"sprites/{character}.png")
        selfimage = pygame.transform.scale(self.image, (10, 0.1))
        self.rect = self.image.get_rect()

    def blit_character(self, location=tuple):
        self.screen.blit(self.image, location)