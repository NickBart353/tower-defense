import pygame

from bullet import *

class TOWER:
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.bullet_list = []
        self.last_fired = -1

        match self.tower_type:
            case "basic":
                self.radius = 500 #500 pixels
                self.radius_rect_circle = pygame.Rect((self.x*COL_SIZE)-self.radius/2, self.y*ROW_SIZE-self.radius/2, self.radius, self.radius)
                self.damage = 1 #1 damage
                self.fire_rate = 100 #5 shots per second
                self.bullet_speed = 50 #50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
            self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed, self.radius, self.damage))
            self.last_fired = now