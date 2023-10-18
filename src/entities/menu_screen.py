import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from src.entities.text_screen import TextScreen


class MenuScreen(TextScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_screen = "menu"
        self.screen = screen
        self.speed_slider = self.set_up_slider(
            y_coordinate=150, max_value=10, initial_value=2
        )
        self.group_slider = self.set_up_slider(
            y_coordinate=250, max_value=150, initial_value=30
        )

    def get_speed(self):
        return self.speed_slider.getValue()

    def get_group_size(self):
        return self.group_slider.getValue()

    def sub_loop(self):
        speed = self.get_speed()
        group_size = self.get_group_size()
        self.blit_text(f"Speed: {speed}", 185)
        self.blit_text(f"Group size: {group_size}", 285)

        play_rect = self.blit_text("PLAY", 350, font_size=24)
        self.mouse_interaction(play_rect, "PLAY", self.play_button, font_size=24)

        pygame_widgets.update(pygame.event.get())

    def set_up_slider(self, y_coordinate, max_value, initial_value):
        slider = Slider(
            self.screen,
            100,
            y_coordinate,
            300,
            15,
            min=1,
            max=max_value,
            step=1,
            initial=initial_value,
            colour=(166, 208, 221),
            handleColour=(87, 117, 127),
        )
        return slider

    def play_button(self):
        self.speed_slider.hide()
        self.group_slider.hide()
        self.current_screen = "game"
        self.stop()
