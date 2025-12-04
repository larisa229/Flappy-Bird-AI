import pygame
import random
import config


class Pipes:
    GAP = 200
    SPEED = 2

    def __init__(self, window_width):

        if not hasattr(Pipes, "pipe_bottom_img"):
            Pipes.pipe_bottom_img = pygame.image.load("assets/pipe_bottom.png").convert_alpha()
            Pipes.pipe_top_img = pygame.image.load("assets/pipe_top.png").convert_alpha()

        self.scored = False

        self.x = window_width

        # random gap positioning
        self.gap_y = random.randint(150, config.window_height - 250)

        # bottom pipe positioning
        self.bottom_img = Pipes.pipe_bottom_img
        self.bottom_rect = self.bottom_img.get_rect()
        self.bottom_rect.x = self.x
        self.bottom_rect.top = self.gap_y + Pipes.GAP // 2

        # tyop pipe
        self.top_img = Pipes.pipe_top_img
        self.top_rect = self.top_img.get_rect()
        self.top_rect.x = self.x
        self.top_rect.bottom = self.gap_y - Pipes.GAP // 2

        # tighten collision hitboxes
        HITBOX_INSET = 6  # shrink 6px from both sides

        self.top_rect.inflate_ip(-HITBOX_INSET, -HITBOX_INSET)
        self.bottom_rect.inflate_ip(-HITBOX_INSET, -HITBOX_INSET)

        self.passed = False
        self.off_screen = False

    def update(self):
        self.x -= Pipes.SPEED
        self.bottom_rect.x = self.x
        self.top_rect.x = self.x

        if self.x < -self.bottom_rect.width:
            self.off_screen = True

    def draw(self, window):
        window.blit(self.top_img, self.top_rect)
        window.blit(self.bottom_img, self.bottom_rect)

    def collides(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
