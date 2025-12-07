import random
import pygame
import config
from ai.brain import Brain
from utils.sound_manager import SoundManager


class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.color = (255, 0, 0)
        bird_color_sets = {
            "yellow": [
                "assets/birds/cropped_bird1.png",
                "assets/birds/cropped_bird2.png",
                "assets/birds/cropped_bird3.png",
            ],
            "blue": [
                "assets/birds/cropped_blue_bird1.png",
                "assets/birds/cropped_blue_bird2.png",
                "assets/birds/cropped_blue_bird3.png",
            ],
            "green": [
                "assets/birds/cropped_green_bird1.png",
                "assets/birds/cropped_green_bird2.png",
                "assets/birds/cropped_green_bird3.png",
            ],
            "orange": [
                "assets/birds/cropped_orange_bird1.png",
                "assets/birds/cropped_orange_bird2.png",
                "assets/birds/cropped_orange_bird3.png",
            ],
            "pink": [
                "assets/birds/cropped_pink_bird1.png",
                "assets/birds/cropped_pink_bird2.png",
                "assets/birds/cropped_pink_bird3.png",
            ],
            "rainbow": [
                "assets/birds/cropped_rainbow_bird1.png",
                "assets/birds/cropped_rainbow_bird2.png",
                "assets/birds/cropped_rainbow_bird3.png",
            ]
        }

        chosen_color = random.choice(list(bird_color_sets.keys()))

        self.frames = [
            pygame.image.load(frame).convert_alpha()
            for frame in bird_color_sets[chosen_color]
        ]

        self.frame = 0
        self.frame_timer = 0
        self.frame_speed = 7

        w = self.frames[0].get_width()
        h = self.frames[0].get_height()
        self.rect = pygame.Rect(self.x, self.y, w, h)

        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = Brain(self.inputs)
        self.brain.generate_net() # initialize the neural network

        self.score = 0

        self.float_offset = 0
        self.float_direction = 1

    def draw(self, window):
        img = self.frames[self.frame]
        window.blit(img, self.rect)

    def ground_collision(self, ground):
        return self.rect.bottom >= ground.y_pos

    def sky_collision(self):
        return self.rect.top <= 0

    def pipe_collision(self):
        for p in config.pipes:
            if self.rect.colliderect(p.top_rect) or self.rect.colliderect(p.bottom_rect):
                return True
        return False

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            self.lifespan += 1
            self.check_score()
        else:
            self.alive = False
            self.flap = False
            self.vel = 0
            SoundManager.play_death()

            # check if the bird passed a pipe
    def check_score(self):
        for p in config.pipes:
            if not p.passed and p.x + p.bottom_rect.width < self.rect.x:
                p.passed = True
                self.score += 1
                SoundManager.play_score()

    # make the bird move upward
    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -6
            SoundManager.play_flap()

        if self.vel >= 3:
            self.flap = False

    # find the pipe with the smallest x coordinate that hasn't been passed
    @staticmethod
    def closest_pipe():
        unpassed = [p for p in config.pipes if not p.passed]
        if unpassed:
            return min(unpassed, key=lambda p: p.x)
        return None

    # AI related functions
    def look(self):
        closest = self.closest_pipe()
        if closest:
            self.vision[0] = max(0, self.rect.center[1] - closest.top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], closest.top_rect.bottom))
        if config.pipes:
            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))

    # send vision to neural network
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.6:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone

    # IDLE FLOAT (before start)
    def idle_float(self):
        self.float_offset += 0.3 * self.float_direction
        if abs(self.float_offset) > 6:
            self.float_direction *= -1
        self.animate()

    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_timer = 0