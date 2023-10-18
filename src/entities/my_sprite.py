import math
import random
import pygame
from pygame.sprite import Sprite
from src.utils import constants


class MySprite(Sprite):
    """
    Class that creates a Rock/Paper/Scissor sprite.
    """

    def __init__(
        self, screen, image, location, speed, own_group, hunter_group, prey_group
    ):
        """
        Initializes a single sprite.
        """
        super().__init__()
        self.screen = screen
        self.sprite_text = image
        self.image = pygame.image.load(f"assets/sprites/{self.sprite_text}.png")
        self.rect = self.create_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.speed = speed
        self.own_group = own_group
        self.hunter_group = hunter_group
        self.prey_group = prey_group

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def get_rect(self):
        return self.rect

    def get_sprite_text(self):
        return self.sprite_text

    def get_distance(self, sprite):
        sprite_coordinates = sprite.get_coordinates()
        distance_x = sprite_coordinates[0] - self.rect.x
        distance_y = sprite_coordinates[1] - self.rect.y
        return math.sqrt(distance_x**2 + distance_y**2)

    def get_closest(self, group):
        closest_sprite = None
        closest_distance = float("inf")
        for sprite in group:
            distance = self.get_distance(sprite)
            if distance < closest_distance:
                closest_distance = distance
                closest_sprite = sprite
        return closest_sprite

    def set_groups(self, own_group, hunter_group, prey_group):
        self.own_group = own_group
        self.hunter_group = hunter_group
        self.prey_group = prey_group

    def set_image(self, image):
        self.image = image
        self.create_rect()

    def create_rect(self):
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((255, 255, 255))
        return self.image.get_rect()

    def update_sprite(self):
        self.move_sprite()
        self.self_collision()
        self.check_walls()

    def move_sprite(self):
        self.random_movement()
        self.hunter_prey_behaviour()

    def random_movement(self):
        """
        Makes random movement.
        """
        self.rect.x += random.uniform(-1, 1)
        self.rect.y += random.uniform(-1, 1)

    def hunter_prey_behaviour(self):
        closest_prey = self.get_closest(self.prey_group)
        if closest_prey:
            self.chase(closest_prey, 1)
            if pygame.sprite.collide_rect(self, closest_prey):
                self.eat(closest_prey)

        closest_hunter = self.get_closest(self.hunter_group)
        if closest_hunter:
            if self.hunter_close_by(closest_hunter):
                self.chase(closest_hunter, -0.95)

    def chase(self, sprite, direction):
        distance = self.get_distance(sprite)
        if distance == 0:
            return
        distance_x = sprite.get_coordinates()[0] - self.rect.x
        self.rect.x += (
            (distance_x / distance)
            * random.uniform(self.speed - 0.2, self.speed)
            * direction
        )

        distance_y = sprite.get_coordinates()[1] - self.rect.y
        self.rect.y += (
            (distance_y / distance)
            * random.uniform(self.speed - 0.2, self.speed)
            * direction
        )

    def hunter_close_by(self, hunter):
        distance = self.get_distance(hunter)
        return distance < 100

    def eat(self, prey):
        # TODO: images are flickering when eaten
        sprite = MySprite(
            self.screen,
            self.sprite_text,
            prey.get_coordinates(),
            self.speed,
            self.own_group,
            self.hunter_group,
            self.prey_group,
        )
        self.own_group.add(sprite)
        prey.kill()

    def check_walls(self):
        self.avoid_walls()
        self.stay_inside_walls()

    def avoid_walls(self):
        """
        Make sprites avoid screen borders.
        """
        # Only avoid walls, if sprite is in the outer quarters
        in_outer_quarter = (
            self.rect.centerx < constants.RESOLUTION * 0.25
            or self.rect.centerx > constants.RESOLUTION * 0.75
            or self.rect.centery < constants.RESOLUTION * 0.25
            or self.rect.centery > (constants.RESOLUTION - 40) * 0.27
        )
        if not in_outer_quarter:
            return

        avoidance_x = self.calculate_aviodance(self.rect.x)
        avoidance_y = self.calculate_aviodance(self.rect.y)

        self.rect.x += random.uniform(0, avoidance_x)
        self.rect.y += random.uniform(0, avoidance_y)

    def calculate_aviodance(self, coordinate):
        """
        Calculate avoidance based on the position of the sprite.
        """
        # Play with avoidance_weight to make the effect weaker or stronger.
        avoidance_weight = self.speed
        distance_from_zero = coordinate
        distance_from_max = constants.RESOLUTION - coordinate
        # get position
        distance_from_border = min(distance_from_zero, distance_from_max)
        if distance_from_border == 0:
            return 0
        avoidance = (
            avoidance_weight
            - ((avoidance_weight - 1) / (constants.RESOLUTION / 4))
            * distance_from_border
        )
        #  if in the second half of the coordinates, inverse avoidance
        if distance_from_border == distance_from_max:
            avoidance *= -1
        return avoidance

    def stay_inside_walls(self):
        """
        Stops sprite at walls.
        """
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > constants.RESOLUTION - 40:
            self.rect.bottom = constants.RESOLUTION - 40
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500

    def self_collision(self):
        """
        Stops sprites in the same group from colliding.
        """
        for sprite in self.own_group:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                distance_x = self.rect.x - sprite.get_coordinates()[0]
                # distance_X negative --> self is on the left
                if distance_x > 0:
                    self.rect.x += self.speed
                elif distance_x < 0:
                    self.rect.x -= self.speed

                distance_y = self.rect.y - sprite.get_coordinates()[1]
                # distance_y negative --> self is on the top
                if distance_y > 0:
                    self.rect.y += self.speed
                elif distance_y < 0:
                    self.rect.y -= self.speed

    def blit_sprite(self):
        """
        Blits sprite to screen.
        """
        self.screen.blit(self.image, self.rect)
