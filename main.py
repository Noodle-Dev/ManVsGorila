import pygame
import random
import math
import sys
from pygame import gfxdraw

# Inicialización
pygame.init()
SIZE = 1000  # Ventana más grande para mejor visualización
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Simulación Realista: 100 Hombres vs Gorila")
clock = pygame.time.Clock()

# Colores y texturas
SKIN_TONES = [
    (232, 190, 172), (210, 180, 140), (170, 140, 110),
    (160, 120, 90), (140, 90, 60), (90, 60, 40)
]
GORILA_COLOR = (80, 80, 80)
BLOOD_COLOR = (150, 30, 30)
GROUND_COLOR = (100, 80, 60)
TRAIL_COLOR = (120, 100, 80)

# Sistema de partículas para efectos
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

# Clase para los hombres (representación más realista)
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
        self.fatigue = 0  # Cansancio acumulado
        self.trail = []  # Para dejar huellas
        self.direction = random.uniform(0, 2*math.pi)
        self.fear = 0  # Nivel de miedo
        
    def update(self, gorila, hombres, particles):
        # Comportamiento basado en estado emocional
        if self.health < 30:
            self.fear = min(1.0, self.fear + 0.02)
        
        dist_to_gorila = math.hypot(gorila.x - self.x, gorila.y - self.y)
        
        # Toma de decisiones
        if dist_to_gorila < 150 and self.fear < 0.7:
            # Modo ataque (cauteloso)
            self.direction = math.atan2(gorila.y - self.y, gorila.x - self.x)
            
            # Distancia óptima de ataque
            if dist_to_gorila > 80:
                # Acercarse
                move_dist = min(self.speed * 0.8, dist_to_gorila - 80)
            elif dist_to_gorila < 60:
                # Alejarse un poco
                move_dist = -self.speed * 0.5
            else:
                # Movimiento lateral táctico
                self.direction += math.pi/2 * (0.5 if random.random() > 0.5 else -0.5)
                move_dist = self.speed * 0.6
            
            # Aplicar movimiento
            self.x += math.cos(self.direction) * move_dist * (1 - self.fear)
            self.y += math.sin(self.direction) * move_dist * (1 - self.fear)
            
            # Atacar si está en rango
            if 60 <= dist_to_gorila <= 90 and self.attack_cooldown <= 0:
                damage = self.attack_power * (1 - self.fear)
                gorila.health -= damage
                self.attack_cooldown = 25
                
                # Efecto de golpe
                for _ in range(5):
                    angle = random.uniform(0, 2*math.pi)
                    speed = random.uniform(1, 3)
                    particles.add_particle(
                        gorila.x, gorila.y, BLOOD_COLOR,
                        (math.cos(angle)*speed, math.sin(angle)*speed),
                        random.randint(20, 40)
                    )
        else:
            # Comportamiento defensivo/evasivo
            if self.fear > 0.3 or dist_to_gorila < 120:
                # Huir del gorila
                self.direction = math.atan2(self.y - gorila.y, self.x - gorila.x)
            else:
                # Buscar compañeros
                if hombres:
                    avg_x = sum(h.x for h in hombres) / len(hombres)
                    avg_y = sum(h.y for h in hombres) / len(hombres)
                    self.direction = math.atan2(avg_y - self.y, avg_x - self.x)
            
            # Aplicar movimiento con variación
            self.direction += random.uniform(-0.3, 0.3)
            move_dist = self.speed * (0.5 + self.fear * 0.7)
            self.x += math.cos(self.direction) * move_dist
            self.y += math.sin(self.direction) * move_dist
        
        # Actualizar trail (huellas)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        
        # Actualizar cooldowns y estados
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.fatigue = min(100, self.fatigue + 0.1)
        if self.fatigue > 80:
            self.speed = max(0.3, self.speed * 0.95)
        
        # Mantener dentro de límites con rebote
        if not (0 <= self.x <= SIZE):
            self.direction = math.pi - self.direction
        if not (0 <= self.y <= SIZE):
            self.direction = -self.direction
        
        self.x = max(5, min(SIZE-5, self.x))
        self.y = max(5, min(SIZE-5, self.y))
    
    def draw(self, surface):
        # Dibujar huellas
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i+1)/len(self.trail))
            color = (*TRAIL_COLOR, alpha//2)
            gfxdraw.filled_circle(surface, int(tx), int(ty), 3, color)
        
        # Dibujar cuerpo cuadrado
        rect_size = self.size * 2
        rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), rect_size, rect_size)
        pygame.draw.rect(surface, self.color, rect)

        
        # Barra de salud
        health_width = 20 * (self.health / self.max_health)
        pygame.draw.rect(surface, (0,0,0), (self.x-10, self.y-self.size-15, 20, 5))
        pygame.draw.rect(surface, (0,255,0), (self.x-10, self.y-self.size-15, health_width, 5))

