import pygame
from src.entities.screen import Screen
from src.utils import constants


class TextScreen(Screen):
    def blit_text(
        self,
        text,
        y_coordinate,
        color=constants.TEXTCOLOR,
        font_size=14,
    ):
        image = pygame.font.Font(constants.FONT, font_size).render(text, 1, color)
        rect = image.get_rect()
        rect.center = (constants.RESOLUTION / 2, y_coordinate)
        self.screen.blit(image, rect)
        return rect

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

    def mouse_interaction(self, rect, text, method, font_size=14):
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
