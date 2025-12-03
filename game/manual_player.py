import pygame


class ManualPlayer:
    def __init__(self):
        self.x = 80
        self.y = 320
        self.vel = 0
        self.gravity = 0.4
        self.jump_power = -7

        self.frame = 0
        self.frame_timer = 0
        self.frame_speed = 7

        self.score = 0

        self.frames = [
            pygame.image.load("assets/cropped_bird1.png").convert_alpha(),
            pygame.image.load("assets/cropped_bird2.png").convert_alpha(),
            pygame.image.load("assets/cropped_bird3.png").convert_alpha(),
        ]

        self.float_offset = 0
        self.float_direction = 1

        w = self.frames[0].get_width()
        h = self.frames[0].get_height()
        self.rect = pygame.Rect(self.x, self.y, w, h)


    # IDLE FLOAT (before start)
    def idle_float(self):
        self.float_offset += 0.3 * self.float_direction
        if abs(self.float_offset) > 6:
            self.float_direction *= -1
        self.animate()


    def update(self, ground):
        self.vel += self.gravity
        self.y += self.vel

        # falling speed
        if self.vel > 8:
            self.vel = 8

        self.animate()


    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_timer = 0


    def draw(self, screen):
        y_pos = self.y + (self.float_offset if self.vel == 0 else 0)

        screen.blit(self.frames[self.frame], (self.x, y_pos))

        img = self.frames[self.frame]
        self.rect.x = self.x
        self.rect.y = y_pos
        self.rect.width = img.get_width()
        self.rect.height = img.get_height()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.vel = self.jump_power


    def get_rect(self):
        return self.rect
