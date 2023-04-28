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
        self.repulsion_strength = 3
        self.food_distance = float("inf")
        self.enemy_distance = float("inf")

    def random_movement(self):
        """
        Makes random movement.
        """
        self.rect.x += random.uniform(-0.5, 0.5)
        self.rect.y += random.uniform(-0.5, 0.5)

    def get_info(self, info_tree, info_list):
        """
        Gets info about closest sprite.
        Returns closest sprite's distance and angle.
        """
        # query the kd-tree for the nearest neighbor
        my_location = (self.rect.centerx, self.rect.centery)
        dist, idx = info_tree.query([my_location], k=1)

        # `idx` is the index of the nearest sprite in info_list
        closest = info_list[idx[0]]

        distance_x = closest.rect.centerx - self.rect.centerx
        distance_y = closest.rect.centery - self.rect.centery
        closest_distance = dist[0]
        closest_angle = math.atan2(distance_y, distance_x)

        return closest, closest_distance, closest_angle

    def move(self, distance, angle, speed):
        """
        Makes sprite move.
        """
        if distance != float("inf"):
            try:
                self.rect.centerx += math.cos(angle) * random.uniform(speed-0.4, speed)
                self.rect.centery += math.sin(angle) * random.uniform(speed-0.4, speed)

            except AttributeError:
                pass
            distance = float("inf")

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

        # Calculate repulsion force from walls
        repulsion_force = pygame.math.Vector2(0, 0)
        if self.rect.left < 100:
            repulsion_force.x += 1 / (self.rect.left - 100)
        if self.rect.right > 400:
            repulsion_force.x -= 1 / (self.rect.right - 400)
        if self.rect.top < 100:
            repulsion_force.y += 1 / (self.rect.top - 100)
        if self.rect.bottom > 360:
            repulsion_force.y -= 1 / (self.rect.bottom - 360)

        # Apply repulsion force to move sprite away from walls
        self.rect.move_ip(repulsion_force * self.repulsion_strength)

    def check_self_collision(self, current_tree, current_list):
        """
        Stops sprites in the same group from colliding.
        """
        def move_away(sprites):
            for sprite in sprites:
                if pygame.sprite.collide_rect(self, sprite):
                    distance_x = self.rect.centerx - sprite.rect.centerx
                    # distance_X negative --> self is on the left
                    if distance_x > 0:
                        self.rect.x += self.speed
                    elif distance_x < 0:
                        self.rect.x -= self.speed

                    distance_y = self.rect.centery - sprite.rect.centery
                    # distance_y negative --> self is on the top
                    if distance_y > 0:
                        self.rect.y += self.speed
                    elif distance_y < 0:
                        self.rect.y -= self.speed

        if len(current_list) > 6:
            my_location = (self.rect.centerx, self.rect.centery)
            dist, idx = current_tree.query([my_location], k=6)

            # `idx` is the index of the nearest sprite in info_list
            closest_5 = [current_list[idx[0][i+1]] for i in range(5)]
            move_away(closest_5)
        else:
            move_away(current_list)

    def action(self, current_tree, current_list, food_tree, food_list, enemy_tree, enemy_list):
        """
        Does every action for sprite.
        """
        self.random_movement()
        if food_list:
            closest_food, self.food_distance, self.food_angle = self.get_info(food_tree, food_list)
        if enemy_list:
            closest_enemy, self.enemy_distance, self.enemy_angle = self.get_info(enemy_tree, enemy_list)
        self.check_walls()
        self.move(self.food_distance, self.food_angle, self.speed)
        if self.enemy_distance < 50:
            self.move(self.enemy_distance, self.enemy_angle, -1*(self.speed-0.2))
        self.check_self_collision(current_tree, current_list)

    def blit_sprite(self):
        """
        Blits sprite to screen.
        """
        self.screen.blit(self.image, self.rect)
