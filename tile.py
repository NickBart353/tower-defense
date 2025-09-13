import pygame

class TILE:
    def __init__(self, x, y, field_type, can_collide_with, tower = None, rect =  None,):
        self.x = x
        self.y = y
        self.field_type = field_type
        self.can_collide_with = can_collide_with
        self.tower = tower
        if rect is None:
            self.rect = pygame.Rect(0,0,0,0)
        self.on_tile = 1

    def __str__(self):
        return "{}".format(self.field_type)