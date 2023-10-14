import sys
from abc import ABC, abstractmethod
import pygame
from src.utils import constants


class Screen(ABC):
    """
    Create Pygame Window.
    """
    def __init__(self, screen):
        self.current_screen = ""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.click = False
        self.is_running = True

    def get_current_screen(self):
        return self.current_screen

    def get_is_running(self):
        return self.is_running

    def stop(self):
        self.is_running = False

    def main_loop(self):
        self.click = False
        self.blit_background()
        self.check_events()
        self.sub_loop()
        pygame.display.flip()
        self.clock.tick(60)

    def blit_background(self):
        self.screen.fill(constants.BGCOLOR)

    def check_events(self):
        """
        Checks for user input events such as key presses or window close events.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click = True

    @abstractmethod
    def sub_loop(self):
        pass
