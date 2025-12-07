import pygame
import config
from utils.highscore_manager import HighscoreManager


class ScoresScreen:
    def __init__(self, game, previous_screen=None):
        self.game = game
        self.screen = game.screen
        self.previous_screen = previous_screen

        self.bg = pygame.image.load("assets/day.png").convert()

        self.back_btn = pygame.image.load("assets/buttons/back_btn.png").convert_alpha()
        self.back_btn_rect = self.back_btn.get_rect(topleft=(10, 10))

        self.menu_btn = pygame.image.load("assets/buttons/menu_btn.png").convert_alpha()
        self.menu_rect = self.menu_btn.get_rect(
            center=(config.window_width // 2, config.window_height - 80)
        )

        self.title_font = pygame.font.Font(config.font_path, 64)
        self.header_font = pygame.font.Font(config.font_path, 36)
        self.score_font = pygame.font.Font(config.font_path, 34)

        self.scores = HighscoreManager.get_top_scores("manual", 5)

        self.title_text = self.title_font.render("HIGHSCORES", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(config.window_width // 2, 80))

        self.place_text = self.header_font.render("Place", True, (0, 0, 0))
        self.score_text = self.header_font.render("Score", True, (0, 0, 0))


    def update(self):
        return None


    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.back_btn, self.back_btn_rect)

        self.screen.blit(self.place_text, (config.window_width // 2 - 120, 160))
        self.screen.blit(self.score_text, (config.window_width // 2 + 60, 160))

        start_y = 220
        spacing = 42

        if self.scores:
            for i, score in enumerate(self.scores):
                place = self.score_font.render(f"{i+1}.", True, (0, 0, 0))
                value = self.score_font.render(str(score), True, (0, 0, 0))

                self.screen.blit(place, (config.window_width // 2 - 120, start_y + i * spacing))
                self.screen.blit(value, (config.window_width // 2 + 60, start_y + i * spacing))
        else:
            empty_text = self.score_font.render("No scores yet!", True, (0, 0, 0))
            empty_rect = empty_text.get_rect(center=(config.window_width // 2, start_y))
            self.screen.blit(empty_text, empty_rect)

        self.screen.blit(self.menu_btn, self.menu_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.back_btn_rect.collidepoint((mx, my)):
                if self.previous_screen == "game_over":
                    return "back_to_game_over"
                return "menu"

            if self.menu_rect.collidepoint((mx, my)):
                return "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"

        return None
