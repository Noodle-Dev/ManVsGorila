# gorila.py

import pygame
from config import GRAVITY, HEIGHT
from particle_system import ParticleSystem

class Gorila:
    def __init__(self, x, y, particles: ParticleSystem):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False
        self.particles = particles
        self.last_footprint_time = 0

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -10
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

        # Generar huellas si se mueve
        if self.on_ground and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            if time - self.last_footprint_time > 150:
                self.particles.add_footprint(self.rect.midbottom)
                self.last_footprint_time = time

        # Simular sangre al caer de gran altura
        if self.vel_y > 15:
            self.particles.blood_splash(self.rect.midbottom, amount=20)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 0, 0), self.rect)
