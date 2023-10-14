import random
import pygame
from src.entities.screen import Screen
from src.entities.my_sprite import MySprite
from src.entities.score_bar import ScoreBar
from src.utils import constants


class GameScreen(Screen):
    def __init__(self, screen, speed, group_size):
        super().__init__(screen)
        self.screen = screen
        self.speed = speed
        self.group_size = group_size
        self.rocks = pygame.sprite.Group()
        self.papers = pygame.sprite.Group()
        self.scissors = pygame.sprite.Group()
        self.sprite_groups = [self.rocks, self.papers, self.scissors]

        self.rock_score = ScoreBar(self.screen, constants.ROCK_COLOR)
        self.paper_score = ScoreBar(self.screen, constants.PAPER_COLOR)
        self.scissors_score = ScoreBar(self.screen, constants.SCISSORS_COLOR)

        self.winner_group = None

        self.create_sprites("rock", self.rocks, self.papers, self.scissors)
        self.create_sprites("paper", self.papers, self.scissors, self.rocks)
        self.create_sprites("scissors", self.scissors, self.rocks, self.papers)

    def get_winner(self):
        return self.winner_group.sprites()[0].get_sprite_text()

    def sub_loop(self):
        self.update_sprites()
        self.draw_score_bars()

    def update_sprites(self):
        for group in self.sprite_groups:
            self.check_winner(group)
            for sprite in group:
                sprite.update_sprite()
                sprite.blit_sprite()

    def check_winner(self, group):
        if len(group) == self.group_size * 3:
            self.winner_group = group
            self.current_screen = "game_over"
            self.stop()

    def create_sprites(self, image, own_group, hunter_group, prey_group):
        """
        Generates initial sprites.
        """
        for _ in range(self.group_size):
            random_x = random.randint(10, 490)
            random_y = random.randint(10, 490)
            sprite = MySprite(self.screen,
                              image,
                              (random_x, random_y),
                              self.speed,
                              own_group,
                              hunter_group,
                              prey_group)
            own_group.add(sprite)

    def draw_score_bars(self):
        """
        Draw score bars on the bottom.
        """
        multipilier = constants.RESOLUTION / (self.group_size * 3)

        len_rocks = len(self.rocks) * multipilier
        len_papers = len(self.papers) * multipilier

        self.rock_score.draw(0, len_rocks)
        self.paper_score.draw(len_rocks, len_papers)
        self.scissors_score.draw(len_rocks+len_papers-2, constants.RESOLUTION)
