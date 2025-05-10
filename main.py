import pygame
import sys
from hombre import Hombre
from gorila import Gorila
from particle_system import ParticleSystem
from terrain import create_terrain_surface
from config import *
import random
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Simulación Realista: 100 Hombres vs Gorila")
    clock = pygame.time.Clock()
    
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
        stats_text = f"Mens: {len(hombres)}  Gorila health: {max(0, int(gorila.health))}"
        text_surface = font.render(stats_text, True, (BLACK))
        screen.blit(text_surface, (20, 20))
        
        # Mostrar resultado
        if outcome:
            result_surface = big_font.render(outcome, True, (BLACK))
            text_rect = result_surface.get_rect(center=(SIZE//2, SIZE//2))
            screen.blit(result_surface, text_rect)
            
            restart_text = font.render("Press R to reload", True, (BLACK))
            restart_rect = restart_text.get_rect(center=(SIZE//2, SIZE//2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()