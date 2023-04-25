import pygame
import sys
import random

from sprites import Sprite

RESX = RESY = 500

STARTING_SPRITES = 50


class Game():
    """
    This class initializes the Pygame module and creates the game screen.
    """

    def __init__(self) -> None:
        """
        Initializes Pygame module and creates game screen.
        """
        pygame.init()

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Rock Paper Scissors")

        self.screen = pygame.display.set_mode((RESX, RESY))

        self.rocks = pygame.sprite.Group()
        self.papers = pygame.sprite.Group()
        self.scissors = pygame.sprite.Group()

        self.sprite_groups = [self.rocks, self.papers, self.scissors]

        self.create_sprites("rock", self.rocks)
        self.create_sprites("paper", self.papers)
        self.create_sprites("scissors", self.scissors)

    def run_game(self):
        """
        Starts the game loop that continues until the user exits the game.
        """
        while True:
            self.check_events()
            # self.rocks.sprites()[0].eat(self.scissors)
            self.move_sprites(self.rocks, self.scissors, self.papers)
            self.move_sprites(self.scissors, self.papers, self.rocks)
            self.move_sprites(self.papers, self.rocks, self.scissors)
            self.check_collisions()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        """
        Updates the game screen with new information.
        """
        self.screen.fill((255, 255, 255))
        self.draw_score()

        for group in self.sprite_groups:
            for sprite in group:
                sprite.blit_sprite()

        pygame.display.flip()

    def check_events(self):
        """
        Checks for user input events such as key presses or window close events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def collision(self, hunter_group, food_group, type):
        """
        Kills food sprite, creates a new sprite in the 'hunter' group
        """
        for hunter in hunter_group:
            for food in food_group:
                collision = pygame.sprite.collide_rect(
                    hunter, food)

                if collision:
                    sprite = Sprite(
                        self, type, (food.rect.x, food.rect.y))
                    hunter_group.add(sprite)
                    food.kill()

    def check_collisions(self):
        """
        Check for collisions between sprite groups.
        """
        self.collision(self.rocks, self.scissors, "rock")
        self.collision(self.scissors, self.papers, "scissors")
        self.collision(self.papers, self.rocks, "paper")

    def move_sprites(self, current, food, enemy):
        """
        Makes sprites move.
        """
        for sprite in current:
            sprite.action(current, food, enemy)

    def create_sprites(self, type, group):
        """
        Generates initial sprites.
        """
        for _ in range(STARTING_SPRITES):
            random_x = random.randint(10, 490)
            random_y = random.randint(10, 490)
            sprite = Sprite(self, type, (random_x, random_y))
            group.add(sprite)

    def draw_score(self):
        """
        Draw score lines on the bottom.
        """
        multipilier = RESX / (STARTING_SPRITES * 3)

        len_rocks = len(self.rocks) * multipilier
        len_papers = len(self.papers) * multipilier

        pygame.draw.rect(self.screen, (166, 208, 221), [0, RESY-25, len_rocks, RESY])
        pygame.draw.rect(self.screen, (255, 211, 176), [
                         len_rocks, RESY-25, len_papers, RESY])
        pygame.draw.rect(self.screen, (255, 105, 105), [
                         len_rocks+len_papers, RESY-25, RESX, RESY])


if __name__ == "__main__":
    game = Game()
    game.run_game()
