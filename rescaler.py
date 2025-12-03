import pygame

pygame.init()

pygame.display.set_mode((1, 1))

bg = pygame.image.load("C:/Users/Nicola/Downloads/g.png").convert_alpha()

scale_factor = 3
new_width = bg.get_width() * scale_factor
new_height = bg.get_height() * scale_factor

bg_scaled = pygame.transform.scale(bg, (new_width, new_height))

pygame.image.save(bg_scaled, "C:/Users/Nicola/Downloads/pipe_bottom.png")

print("Saved:", new_width, "x", new_height)
