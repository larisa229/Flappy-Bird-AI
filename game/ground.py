import pygame
import config

class Ground:
    def __init__(self, window_width):
        self.window_width = window_width

        self.image = pygame.image.load("assets/ground.png").convert_alpha()
        self.height = self.image.get_height()

        self.y_pos = config.window_height - self.height

        # for infinite scrolling
        self.x1 = 0
        self.x2 = self.image.get_width()

    def update(self):
        # Scroll left
        speed = 2
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 <= -self.image.get_width():
            self.x1 = self.x2 + self.image.get_width()
        if self.x2 <= -self.image.get_width():
            self.x2 = self.x1 + self.image.get_width()

    def draw(self, window):
        window.blit(self.image, (self.x1, self.y_pos))
        window.blit(self.image, (self.x2, self.y_pos))
