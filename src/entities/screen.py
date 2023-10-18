"""
Module for the abstract class `Screen`.
"""
import sys
from abc import ABC, abstractmethod
import pygame
from src.utils import constants


class Screen(ABC):
    """
    Abstract base class for managing the 3 screens of the game.
    """

    def __init__(self, screen):
        """
        Initialize the Screen object.

        Args:
            screen (pygame.Surface): The Pygame surface representing the game screen.
        """
        self.current_screen = ""
        self.screen = screen  # The Pygame screen surface
        self.clock = pygame.time.Clock()  # Pygame clock for controlling frame rate
        self.click = False  # Flag to track mouse clicks
        self.is_running = True  # Flag to control the main loop

    def get_current_screen(self):
        """
        Get the name of the current screen to be displayed in the game.

        Returns:
            str: A string representing the current screen, which is used by the
            `Main` class's `run_game` method to determine which screen should be
            displayed.
        """
        return self.current_screen

    def get_is_running(self):
        """
        Get the status indicating if the screen is currently running.

        Returns:
            bool: A boolean value that specifies whether the screen is running.
            Used in the `Main` class's `loop_screen` method to control
            the while loop and determine whether the screen should continue running.
        """
        return self.is_running

    def stop(self):
        """
        Stop the main loop of the screen.

        This method sets the `is_running` flag to `False`.
        """
        self.is_running = False

    def main_loop(self):
        """
        Main loop for managing the screen's rendering and event handling.

        This method performs the following tasks in order:
        1. Resets the `click` flag.
        2. Clears the screen by filling it with background color.
        3. Checks for user inputs.
        4. Calls `sub_loop` abstract method implemented by subclasses.
        5. Updates display.
        6. Limits framerate at 60 FPS.
        This method is responsible for coordinating the screen's operations, including
        updating the display, checking user input events, and managing the frame rate.

        Called within the `Main` class's `loop_screen`.
        """
        self.click = False
        self.blit_background()
        self.check_events()
        self.sub_loop()
        pygame.display.flip()
        self.clock.tick(60)

    def blit_background(self):
        """
        Fills the screen with background color.
        """
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click = True

    @abstractmethod
    def sub_loop(self):
        """
        An abstract method to handle the specific behavior of the screen.

        This method should be implemented in concrete subclasses of the `Screen` class
        to define the behavior and content of the screen. It is called within the `main_loop`
        method to perform screen-specific tasks, such as rendering game elements and handling
        user interactions.
        """
