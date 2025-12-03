import pygame
from game.ground import Ground

window_height = 768
window_width = 429
window = pygame.display.set_mode((window_width, window_height))

ground = Ground(window_width)
pipes = []
