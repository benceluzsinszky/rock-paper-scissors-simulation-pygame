"""
This module defines the `TextScreen` class, which is a subclass of the `Screen` class and designed for
creating the menu and the game over screens.
"""
import pygame
from src.entities.screen import Screen
from src.utils import constants


class TextScreen(Screen):
    """
    A subclass of `Screen` for managing text-based game screens.
    """

    def blit_text(
        self,
        text,
        y_coordinate,
        color=constants.TEXTCOLOR,
        font_size=14,
    ):
        """
        Render and display text on the screen with specified attributes.

        Args:
            text (str): The text to be displayed.
            y_coordinate (int): The vertical coordinate of the text.
            color (tuple): The RGB color value for the text (default: constants.TEXTCOLOR).
            font_size (int): The font size of the text (default: 14).

        Returns:
            pygame.Rect: The rectangular area of the rendered text.
        """
        image = pygame.font.Font(constants.FONT, font_size).render(text, 1, color)
        rect = image.get_rect()
        rect.center = (constants.RESOLUTION / 2, y_coordinate)
        self.screen.blit(image, rect)
        return rect

    def get_mouse_position(self):
        """
        Get the current mouse cursor position on the screen.

        Returns:
            tuple: A tuple (x, y) representing the mouse cursor's coordinates.
        """
        return pygame.mouse.get_pos()

    def mouse_interaction(self, rect, text, method, font_size=14):
        """
        Check and respond to mouse interactions with text on the screen.

        Args:
            rect (pygame.Rect): The rectangular area of the text.
            text (str): The text displayed within the rectangular area.
            method (function): The function to execute when the text is clicked.
            font_size (int): The font size of the text (default: 14).

        - Highlights text when the mouse hovers over it.
        - Executes the specified method when the text is clicked.
        """
        mx, my = self.get_mouse_position()
        # Highlight text colored when mouse is hovered on it
        if rect.collidepoint(mx, my):
            self.blit_text(
                text,
                rect.centery,
                color=constants.TEXTCOLOR_HIGHLIGHTED,
                font_size=font_size,
            )
            if self.click:
                self.click = False
                method()
