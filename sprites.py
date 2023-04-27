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
        self.repulsion_strength = 2
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

    def check_walls(self, game):
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

        # Calculate repulsion force from walls
        repulsion_force = pygame.math.Vector2(0, 0)
        if self.rect.left < 50:
            repulsion_force.x += 1 / (self.rect.left - 50)
        if self.rect.right > 450:
            repulsion_force.x -= 1 / (self.rect.right - 450)
        if self.rect.top < 50:
            repulsion_force.y += 1 / (self.rect.top - 50)
        if self.rect.bottom > 410:
            repulsion_force.y -= 1 / (self.rect.bottom - 410)

        # Apply repulsion force to move sprite away from walls
        self.rect.move_ip(repulsion_force * self.repulsion_strength)

    def check_self_collision(self, current):
        """
        Stops sprites in the same group from colliding.
        """
        # create a list of sprites within a certain distance of the player
        nearby_sprites = []
        for sprite in current:
            if sprite != self:
                distance_x = sprite.rect.centerx - self.rect.centerx
                distance_y = sprite.rect.centery - self.rect.centery
                distance = math.sqrt(distance_x**2 + distance_y**2)
                if distance < 50:
                    nearby_sprites.append(sprite)

        # check for collisions with nearby sprites
        for sprite in nearby_sprites:
            if pygame.sprite.collide_rect(self, sprite):
                distance_x = self.rect.centerx - sprite.rect.centerx
                # distance_X negative --> self is on the left
                if distance_x > 0:
                    self.rect.x += 1
                elif distance_x < 0:
                    self.rect.x -= 1

                distance_y = self.rect.centery - sprite.rect.centery
                # distance_y negative --> self is on the top
                if distance_y > 0:
                    self.rect.y += 1
                elif distance_y < 0:
                    self.rect.y -= 1

    def action(self, game, current, food, enemy):
        """
        Does every action for sprite.
        """
        self.random_movement()
        self.get_food_info(food)
        self.get_enemy_info(enemy)
        self.check_walls(game)
        self.eat()
        if self.closest_enemy_distance < 50:
            self.run()
        self.check_self_collision(current)

    def blit_sprite(self):
        """
        Blits sprite to screen.
        """
        self.screen.blit(self.image, self.rect)
