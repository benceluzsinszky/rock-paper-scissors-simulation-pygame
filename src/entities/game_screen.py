"""
This module defines the `GameScreen` class, which represents the display of the simulation.
It extends the `Screen` class.
"""
import random
import pygame
from src.entities.screen import Screen
from src.entities.my_sprite import MySprite
from src.entities.score_bar import ScoreBar
from src.utils import constants


class GameScreen(Screen):
    """
    A class for managing the game screen in a Rock, Paper, Scissors simulation.
    """

    def __init__(self, screen, speed, group_size):
        """
        Initialize a `GameScreen` object.

        Args:
            screen (pygame.Surface): The Pygame surface representing the game screen.
            speed (int): The speed of the sprites.
            group_size (int): The number of sprites in each contender group.
        """
        super().__init__(screen)  # Initialize the parent class (Screen)
        self.screen = screen  # Pygame screen surface
        self.speed = speed  # Speed of sprite movement
        self.group_size = group_size  # Size of each group of sprites
        self.rocks = pygame.sprite.Group()  # Group for rock sprites
        self.papers = pygame.sprite.Group()  # Group for paper sprites
        self.scissors = pygame.sprite.Group()  # Group for scissor sprites
        self.sprite_groups = [
            self.rocks,
            self.papers,
            self.scissors,
        ]  # List of sprite groups

        # Initialize score bars with the appropriate colors
        self.rock_score = ScoreBar(self.screen, constants.ROCK_COLOR)
        self.paper_score = ScoreBar(self.screen, constants.PAPER_COLOR)
        self.scissors_score = ScoreBar(self.screen, constants.SCISSORS_COLOR)

        self.winner_group = None  # Initialize the winner group as None

        # Create initial sprites for rock, paper, and scissor groups
        self.create_sprites("rock", self.rocks, self.papers, self.scissors)
        self.create_sprites("paper", self.papers, self.scissors, self.rocks)
        self.create_sprites("scissors", self.scissors, self.rocks, self.papers)

    def get_winner(self):
        """
        Get the text representing the winning sprite type.
        String used in `Main` class, for initalizing `GameOverScreen` object.

        Returns:
            str: A string representing the winning sprite type (rock, paper, or scissors).
        """
        return self.winner_group.sprites()[0].get_sprite_text()

    def sub_loop(self):
        """
        Manage the game screen's content and interactions.
        """
        self.update_sprites()
        self.draw_score_bars()

    def update_sprites(self):
        """
        Update the positions of all sprites and render them on the screen.

        This method iterates through the sprite groups, checks if a group has won,
        and updates and renders individual sprites.
        """
        for group in self.sprite_groups:
            self.check_winner(group)
            for sprite in group:
                sprite.update_sprite()
                sprite.blit_sprite()

    def check_winner(self, group):
        """
        This method determines the winning sprite group when it reaches the required size.

        Args:
            group (pygame.sprite.Group): The sprite group to be checked for victory.
        """
        if len(group) == self.group_size * 3:
            self.winner_group = group
            self.current_screen = "game_over"
            self.stop()

    def create_sprites(self, image, own_group, hunter_group, prey_group):
        """
        This method is called to initialize the game with a set of sprites.

        Args:
            image (str): The type of sprite to create (rock, paper, or scissors).
            own_group (pygame.sprite.Group): The sprite group to which the new sprites will belong.
            hunter_group (pygame.sprite.Group): The group of sprites that the new sprites will target.
            prey_group (pygame.sprite.Group): The group of sprites that the new sprites will avoid.
        """
        for _ in range(self.group_size):
            random_x = random.randint(10, 490)
            random_y = random.randint(10, 490)
            sprite = MySprite(
                self.screen,
                image,
                (random_x, random_y),
                self.speed,
                own_group,
                hunter_group,
                prey_group,
            )
            own_group.add(sprite)

    def draw_score_bars(self):
        """
        Draw score bars at the bottom of the screen.

        This method calculates the positions and lengths of the score bars for each sprite type
        and then draws them on the game screen. The score bars represent the progress of each sprite group.

        """
        multipilier = constants.RESOLUTION / (self.group_size * 3)

        len_rocks = len(self.rocks) * multipilier
        len_papers = len(self.papers) * multipilier

        self.rock_score.draw(0, len_rocks)
        self.paper_score.draw(len_rocks, len_papers)
        self.scissors_score.draw(len_rocks + len_papers - 2, constants.RESOLUTION)
