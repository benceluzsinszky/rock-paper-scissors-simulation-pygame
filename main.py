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

    def collision(self, wached_group, loser_group, type):
        self_collision = pygame.sprite.groupcollide(
            wached_group, wached_group, False, False)
        if self_collision:
            ...

        collision = pygame.sprite.groupcollide(
            wached_group, loser_group, False, True)

        if collision:
            dead_sprite_rect_x = list(collision.values())[0][0].rect.x
            dead_sprite_rect_y = list(collision.values())[0][0].rect.y
            sprite = Sprite(
                self, type, (dead_sprite_rect_x, dead_sprite_rect_y))
            wached_group.add(sprite)

    def check_collisions(self):
        self.collision(self.rocks, self.scissors, "rock")
        self.collision(self.scissors, self.papers, "scissors")
        self.collision(self.papers, self.rocks, "paper")

    def move_sprites(self, current, food, enemy):
        for sprite in current:
            sprite.action(current, food, enemy)

    def create_sprites(self, type, group):
        for _ in range(STARTING_SPRITES):
            random_x = random.randint(10, 490)
            random_y = random.randint(10, 490)
            sprite = Sprite(self, type, (random_x, random_y))
            group.add(sprite)

    def draw_score(self):
        multipilier = RESX / (STARTING_SPRITES * 3)  # TODO: counting is off

        len_rocks = len(self.rocks) * multipilier
        len_papers = len(self.papers) * multipilier
        len_scissors = len(self.scissors) * multipilier

        pygame.draw.rect(self.screen, 'red', [0, RESY-25, len_rocks, RESY])
        pygame.draw.rect(self.screen, 'green', [
                         len_rocks, RESY-25, len_papers, RESY])
        pygame.draw.rect(self.screen, 'blue', [
                         len_rocks+len_papers, RESY-25, RESX, RESY])

        # rock_image = pygame.image.load("sprites/rock.png")
        # rock_image = pygame.transform.scale(rock_image, (25, 25))
        # paper_image = pygame.image.load("sprites/paper.png")
        # paper_image = pygame.transform.scale(paper_image, (25, 25))
        # scissors_image = pygame.image.load("sprites/scissors.png")
        # scissors_image = pygame.transform.scale(scissors_image, (25, 25))

        # if len_rocks > 0:
        #     self.screen.blit(rock_image, [len_rocks/2-20, RESY-40])
        # if len_papers > 0:
        #     self.screen.blit(
        #         paper_image, [len_rocks+len_papers-len_papers/2-20, RESY-40])
        # if len_scissors > 0:
        #     self.screen.blit(scissors_image, [
        #                      len_rocks+len_papers+len_scissors-len_scissors/2-20, RESY-40])


if __name__ == "__main__":
    game = Game()
    game.run_game()
