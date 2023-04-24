import pygame
import sys
import random

from sprites import Sprite


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

        self.screen = pygame.display.set_mode((500, 500))

        self.rocks = pygame.sprite.Group()
        self.papers = pygame.sprite.Group()
        self.scissors = pygame.sprite.Group()

        self.sprite_groups = [self.rocks, self.papers, self.scissors]

        self.create_sprites("rock", self.rocks)
        # self.create_sprites("paper", self.papers)
        self.create_sprites("scissors", self.scissors)

    def run_game(self):
        """
        Starts the game loop that continues until the user exits the game.
        """
        while True:
            self.check_events()
            # self.rocks.sprites()[0].eat(self)
            self.move_sprites(self.rocks, self.scissors, self.papers)
            self.move_sprites(self.scissors, self.papers)
            self.move_sprites(self.papers, self.rocks)
            self.check_collisions()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        """
        Updates the game screen with new information.
        """
        self.screen.fill((255, 255, 255))

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

    def collision(self, winner, loser, type):
        collision = pygame.sprite.groupcollide(winner, loser, False, True)

        if collision:
            dead_sprite_rect_x = list(collision.values())[0][0].rect.x
            dead_sprite_rect_y = list(collision.values())[0][0].rect.y
            list(collision.keys())[0].closest_food_distance = float("inf")
            sprite = Sprite(self, type, (dead_sprite_rect_x, dead_sprite_rect_y))
            winner.add(sprite)

    def check_collisions(self):
        self.collision(self.rocks, self.scissors, "rock")
        self.collision(self.scissors, self.papers, "scissors")
        self.collision(self.papers, self.rocks, "paper")

    def move_sprites(self, wathced_group, food):
        for sprite in wathced_group:
            sprite.eat(food)

    def create_sprites(self, type, group):
        for _ in range(10):
            random_x = random.randint(10, 490)
            random_y = random.randint(10, 490)
            sprite = Sprite(self, type, (random_x, random_y))
            group.add(sprite)


if __name__ == "__main__":
    game = Game()
    game.run_game()