# particle_system.py

import pygame
import random
from config import BLOOD_COLOR, FOOTPRINT_COLOR

class Particle:
    def __init__(self, pos, color, lifetime=30, size=3):
        self.pos = list(pos)
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.lifetime = lifetime
        self.size = size
        self.color = color

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def blood_splash(self, pos, amount=10):
        for _ in range(amount):
            self.particles.append(Particle(pos, BLOOD_COLOR, lifetime=random.randint(20, 40)))

    def add_footprint(self, pos):
        self.particles.append(Particle(pos, FOOTPRINT_COLOR, lifetime=60, size=2))
