import pygame
import config
from utils.highscore_manager import HighscoreManager

class GameOverScreen:
    def __init__(self, game, score, mode="manual"):
        self.game = game
        self.screen = game.screen
        self.score = score
        self.mode = mode

        self.best_score = HighscoreManager.get_best_score(mode)

        self.load_assets()
        self.create_ui()

        self.font = pygame.font.Font(config.font_path, 42)
        self.medal_img = self.get_medal_for_score(self.score)


    def load_assets(self):
        self.bg = pygame.image.load("assets/day.png").convert()
        self.ground_img = pygame.image.load("assets/ground.png").convert_alpha()
        self.ground_y = config.window_height - self.ground_img.get_height()
        self.game_over_img = pygame.image.load("assets/text/game_over.png").convert_alpha()
        self.panel_img = pygame.image.load("assets/medal_score.png").convert_alpha()

        self.bronze_medal = pygame.image.load("assets/bronze_medal.png").convert_alpha()
        self.silver_medal = pygame.image.load("assets/silver_medal.png").convert_alpha()
        self.gold_medal = pygame.image.load("assets/gold_medal.png").convert_alpha()
        self.platinum_medal = pygame.image.load("assets/platinum_medal.png").convert_alpha()

        self.btn_restart = pygame.image.load("assets/buttons/start_btn.png").convert_alpha()
        self.btn_menu = pygame.image.load("assets/buttons/menu_btn.png").convert_alpha()
        self.btn_highscore = pygame.image.load("assets/buttons/high_btn.png").convert_alpha()


    def create_ui(self):
        screen_w = self.screen.get_width()
        center_x = screen_w // 2

        self.game_over_rect = self.game_over_img.get_rect(center=(center_x, 120))
        self.panel_rect = self.panel_img.get_rect(center=(center_x, 300))

        self.medal_rect = pygame.Rect(0, 0, 90, 90)
        self.medal_rect.center = (self.panel_rect.left + 75,  self.panel_rect.centery + 5)

        self.restart_rect = self.btn_restart.get_rect(center=(center_x - 100, 500))
        self.highscore_rect = self.btn_highscore.get_rect(center=(center_x + 100, 500))
        self.menu_rect = self.btn_menu.get_rect(center=(center_x, 650))


    def get_medal_for_score(self, score):
        if score >= 40:
            return self.platinum_medal
        elif score >= 30:
            return self.gold_medal
        elif score >= 20:
            return self.silver_medal
        elif score >= 10:
            return self.bronze_medal
        else:
            return None


    def update(self):
        return None


    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.game_over_img, self.game_over_rect)
        self.screen.blit(self.panel_img, self.panel_rect)
        self.screen.blit(self.ground_img, (0, self.ground_y))

        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        score_x = self.panel_rect.centerx + 90
        score_y = self.panel_rect.centery - 20
        score_rect = score_text.get_rect(center=(score_x, score_y))
        self.screen.blit(score_text, score_rect)

        if self.medal_img is not None:
            medal_scaled = pygame.transform.scale(self.medal_img, (90, 90))
            self.screen.blit(medal_scaled, self.medal_rect)

        best_score_text = self.font.render(str(self.best_score), True, (255, 255, 255))
        best_score_x = self.panel_rect.centerx + 100
        best_score_y = self.panel_rect.centery + 40
        best_score_rect = best_score_text.get_rect(center=(best_score_x, best_score_y))
        self.screen.blit(best_score_text, best_score_rect)

        self.screen.blit(self.btn_restart, self.restart_rect)
        self.screen.blit(self.btn_highscore, self.highscore_rect)
        self.screen.blit(self.btn_menu, self.menu_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.restart_rect.collidepoint((mx, my)):
                return "restart"

            if self.highscore_rect.collidepoint((mx, my)):
                return "scores_from_game_over"

            if self.menu_rect.collidepoint((mx, my)):
                return "menu"

        return None
