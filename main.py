import pygame
from sys import exit
import config
from screens.title_screen import TitleScreen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = config.window
        self.clock = pygame.time.Clock()
        self.current_screen = None

        self.pending_mode = None
        self.last_score = 0

    def set_screen(self, screen):
        self.current_screen = screen

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                action = self.current_screen.handle_event(event)
                if action:
                    self.handle_action(action)

            action_from_update = self.current_screen.update()
            if action_from_update:
                self.handle_action(action_from_update)
                continue

            self.current_screen.draw()

            pygame.display.update()
            self.clock.tick(60)


    def handle_action(self, action):

        if action == "manual_tutorial":
            self.pending_mode = "manual"
            from screens.tutorial_screen import TutorialScreen
            self.set_screen(TutorialScreen(self, mode="manual"))

        elif action == "auto_tutorial":
            self.pending_mode = "auto"
            from screens.tutorial_screen import TutorialScreen
            self.set_screen(TutorialScreen(self, mode="auto"))

        elif action == "start_game":
            from screens.game_screen import GameScreen
            self.set_screen(GameScreen(self, mode=self.pending_mode))

        elif action == "game_over":
            from screens.game_over_screen import GameOverScreen
            self.set_screen(GameOverScreen(self, score=self.last_score))

        elif action == "menu":
            from screens.title_screen import TitleScreen
            self.set_screen(TitleScreen(self))

        elif action == "restart":
            from screens.game_screen import GameScreen
            self.set_screen(GameScreen(self, mode=self.pending_mode))

        # Highscore Screen
        elif action == "scores":
            from screens.scores_screen import ScoresScreen
            self.set_screen(ScoresScreen(self))


def main():
    game = Game()
    game.set_screen(TitleScreen(game))
    game.run()


if __name__ == "__main__":
    main()
