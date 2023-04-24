import pygame


class Character():
    """
    Class that creats a Rock/Papaer/Scissor character.
    """
    def __init__(self, game, character=str) -> None:
        self.screen = game.screen
        self.image = pygame.image.load(f"/{character}")
        image = pygame.transform.scale(image, (50, 50))
        self.rect = image.get_rect()