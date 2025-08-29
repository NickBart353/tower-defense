import pygame

class BULLET:
    def __init__(self,my_x,my_y,x_vec,y_vec, velocity, distance, damage):
        self.my_x = my_x
        self.my_y = my_y
        self.x_vec = x_vec
        self.y_vec = y_vec
        self.velocity = velocity
        self.distance = distance
        self.damage = damage
        self.bullet_rect = pygame.Rect(0,0,0,0)