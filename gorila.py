import pygame
import math
import random
from pygame import gfxdraw
from config import *

class Gorila:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 45
        self.speed = 1.2
        self.health = 800
        self.max_health = 800
        self.attack_power = 35
        self.color = GORILA_COLOR
        self.attack_cooldown = 0
        self.rage = 0
        self.trail = []
        self.target = None
    
    def update(self, hombres, particles):
        if hombres:
            self.target = min(
                hombres,
                key=lambda h: math.hypot(h.x-self.x, h.y-self.y) - h.health*0.5
            )
            
            dx = self.target.x - self.x + random.uniform(-30, 30)
            dy = self.target.y - self.y + random.uniform(-30, 30)
            dist = max(1, math.hypot(dx, dy))
            
            current_speed = self.speed * (1 + self.rage * 0.5)
            
            self.x += (dx / dist) * current_speed
            self.y += (dy / dist) * current_speed
            
            if dist < 100 and self.attack_cooldown <= 0:
                self.atacar(hombres, particles)
                self.attack_cooldown = 40 - self.rage*10
                self.rage = min(1.0, self.rage + 0.1)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.rage = max(0, self.rage - 0.005)
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)
        
        self.x = max(self.size, min(SIZE-self.size, self.x))
        self.y = max(self.size, min(SIZE-self.size, self.y))
    
    def atacar(self, hombres, particles):
        for hombre in hombres[:]:
            dist = math.hypot(hombre.x-self.x, hombre.y-self.y)
            if dist < 110:
                damage = self.attack_power * (1.2 - dist/110) * (0.8 + self.rage*0.4)
                hombre.health -= damage
                
                if damage > 5:
                    for _ in range(int(damage//3)):
                        angle = random.uniform(0, 2*math.pi)
                        speed = random.uniform(1, 5)
                        particles.add_particle(
                            hombre.x, hombre.y, BLOOD_COLOR,
                            (math.cos(angle)*speed, math.sin(angle)*speed),
                            random.randint(20, 50)
                        )
                
                if hombre.health <= 0:
                    hombres.remove(hombre)
                    for _ in range(15):
                        angle = random.uniform(0, 2*math.pi)
                        speed = random.uniform(1, 6)
                        particles.add_particle(
                            hombre.x, hombre.y, BLOOD_COLOR,
                            (math.cos(angle)*speed, math.sin(angle)*speed),
                            random.randint(30, 60)
                        )
    
    def draw(self, surface):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(200 * (i+1)/len(self.trail))
            color = (*GORILA_COLOR, alpha//3)
            gfxdraw.filled_circle(surface, int(tx), int(ty), 8, color)
        
        rect_size = self.size * 2
        rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), rect_size, rect_size)
        pygame.draw.rect(surface, self.color, rect)

        eye_color = (
            min(255, 150 + 105*self.rage), 
            50, 
            50
        )
        left_eye = (int(self.x-10), int(self.y-5))
        right_eye = (int(self.x+10), int(self.y-5))
        gfxdraw.filled_circle(surface, *left_eye, 5 + int(3*self.rage), eye_color)
        gfxdraw.filled_circle(surface, *right_eye, 5 + int(3*self.rage), eye_color)
        
        health_width = 40 * (max(0, self.health) / self.max_health)
        pygame.draw.rect(surface, (0, 0, 0), (self.x-20, self.y-self.size-25, 40, 10))
        
        health_ratio = max(0, min(1, self.health / self.max_health))
        health_color = (
            int(255 * (1 - health_ratio)),
            int(255 * health_ratio),
            0
        )
        pygame.draw.rect(surface, health_color, (self.x-20, self.y-self.size-25, health_width, 10))