from src.entities.text_screen import TextScreen


class GameOverScreen(TextScreen):
    def __init__(self, screen, winner):
        super().__init__(screen)
        self.current_screen = "game_over"
        self.winner = winner.upper()

    def sub_loop(self):
        self.blit_text(f"{self.winner} WON", 200, font_size=24)
        restart_rect = self.blit_text("Restart", 300)
        menu_rect = self.blit_text("Main menu", 350)

        self.mouse_interaction(restart_rect, "Restart", self.restart_button)
        self.mouse_interaction(menu_rect, "Main menu", self.menu_button)

    def menu_button(self):
        self.current_screen = "menu"
        self.stop()

    def restart_button(self):
        self.current_screen = "game"
        self.stop()
