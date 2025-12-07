import pygame

class TutorialScreen:
    def __init__(self, game, mode="manual"):
        self.game = game
        self.screen = game.screen
        self.mode = mode
        self.load_assets()
        self.create_ui()

        self.bird_offset = 0
        self.bird_direction = 1
        self.bird_frame_counter = 0
        self.current_bird_frame = 0


    def load_assets(self):

        self.background = pygame.image.load("assets/day.png").convert()

        self.bird_frames = [
            pygame.image.load("assets/birds/bird1.png").convert_alpha(),
            pygame.image.load("assets/birds/bird2.png").convert_alpha(),
            pygame.image.load("assets/birds/bird3.png").convert_alpha(),
        ]

        if self.mode == "manual":
            self.tutorial_text = pygame.image.load("assets/text/manual_text.png").convert_alpha()
            self.tap_icon = pygame.image.load("assets/tap_tut.png").convert_alpha()
        else:
            self.tutorial_text = pygame.image.load("assets/text/auto_tut.png").convert_alpha()
            self.tap_icon = None

        self.start_btn = pygame.image.load("assets/buttons/start_btn.png").convert_alpha()
        self.back_btn = pygame.image.load("assets/buttons/back_btn.png").convert_alpha()

    def create_ui(self):
        screen_w = self.screen.get_width()
        center_x = screen_w // 2

        if self.mode == "manual":
            self.tutorial_rect = self.tutorial_text.get_rect(center=(center_x, 260))
        else:
            self.tutorial_rect = self.tutorial_text.get_rect(center=(center_x, 320))

        self.bird_rect = self.bird_frames[0].get_rect(center=(center_x, 100))

        if self.mode == "manual":
            self.tap_rect = self.tap_icon.get_rect(center=(center_x, 450))
        else:
            self.tap_rect = None

        self.start_rect = self.start_btn.get_rect(center=(center_x, 650))
        self.back_rect = self.back_btn.get_rect(topleft=(10, 10))

    def update(self):

        self.bird_offset += 0.3 * self.bird_direction
        if abs(self.bird_offset) > 6:
            self.bird_direction *= -1

        self.bird_frame_counter += 1
        if self.bird_frame_counter > 10:
            self.current_bird_frame = (self.current_bird_frame + 1) % 3
            self.bird_frame_counter = 0


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.tutorial_text, self.tutorial_rect)

        if self.mode == "manual" and self.tap_rect:
            self.screen.blit(self.tap_icon, self.tap_rect)

        bird_rect = self.bird_rect.copy()
        bird_rect.y += int(self.bird_offset)
        self.screen.blit(self.bird_frames[self.current_bird_frame], bird_rect)

        self.screen.blit(self.start_btn, self.start_rect)
        self.screen.blit(self.back_btn, self.back_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.start_rect.collidepoint((mx, my)):
                return "start_game"

            if self.back_rect.collidepoint((mx, my)):
                return "menu"


