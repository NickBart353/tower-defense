import pygame
class ENEMY:
    def __init__(self, x, y, health, damage, i_came_from = None):
        self.x = x
        self.y = y
        self.health = health
        self.current_health = health
        self.i_came_from = i_came_from
        self.enemy_rect = pygame.Rect(0,0,0,0)
        self.damage = damage

def get_move_interval():
    return 200
