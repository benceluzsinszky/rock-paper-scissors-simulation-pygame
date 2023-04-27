import pygame
import math
import random

from pygame.sprite import Sprite


class Sprite(Sprite):
    """
    Class that creates a Rock/Papaer/Scissor sprite.
    """

    def __init__(self, game, character=str, location=tuple) -> None:
        """
        Initializes a single sprite.
        """
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load(f"sprites/{character}.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.food_angle = 0
        self.enemy_angle = 0
        self.speed = game.speed
        self.closest_food = None
        self.closest_food_distance = float("inf")
        self.closest_enemy = None
        self.closest_enemy_distance = float("inf")

    def random_movement(self):
        """
        Makes random movement.
        """
        self.rect.x += random.uniform(-0.5, 0.5)
        self.rect.y += random.uniform(-0.5, 0.5)

    def get_food_info(self, food):
        """
        Gets info about closest food sprite.
        """
        for sprite in food:
            distance_x = sprite.rect.centerx - self.rect.centerx
            distance_y = sprite.rect.centery - self.rect.centery
            distance = math.sqrt(distance_x**2 + distance_y**2)
            if distance < self.closest_food_distance:
                self.closest_food_distance = distance
                self.closest_food = sprite
                self.food_angle = math.atan2(distance_y, distance_x)

    def eat(self):
        """
        Makes sprite go towards food.
        """
        if self.closest_food_distance != float("inf"):
            try:
                self.rect.centerx += math.cos(self.food_angle) * random.uniform(self.speed-0.4, self.speed)
                self.rect.centery += math.sin(self.food_angle) * random.uniform(self.speed-0.4, self.speed)

            except AttributeError:
                pass
            self.closest_food_distance = float("inf")

    def get_enemy_info(self, enemy):
        """
        Gets info about closest enemy sprite.
        """
        for sprite in enemy:
            distance_x = sprite.rect.centerx - self.rect.centerx
            distance_y = sprite.rect.centery - self.rect.centery
            distance = math.sqrt(distance_x**2 + distance_y**2)
            if distance < self.closest_enemy_distance:
                self.closest_enemy_distance = distance
                self.closest_enemy = sprite
                self.enemy_angle = math.atan2(distance_y, distance_x)

    def run(self):
        """
        Makes sprite go away from enemies.
        """
        if self.closest_enemy_distance != float("inf"):
            try:
                self.rect.centerx -= math.cos(self.enemy_angle) * random.uniform(self.speed-0.6, self.speed-0.2)
                self.rect.centery -= math.sin(self.enemy_angle) * random.uniform(self.speed-0.6, self.speed-0.2)
            except AttributeError:
                pass
            self.closest_enemy_distance = float("inf")

    def check_walls(self):
        """
        Stops sprite at walls.
        """
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 460:
            self.rect.bottom = 460
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500

    def check_self_collision(self, current):
        """
        Stops sprites in the same group from colliding.
        """
        for sprite in current:
            if sprite != self:
                if pygame.sprite.collide_rect(self, sprite):
                    distance_x = self.rect.centerx - sprite.rect.centerx
                    # distance_X negative --> self is on the left
                    if distance_x > 0:
                        self.rect.x += 1.5
                    elif distance_x < 0:
                        self.rect.x -= 1.5

                    distance_y = self.rect.centery - sprite.rect.centery
                    # distance_y negative --> self is on the top
                    if distance_y > 0:
                        self.rect.y += 1.5
                    elif distance_y < 0:
                        self.rect.y -= 1.5

    def action(self, current, food, enemy):
        """
        Does every action for sprite.
        """
        self.random_movement()
        self.get_food_info(food)
        self.get_enemy_info(enemy)
        self.check_walls()
        self.eat()
        if self.closest_enemy_distance < 50:
            self.run()
        self.check_self_collision(current)

    def blit_sprite(self):
        """
        Blits sprite to screen.
        """
        self.screen.blit(self.image, self.rect)
