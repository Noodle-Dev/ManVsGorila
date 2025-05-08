# hombre.py

import pygame
from config import GRAVITY, HEIGHT
from particle_system import ParticleSystem

class Hombre:
    def __init__(self, x, y, particles: ParticleSystem):
        self.rect = pygame.Rect(x, y, 30, 50)
        self.vel_y = 0
        self.on_ground = False
        self.particles = particles
        self.last_footprint_time = 0

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= 4
        if keys[pygame.K_d]:
            self.rect.x += 4
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = -9
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True

    def update(self, keys, time):
        self.handle_input(keys)
        self.apply_gravity()

        # Huellas al caminar
        if self.on_ground and (keys[pygame.K_a] or keys[pygame.K_d]):
            if time - self.last_footprint_time > 200:
                self.particles.add_footprint(self.rect.midbottom)
                self.last_footprint_time = time

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 200), self.rect)
