"""
This module defines the `MySprite` class, which represents a Rock, Paper or Scissor sprite in the game.
It extends the `Sprite` class from the `pygame.sprite` module and
includes methods for sprite behavior, movement, and interactions.
"""
import math
import random
import pygame
from pygame.sprite import Sprite
from src.utils import constants


class MySprite(Sprite):
    """
    A class for managing Rock, Paper, Scissor sprites in the game.
    """

    def __init__(
        self, screen, image, location, speed, own_group, hunter_group, prey_group
    ):
        """
        Initialize a single sprite with the provided parameters.

        Args:
            screen (pygame.Surface): The Pygame surface representing the game screen.
            image (str): The type of sprite (rock, paper, or scissors).
            location (tuple): The initial location of the sprite (x, y).
            speed (float): The speed at which the sprite moves.
            own_group (pygame.sprite.Group): The sprite's own group for tracking.
            hunter_group (pygame.sprite.Group): The group of sprites to avoid.
            prey_group (pygame.sprite.Group): The group of sprites to target.
        """
        super().__init__()
        self.screen = screen
        self.sprite_text = image
        self.image = pygame.image.load(f"assets/sprites/{self.sprite_text}.png")
        self.size = 15
        self.rect = self.create_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.speed = speed
        self.own_group = own_group
        self.hunter_group = hunter_group
        self.prey_group = prey_group

    def get_coordinates(self):
        """
        Get the current coordinates of the sprite.

        Returns:
            tuple: A tuple containing the x and y coordinates of the sprite.
        """
        return (self.rect.x, self.rect.y)

    def get_rect(self):
        """
        Get the pygame rect of the sprite.

        Returns:
            pygame.Rect: The pygame Rect representing the sprite's position and dimensions.
        """
        return self.rect

    def get_sprite_text(self):
        """
        Get the type of the sprite (rock, paper, or scissors).
        Used to load the image of the sprite and for the initialization of a `GameOverScreen` object.

        Returns:
            str: The type of the sprite.
        """
        return self.sprite_text

    def get_coordinate_distances(self, sprite):
        """
        Calculate the distance between this sprite and another sprite in terms of x and y coordinates.

        Args:
            sprite (MySprite): The other sprite for which to calculate the distance.

        Returns:
            tuple: A tuple containing the distance in x and y directions.
        """
        sprite_coordinates = sprite.get_coordinates()
        distance_x = sprite_coordinates[0] - self.rect.x
        distance_y = sprite_coordinates[1] - self.rect.y
        return distance_x, distance_y

    def get_distance(self, sprite):
        """
        Calculate the Euclidean distance between this sprite and another sprite.

        Args:
            sprite (MySprite): The other sprite for which to calculate the distance.

        Returns:
            float: The distance between the two sprites.
        """
        distance_x, distance_y = self.get_coordinate_distances(sprite)
        return math.sqrt(distance_x**2 + distance_y**2)

    def get_closest(self, group):
        """
        Find the closest sprite within a group to this sprite.

        Args:
            group (pygame.sprite.Group): The group of sprites to search for the closest one.

        Returns:
            MySprite: The closest sprite found in the group.
        """
        closest_sprite = None
        closest_distance = float("inf")
        for sprite in group:
            distance = self.get_distance(sprite)
            if distance < closest_distance:
                closest_distance = distance
                closest_sprite = sprite
        return closest_sprite

    def set_groups(self, own_group, hunter_group, prey_group):
        """
        Set the groups for this sprite.

        Args:
            own_group (pygame.sprite.Group): The sprite's own group for tracking.
            hunter_group (pygame.sprite.Group): The group of sprites to avoid.
            prey_group (pygame.sprite.Group): The group of sprites to target.
        """
        self.own_group = own_group
        self.hunter_group = hunter_group
        self.prey_group = prey_group

    def set_image(self, image):
        """
        Set the sprite's image.

        Args:
            image (pygame.Surface): The new image for the sprite.
        """
        self.image = image
        self.create_rect()

    def create_rect(self):
        """
        Create a pygame rect for the sprite based on its image.

        Returns:
            pygame.Rect: The pygame Rect representing the sprite's position and dimensions.
        """
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((255, 255, 255))
        return self.image.get_rect()

    def update_sprite(self):
        """
        Update the sprite's position and behavior.
        """
        self.move_sprite()
        self.self_collision()
        self.check_walls()

    def move_sprite(self):
        """
        Move the sprite based on its interactions with other sprites.
        """
        closest_prey = self.get_closest(self.prey_group)
        if closest_prey:
            self.chase(closest_prey, 1)
            self.eat(closest_prey)

        closest_hunter = self.get_closest(self.hunter_group)
        if closest_hunter:
            if self.hunter_close_by(closest_hunter):
                self.chase(closest_hunter, -0.95)

    def chase(self, sprite, direction):
        """
        Make the sprite chase or evade another sprite.

        Args:
            sprite (MySprite): The target sprite to chase or evade.
            direction (float): The chase direction (positive for chasing, negative for evading).
        """
        distance = self.get_distance(sprite)
        if distance == 0:
            return
        distance_x, distance_y = self.get_coordinate_distances(sprite)
        movement = (direction * random.uniform(self.speed * 0.7, self.speed)) / distance
        self.rect.x += distance_x * movement
        self.rect.y += distance_y * movement

    def hunter_close_by(self, hunter):
        """
        Check if a hunter sprite is close by.

        Args:
            hunter (MySprite): The hunter sprite to check.

        Returns:
            bool: True if a hunter sprite is close by; otherwise, False.
        """
        distance = self.get_distance(hunter)
        return distance < 200

    def eat(self, prey):
        """
        Make the sprite eat another sprite.

        Args:
            prey (MySprite): The prey sprite to eat.
        """
        distance_x, distance_y = self.get_coordinate_distances(prey)
        hitbox = self.size * 0.7

        if not (abs(distance_x) <= hitbox and abs(distance_y) <= hitbox):
            return

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
        sprite.blit_sprite()
        prey.kill()

    def check_walls(self):
        """
        Check for collisions with walls and make the sprite avoid them.
        """
        self.avoid_walls()
        self.stay_inside_walls()

    def avoid_walls(self):
        """
        Make the sprite avoid screen borders.

        This method applies a dynamic avoidance effect to the sprite to prevent it from
        getting too close to the screen borders.
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

        Args:
            coordinate (int): The coordinate value (x or y) for which to calculate avoidance.

        Returns:
            float: The avoidance factor to prevent the sprite from getting too close to walls.
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
        Stops the sprite from moving outside the game screen boundaries.

        If the sprite's position exceeds the game screen boundaries (top, bottom, left, or right),
        this method adjusts its position to keep it within the valid area.
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
        Renders the sprite on the game screen.

        This method blits (renders) the sprite's image onto the game screen at its current position.
        The image is placed within the boundaries of the sprite's pygame Rect.
        """
        self.screen.blit(self.image, self.rect)
