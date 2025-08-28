class TILE:
    def __init__(self, x, y, field_type, can_collide_with, i_came_from = None):
        self.x = x
        self.y = y
        self.field_type = field_type
        self.can_collide_with = can_collide_with
        self.i_came_from = i_came_from
