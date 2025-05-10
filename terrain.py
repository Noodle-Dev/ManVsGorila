import pygame
import random
from config import *

def create_terrain_surface(size):
    terrain = pygame.Surface((size, size))
    terrain.fill(GROUND_COLOR)
    
    for _ in range(20000):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        shade = random.randint(-15, 15)
        color = (
            max(0, min(255, GROUND_COLOR[0] + shade)),
            max(0, min(255, GROUND_COLOR[1] + shade)),
            max(0, min(255, GROUND_COLOR[2] + shade))
        )
        terrain.set_at((x, y), color)
    
    return terrain