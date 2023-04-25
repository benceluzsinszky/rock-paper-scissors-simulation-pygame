import pygame
import math
import random

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

    def random_movement(self):
        self.rect.x += random.uniform(-0.5, 0.5)
        self.rect.y += random.uniform(-0.5, 0.5)

    def get_food_info(self, food):
        for sprite in food:
            distance = math.sqrt(
                (sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)
            if distance < self.closest_food_distance:
                self.closest_food_distance = distance
                self.closest_food = sprite

    def eat(self):
        if self.closest_food_distance != float("inf"):
            try:
                direction = pygame.math.Vector2(
                    self.closest_food.rect.center) - pygame.math.Vector2(self.rect.center)
                try:
                    direction.normalize_ip()
                except ValueError:
                    pass
                self.rect.move_ip(direction * 1.75)

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
        if self.closest_enemy_distance != float("inf"):
            try:
                direction = pygame.math.Vector2(
                    self.closest_enemy.rect.center) - pygame.math.Vector2(self.rect.center)
                try:
                    direction.normalize_ip()
                except ValueError:
                    pass
                self.rect.move_ip(direction * - 1.25)
            except AttributeError:
                pass
            self.closest_enemy_distance = float("inf")

    def check_walls(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 500:
            self.rect.bottom = 500
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500

    def check_self_collision(self, current):
        for sprite in current:
            if sprite != self:
                if pygame.sprite.collide_rect(self, sprite):
                    distance_x = self.rect.centerx - sprite.rect.centerx
                    # distance_X negative --> self is on the left
                    if distance_x > 0:
                        self.rect.x += 2
                    elif distance_x < 0:
                        self.rect.x -= 2

                    distance_y = self.rect.centery - sprite.rect.centery
                    # distance_y negative --> self is on the top
                    if distance_y > 0:
                        self.rect.y += 2
                    elif distance_y < 0:
                        self.rect.y -= 2

    def action(self, current, food, enemy):
        self.random_movement()
        self.get_food_info(food)
        self.get_enemy_info(enemy)
        self.check_walls()
        # if self.closest_enemy_distance > self.closest_food_distance:
        self.eat()
        # else:
        self.run()
        self.check_self_collision(current)

    def blit_sprite(self):
        self.screen.blit(self.image, self.rect)