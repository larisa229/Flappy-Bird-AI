import pygame
import config

class GameOverScreen:
    def __init__(self, game, score, mode="manual"):
        self.game = game
        self.screen = game.screen
        self.score = score
        self.mode = mode

        self.load_assets()
        self.create_ui()


    def load_assets(self):
        self.bg = pygame.image.load("assets/day.png").convert()
        self.ground_img = pygame.image.load("assets/ground.png").convert_alpha()
        self.ground_y = config.window_height - self.ground_img.get_height()
        self.game_over_img = pygame.image.load("assets/game_over.png").convert_alpha()
        self.panel_img = pygame.image.load("assets/medal_score.png").convert_alpha()

        self.btn_restart = pygame.image.load("assets/start_btn.png").convert_alpha()
        self.btn_menu = pygame.image.load("assets/menu_btn.png").convert_alpha()
        self.btn_highscore = pygame.image.load("assets/high_btn.png").convert_alpha()


    def create_ui(self):
        screen_w = self.screen.get_width()
        center_x = screen_w // 2

        self.game_over_rect = self.game_over_img.get_rect(center=(center_x, 120))
        self.panel_rect = self.panel_img.get_rect(center=(center_x, 300))

        self.restart_rect = self.btn_restart.get_rect(center=(center_x - 100, 500))
        self.highscore_rect = self.btn_highscore.get_rect(center=(center_x + 100, 500))
        self.menu_rect = self.btn_menu.get_rect(center=(center_x, 650))


    def update(self):
        return None


    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.game_over_img, self.game_over_rect)
        self.screen.blit(self.panel_img, self.panel_rect)
        self.screen.blit(self.ground_img, (0, self.ground_y))

        # Buttons
        self.screen.blit(self.btn_restart, self.restart_rect)
        self.screen.blit(self.btn_highscore, self.highscore_rect)
        self.screen.blit(self.btn_menu, self.menu_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.restart_rect.collidepoint((mx, my)):
                return "restart"

            if self.highscore_rect.collidepoint((mx, my)):
                return "scores"

            if self.menu_rect.collidepoint((mx, my)):
                return "menu"

        return None
