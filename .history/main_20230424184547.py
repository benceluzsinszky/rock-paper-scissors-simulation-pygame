import pygame
import sys

from ch


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

        scissors = 

    def run_game(self):
        """
        Starts the game loop that continues until the user exits the game.
        """
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        """
        Updates the game screen with new information.
        """
        self.screen.fill((255, 255, 255))

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


if __name__ == "__main__":
    game = Game()
    game.run_game()