import pygame
class ENEMY:
    def __init__(self, health, damage, i_came_from = None, x = 0, y = 0):
        self.x = x
        self.y = y
        self.health = health
        self.current_health = health
        self.i_came_from = i_came_from
        self.enemy_rect = pygame.Rect(0,0,0,0)
        self.damage = damage
        self.movement_interval = 200
        self.last_time_moved = 0

def get_enemy_list(wave_number):
    enemies = []
    match wave_number:
        case 0:
            for i in range(10):
                enemies.append(ENEMY(5, 5))
        case 1:
            for i in range(10):
                enemies.append(ENEMY(10, 5))
        case 2:
            for i in range(20):
                enemies.append(ENEMY(10, 5))
    return enemies