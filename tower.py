class TOWER:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type

        match self.tower_type:
            case "basic":
                self.radius = 500 #500 pixels
                self.damage = 1 #1 damage
                self.fire_rate = 5 #5 per second