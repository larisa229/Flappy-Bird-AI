import pygame
import config
from game.pipes import Pipes
from game.ground import Ground
from ai.population import Population
from game.manual_player import ManualPlayer
from utils.highscore_manager import HighscoreManager
from utils.sound_manager import SoundManager

class GameScreen:
    def __init__(self, game, mode="manual"):

        self.game = game
        self.screen = game.screen
        self.mode = mode
        self.score = 0

        config.pipes.clear()
        config.ground = Ground(config.window_width)

        self.pipes_spawn_timer = 30

        if mode == "manual":
            self.player = ManualPlayer()

        if mode == "auto":
            self.population = Population(100)

        self.background = pygame.image.load("assets/day.png").convert()

        self.started = False
        self.get_ready_img = pygame.image.load("assets/text/get_ready.png").convert_alpha()

        center_x = self.screen.get_width() // 2
        self.get_ready_rect = self.get_ready_img.get_rect(center=(center_x, 250))

        self.back_btn = pygame.image.load("assets/buttons/back_btn.png").convert_alpha()
        self.back_btn_rect = self.back_btn.get_rect(topleft=(10, 10))


    def update(self):

        if not self.started:

            if self.mode == "manual":
                self.player.idle_float()

            if self.mode == "auto":
                for p in self.population.players:
                    if p.alive:
                        p.idle_float()

            return None

        self.spawn_pipes()
        self.update_pipes()
        self.update_ground()
        self.update_score()

        action = self.update_players()
        return action


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if not self.started:
            self.screen.blit(self.get_ready_img, self.get_ready_rect)

        for p in config.pipes:
            p.draw(self.screen)

        config.ground.draw(self.screen)

        if self.mode == "manual":
            self.player.draw(self.screen)
        else:
            for p in self.population.players:
                if p.alive:
                    p.draw(self.screen)

        self.draw_score()

        if self.mode == "auto":
            self.screen.blit(self.back_btn, self.back_btn_rect)


    def spawn_pipes(self):

        if self.pipes_spawn_timer <= 0:
            config.pipes.append(Pipes(config.window_width))
            self.pipes_spawn_timer = 120
        else:
            self.pipes_spawn_timer -= 1


    def update_pipes(self):

        for p in list(config.pipes):
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

    def update_ground(self):
        config.ground.update()

    def update_score(self):

        if self.mode == "auto":
            if not self.population.players:
                return

            best = max(self.population.players, key=lambda p: p.score)
            self.score = best.score

        if self.mode == "manual":
            for pipe in config.pipes:
                pipe_right = pipe.x + pipe.bottom_rect.width

                if pipe_right < self.player.rect.left and not pipe.scored:
                    self.score += 1
                    pipe.scored = True
                    SoundManager.play_score()

    def draw_score(self):

        if not self.started:
            return

        font = pygame.font.Font(config.font_path, 56)
        score_surface = font.render(str(self.score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(config.window_width // 2, 60))
        self.screen.blit(score_surface, score_rect)

    def update_players(self):

        if self.mode == "manual":
            if not self.started:
                self.player.idle_float()
            else:
                self.player.update(config.ground)

            if self.check_collision(self.player):
                self.game.last_score = self.score
                HighscoreManager.save_score(self.score, self.mode)
                SoundManager.play_death()
                return "game_over"

            return None


        if self.mode == "auto":

            if not self.started:
                for p in self.population.players:
                    if p.alive:
                        p.idle_float()
                return

            if not self.population.extinct():
                self.population.update_live_players()
            else:
                best = max(self.population.players, key=lambda p: p.score)
                HighscoreManager.save_score(best.score, "auto")
                config.pipes.clear()
                self.pipes_spawn_timer = 30
                self.population.natural_selection()


    def check_collision(self, bird):

        bird_rect = bird.get_rect()

        if bird_rect.bottom >= config.ground.y_pos:
            return True

        for pipe in config.pipes:
            if pipe.collides(bird_rect):
                return True

        return False


    def handle_event(self, event):
        if self.mode == "auto" and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.back_btn_rect.collidepoint((mx, my)):
                return "menu"

        if not self.started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.started = True
            return None

        if self.mode == "manual":
            self.player.handle_event(event)

        return None

