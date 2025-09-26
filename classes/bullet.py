import pygame

class BULLET:
    def __init__(self,my_x,my_y,x_vec,y_vec, velocity, distance, damage, size, pierce):
        self.my_x = my_x
        self.my_y = my_y
        self.x_vec = x_vec
        self.y_vec = y_vec
        self.velocity = velocity
        self.distance = distance
        self.damage = damage
        self.size = size
        self.pierce = pierce
        self.bullet_rect = pygame.Rect(0,0,0,0)

class ICEBULLET(BULLET):
    def __init__(self, my_x, my_y, x_vec, y_vec, velocity, distance, damage, size, pierce, slow_intensity=0.3, slow_duration=2.0):
        super().__init__(my_x, my_y, x_vec, y_vec, velocity, distance, damage, size, pierce)
        self.slow_intensity = slow_intensity  # How much to slow the enemy (0.0 to 1.0)
        self.slow_duration = slow_duration    # How long the slow effect lasts in seconds
        self.is_ice_bullet = True             # Flag to identify this as an ice bullet
        
    def apply_effect_to_enemy(self, enemy):
        """Apply slow effect to the hit enemy."""
        enemy.apply_slow_effect(self.slow_intensity, self.slow_duration)

class FIREBULLET(BULLET):
    def __init__(self, my_x, my_y, x_vec, y_vec, velocity, distance, damage, size, pierce, burn_damage=1.0, burn_duration=3.0, can_stack=True):
        super().__init__(my_x, my_y, x_vec, y_vec, velocity, distance, damage, size, pierce)
        self.burn_damage = burn_damage        # DOT damage per second
        self.burn_duration = burn_duration    # How long the burn effect lasts in seconds
        self.can_stack = can_stack           # Whether burn effects can stack
        self.is_fire_bullet = True           # Flag to identify this as a fire bullet
        self.spread_chance = 0.0             # Chance to spread fire to nearby enemies (0.0 to 1.0)
        self.spread_radius = 0               # Radius for fire spread effect
        
    def apply_effect_to_enemy(self, enemy):
        """Apply burn effect to the hit enemy."""
        enemy.apply_burn_effect(self.burn_damage, self.burn_duration, self.can_stack)