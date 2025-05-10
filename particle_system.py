import pygame
import random
from pygame import gfxdraw

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, color, velocity, lifetime):
        self.particles.append({
            'x': x, 'y': y,
            'color': color,
            'vx': velocity[0], 'vy': velocity[1],
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'size': random.randint(2, 5)
        })
    
    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1  # Gravedad
            p['lifetime'] -= 1
            if p['lifetime'] <= 0:
                self.particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = (*p['color'], alpha)
            gfxdraw.filled_circle(
                surface, int(p['x']), int(p['y']), p['size'], color
            )