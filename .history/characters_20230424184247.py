import pygame


class Character():
    """
    Class that creats a Rock/Papaer/Scissor character.
    """
    def __init__(self, game, character=str) -> None:
        self.screen = game.screen
        self.image = pygame.image.load(f"/{character}")
        image = pygame.transform.scale(self.image, (10, 10))
        self.rect = image.get_rect()

    def blit_character(self, location=tuple):
        self.screen.blit(self.image, loca
            (self.rect.x - game.scroll[0], self.rect.y - game.scroll[1]),
            (50, 50))