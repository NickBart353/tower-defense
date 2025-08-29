class ENEMY:
    def __init__(self, x, y, health, i_came_from = None):
        self.x = x
        self.y = y
        self.health = health
        self.i_came_from = i_came_from
def get_move_interval():
    return 200
