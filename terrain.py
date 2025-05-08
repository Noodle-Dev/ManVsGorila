# terrain.py

import pygame
from config import WIDTH, HEIGHT, GROUND_COLOR, BG_COLOR

class Terrain:
    def __init__(self):
        self.ground_y = HEIGHT - 100  # Altura del suelo

    def draw(self, screen):
        # Fondo
        screen.fill(BG_COLOR)
        # Suelo rugoso
        pygame.draw.rect(screen, GROUND_COLOR, (0, self.ground_y, WIDTH, HEIGHT - self.ground_y))
        for i in range(0, WIDTH, 40):
            height = 10 + (i % 3) * 3
            pygame.draw.rect(screen, (120, 60, 30), (i, self.ground_y - height, 40, height))
