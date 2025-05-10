import pygame
import math
import random
from pygame import gfxdraw
from config import *

class Hombre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.speed = random.uniform(1.0, 1.8)
        self.health = 100
        self.max_health = 100
        self.attack_power = random.randint(4, 8)
        self.color = random.choice(SKIN_TONES)
        self.attack_cooldown = 0
        self.fatigue = 0
        self.trail = []
        self.direction = random.uniform(0, 2*math.pi)
        self.fear = 0
        
    def update(self, gorila, hombres, particles):
        if self.health < 30:
            self.fear = min(1.0, self.fear + 0.02)
        
        dist_to_gorila = math.hypot(gorila.x - self.x, gorila.y - self.y)
        
        if dist_to_gorila < 150 and self.fear < 0.7:
            self.direction = math.atan2(gorila.y - self.y, gorila.x - self.x)
            
            if dist_to_gorila > 80:
                move_dist = min(self.speed * 0.8, dist_to_gorila - 80)
            elif dist_to_gorila < 60:
                move_dist = -self.speed * 0.5
            else:
                self.direction += math.pi/2 * (0.5 if random.random() > 0.5 else -0.5)
                move_dist = self.speed * 0.6
            
            self.x += math.cos(self.direction) * move_dist * (1 - self.fear)
            self.y += math.sin(self.direction) * move_dist * (1 - self.fear)
            
            if 60 <= dist_to_gorila <= 90 and self.attack_cooldown <= 0:
                damage = self.attack_power * (1 - self.fear)
                gorila.health -= damage
                self.attack_cooldown = 25
                
                for _ in range(5):
                    angle = random.uniform(0, 2*math.pi)
                    speed = random.uniform(1, 3)
                    particles.add_particle(
                        gorila.x, gorila.y, BLOOD_COLOR,
                        (math.cos(angle)*speed, math.sin(angle)*speed),
                        random.randint(20, 40)
                    )
        else:
            if self.fear > 0.3 or dist_to_gorila < 120:
                self.direction = math.atan2(self.y - gorila.y, self.x - gorila.x)
            else:
                if hombres:
                    avg_x = sum(h.x for h in hombres) / len(hombres)
                    avg_y = sum(h.y for h in hombres) / len(hombres)
                    self.direction = math.atan2(avg_y - self.y, avg_x - self.x)
            
            self.direction += random.uniform(-0.3, 0.3)
            move_dist = self.speed * (0.5 + self.fear * 0.7)
            self.x += math.cos(self.direction) * move_dist
            self.y += math.sin(self.direction) * move_dist
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.fatigue = min(100, self.fatigue + 0.1)
        if self.fatigue > 80:
            self.speed = max(0.3, self.speed * 0.95)
        
        if not (0 <= self.x <= SIZE):
            self.direction = math.pi - self.direction
        if not (0 <= self.y <= SIZE):
            self.direction = -self.direction
        
        self.x = max(5, min(SIZE-5, self.x))
        self.y = max(5, min(SIZE-5, self.y))
    
    def draw(self, surface):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i+1)/len(self.trail))
            color = (*TRAIL_COLOR, alpha//2)
            gfxdraw.filled_circle(surface, int(tx), int(ty), 3, color)
        
        rect_size = self.size * 2
        rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), rect_size, rect_size)
        pygame.draw.rect(surface, self.color, rect)

        health_width = 20 * (self.health / self.max_health)
        pygame.draw.rect(surface, (0, 0, 0), (self.x-10, self.y-self.size-15, 20, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.x-10, self.y-self.size-15, health_width, 5))