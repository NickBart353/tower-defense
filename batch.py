from enemy import ENEMY

class BATCH:
    def __init__(self, enemy_type, amount, threshold):
        self.enemies = []
        for i in range(amount):
            self.enemies.append(ENEMY(enemy_type))
        self.spawn_threshold = threshold