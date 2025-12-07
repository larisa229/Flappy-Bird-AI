import pygame

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.load_assets()
        self.create_ui()

        self.bird_offset = 0
        self.bird_direction = 1
        self.bird_frame_counter = 0
        self.current_bird_frame = 0


    def load_assets(self):
        self.background = pygame.image.load("assets/day.png").convert()
        self.title_img = pygame.image.load("assets/text/title.png").convert_alpha()

        self.bird_frames = [
            pygame.image.load("assets/birds/bird1.png").convert_alpha(),
            pygame.image.load("assets/birds/bird2.png").convert_alpha(),
            pygame.image.load("assets/birds/bird3.png").convert_alpha(),
        ]

        self.btn_manual = pygame.image.load("assets/buttons/manual_btn.png").convert_alpha()
        self.btn_auto = pygame.image.load("assets/buttons/auto_btn.png").convert_alpha()
        self.btn_scores = pygame.image.load("assets/buttons/highscore_btn.png").convert_alpha()


    def create_ui(self):
        screen_w = self.screen.get_width()
        center_x = screen_w // 2

        self.title_rect = self.title_img.get_rect(center=(center_x, 210))
        self.bird_rect = self.bird_frames[0].get_rect(center=(center_x, 290))

        self.manual_rect = self.btn_manual.get_rect(center=(center_x, 420))
        self.auto_rect   = self.btn_auto.get_rect(center=(center_x, 480))
        self.scores_rect = self.btn_scores.get_rect(center=(center_x, 540))


    def update(self):
        self.bird_offset += 0.3 * self.bird_direction
        if abs(self.bird_offset) > 8:
            self.bird_direction *= -1

        self.bird_frame_counter += 1
        if self.bird_frame_counter > 10:
            self.current_bird_frame = (self.current_bird_frame + 1) % 3
            self.bird_frame_counter = 0


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_img, self.title_rect)

        bird_rect = self.bird_rect.copy()
        bird_rect.y += int(self.bird_offset)
        self.screen.blit(self.bird_frames[self.current_bird_frame], bird_rect)

        self.screen.blit(self.btn_manual, self.manual_rect)
        self.screen.blit(self.btn_auto, self.auto_rect)
        self.screen.blit(self.btn_scores, self.scores_rect)

        self.font = pygame.font.Font("assets/ByteBounce.ttf", 25)
        text = self.font.render("© 2025 Skinny Legends Studios", True, (255, 255, 255))
        self.screen.blit(text, (10, self.screen.get_height() - 30))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.manual_rect.collidepoint((mx, my)):
                return "manual_tutorial"

            if self.auto_rect.collidepoint((mx, my)):
                return "auto_tutorial"

            if self.scores_rect.collidepoint((mx, my)):
                return "scores"