# Clase para el gorila (más realista)
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
        self.rage = 0  # Nivel de furia
        self.trail = []
        self.target = None
    
    def update(self, hombres, particles):
        # Seleccionar objetivo basado en proximidad y salud
        if hombres:
            self.target = min(
                hombres,
                key=lambda h: math.hypot(h.x-self.x, h.y-self.y) - h.health*0.5
            )
            
            # Movimiento con inercia
            dx = self.target.x - self.x + random.uniform(-30, 30)
            dy = self.target.y - self.y + random.uniform(-30, 30)
            dist = max(1, math.hypot(dx, dy))
            
            # Aumentar velocidad cuando está furioso
            current_speed = self.speed * (1 + self.rage * 0.5)
            
            self.x += (dx / dist) * current_speed
            self.y += (dy / dist) * current_speed
            
            # Ataque en área
            if dist < 100 and self.attack_cooldown <= 0:
                self.atacar(hombres, particles)
                self.attack_cooldown = 40 - self.rage*10
                self.rage = min(1.0, self.rage + 0.1)
        
        # Actualizar cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Actualizar furia (disminuye con el tiempo)
        self.rage = max(0, self.rage - 0.005)
        
        # Actualizar trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)
        
        # Mantener dentro de límites
        self.x = max(self.size, min(SIZE-self.size, self.x))
        self.y = max(self.size, min(SIZE-self.size, self.y))
    
    def atacar(self, hombres, particles):
        # Ataque en área con daño variable por distancia
        for hombre in hombres[:]:
            dist = math.hypot(hombre.x-self.x, hombre.y-self.y)
            if dist < 110:  # Radio de ataque
                # Daño reducido por distancia
                damage = self.attack_power * (1.2 - dist/110) * (0.8 + self.rage*0.4)
                hombre.health -= damage
                
                # Efecto de golpe
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
                    # Explosión de sangre al morir
                    for _ in range(15):
                        angle = random.uniform(0, 2*math.pi)
                        speed = random.uniform(1, 6)
                        particles.add_particle(
                            hombre.x, hombre.y, BLOOD_COLOR,
                            (math.cos(angle)*speed, math.sin(angle)*speed),
                            random.randint(30, 60)
                        )
    
    def draw(self, surface):
        # Dibujar huellas
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(200 * (i+1)/len(self.trail))
            color = (*GORILA_COLOR, alpha//3)
            gfxdraw.filled_circle(surface, int(tx), int(ty), 8, color)
        
        # Dibujar cuerpo cuadrado
        rect_size = self.size * 2
        rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), rect_size, rect_size)
        pygame.draw.rect(surface, self.color, rect)

        
        # Ojos rojos cuando está furioso
        eye_color = (150 + 105*self.rage, 50, 50)
        left_eye = (int(self.x-10), int(self.y-5))
        right_eye = (int(self.x+10), int(self.y-5))
        gfxdraw.filled_circle(surface, *left_eye, 5 + int(3*self.rage), eye_color)
        gfxdraw.filled_circle(surface, *right_eye, 5 + int(3*self.rage), eye_color)
        
        # Barra de salud
        health_width = 40 * (self.health / self.max_health)
        pygame.draw.rect(surface, (0,0,0), (self.x-20, self.y-self.size-25, 40, 10))
        health_color = (
            int(255 * (1 - self.health/self.max_health)),
            int(255 * (self.health/self.max_health)),
            0
        )
        pygame.draw.rect(surface, health_color, (self.x-20, self.y-self.size-25, health_width, 10))

# Crear terreno con textura
def create_terrain_surface(size):
    terrain = pygame.Surface((size, size))
    terrain.fill(GROUND_COLOR)
    
    # Patrón de ruido simple
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

# Función principal
def main():
    terrain = create_terrain_surface(SIZE)
    particles = ParticleSystem()
    
    # Crear hombres en círculo alrededor del centro
    hombres = []
    center_x, center_y = SIZE // 2, SIZE // 2
    radius = SIZE // 3
    
    for i in range(100):
        angle = random.uniform(0, 2*math.pi)
        spread = random.uniform(0.7, 1.3)
        x = center_x + radius * math.cos(angle) * spread
        y = center_y + radius * math.sin(angle) * spread
        hombres.append(Hombre(x, y))
    
    # Crear gorila en el centro
    gorila = Gorila(center_x, center_y)
    
    # Texto
    font = pygame.font.SysFont('Arial', 24)
    big_font = pygame.font.SysFont('Arial', 36, bold=True)
    
    running = True
    outcome = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and outcome:
                    # Reiniciar
                    hombres = []
                    for i in range(100):
                        angle = random.uniform(0, 2*math.pi)
                        spread = random.uniform(0.7, 1.3)
                        x = center_x + radius * math.cos(angle) * spread
                        y = center_y + radius * math.sin(angle) * spread
                        hombres.append(Hombre(x, y))
                    gorila = Gorila(center_x, center_y)
                    particles = ParticleSystem()
                    outcome = None
        
        # Dibujar terreno
        screen.blit(terrain, (0, 0))
        
        # Actualizar y dibujar
        if outcome is None:
            gorila.update(hombres, particles)
            for hombre in hombres[:]:
                hombre.update(gorila, hombres, particles)
            
            # Verificar condiciones de fin
            if gorila.health <= 0:
                outcome = "¡Los hombres han derrotado al gorila!"
            elif len(hombres) <= 10:
                outcome = f"¡El gorila ha ganado! Sobrevivieron {len(hombres)} hombres"
        
        particles.update()
        particles.draw(screen)
        
        for hombre in hombres:
            hombre.draw(screen)
        gorila.draw(screen)
        
        # Estadísticas
        stats_text = f"Hombres: {len(hombres)}  Salud Gorila: {max(0, int(gorila.health))}"
        text_surface = font.render(stats_text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))
        
        # Mostrar resultado
        if outcome:
            result_surface = big_font.render(outcome, True, (255, 255, 0))
            text_rect = result_surface.get_rect(center=(SIZE//2, SIZE//2))
            screen.blit(result_surface, text_rect)
            
            restart_text = font.render("Presiona R para reiniciar", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(SIZE//2, SIZE//2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()