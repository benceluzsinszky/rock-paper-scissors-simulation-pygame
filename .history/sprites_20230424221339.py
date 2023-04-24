import pygame
import math

from pygame.sprite import Sprite


class Sprite(Sprite):
    """
    Class that creats a Rock/Papaer/Scissor character.
    """
    def __init__(self, game, character=str, location=tuple) -> None:
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load(f"sprites/{character}.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.closest_food = None
        self.closest_food_distance = float("inf")
        self.closest_enemy = None
        self.closest_enemy_distance = float("inf")

    def blit_sprite(self):
        self.screen.blit(self.image, self.rect)

    def get_food_info(self, food):
        for sprite in food:
            distance = math.sqrt(
                (sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)
            if distance < self.closest_food_distance:
                self.closest_food_distance = distance
                self.closest_food = sprite

    def eat(self):
        try:
            direction = pygame.math.Vector2(self.closest_food.rect.center) - pygame.math.Vector2(self.rect.center)
            try:
                direction.normalize_ip()
            except ValueError:
                pass
            if (
                self.rect.top > 0 and
                self.rect.bottom < 500 and
                self.rect.left > 0 and
                self.rect.right < 500
                 ):
                self.rect.move_ip(direction * 2)
        except AttributeError:
            pass
        self.closest_food_distance = float("inf")

    def get_enemy_info(self, enemy):
        for sprite in enemy:
            distance = math.sqrt((
                sprite.rect[0] - self.rect[1])**2 + (sprite.rect[1] - self.rect[1])**2)
            if distance < self.closest_enemy_distance:
                self.closest_enemy_distance = distance
                self.closest_enemy = sprite

    def run(self):
        direction = pygame.math.Vector2(self.closest_enemy.rect.center) - pygame.math.Vector2(self.rect.center)
        try:
            direction.normalize_ip()
        except ValueError:
            pass
        if (
            self.rect.top > 0 and
            self.rect.bottom < 500 and
            self.rect.left > 0 and
            self.rect.right < 500
             ):
            self.rect.move_ip(direction * -2)
        self.closest_enemy_distance = float("inf")

    def action(self, food, enemy):
        self.get_food_info(food)
        self.get_enemy_info(enemy)
        if self.closest_enemy_distance < 25:
            self.run()self.closest_food_distance:
            self.eat()
        else:
            self.run()