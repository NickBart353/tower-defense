import math
import pygame

from classes.upgrade import get_upgrade_data
from classes.bullet import BULLET, ICEBULLET, FIREBULLET

class TOWER:
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color, rect = None):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.bullet_list = []
        self.last_fired = -1
        self.circle_counter = 0
        self.color = color
        if rect is None:
            self.rect = pygame.Rect(0,0,0,0)
        else:
            self.rect = rect
        self.upgrade_one_counter = 0
        self.upgrade_two_counter = 0
        self.upgrade_three_counter = 0
        self.bullet_size = COL_SIZE // 6
        self.pierce = 1
        self.upgrade_one_maxed = False
        self.upgrade_two_maxed = False
        self.upgrade_three_maxed = False
        self.can_upgrade_one = True
        self.can_upgrade_two = True
        self.can_upgrade_three = True
        self.cost = get_tower_cost(self.tower_type)
        self.upgrade_data = get_upgrade_data()
        self.value = self.cost // 2

    def fire(self, enemy):
        pass

    def draw(self, screen, radius):
        return pygame.draw.circle(screen,self.color, (self.x, self.y),radius)

    def display_upgrades(self):
        pass

    def update_value(self, upgrade_type, counter):
        self.value += self.upgrade_data[self.tower_type][upgrade_type][str(counter)]["cost"] // 2

    def upgrade_one(self):
        pass
    def upgrade_two(self):
        pass
    def upgrade_three(self):
        pass

class BasicTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 250  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 1000  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second
        self.pierce = 3
        self.value = self.cost // 2

    def fire(self, enemy, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        # Adjust fire rate based on speed multiplier
        adjusted_fire_rate = self.fire_rate / speed_multiplier
        if now > adjusted_fire_rate + self.last_fired:
            self.last_fired = now
            if self.upgrade_one_maxed:
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x + 0.35, enemy.y - self.y + 0.35, self.bullet_speed,
                           self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x - 0.35, enemy.y - self.y - 0.35, self.bullet_speed,
                           self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                           self.radius, self.damage, self.bullet_size, self.pierce))
            else:
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                           self.radius, self.damage, self.bullet_size, self.pierce))

    def upgrade_one(self):
        if not self.upgrade_one_maxed:
            self.update_value("1", self.upgrade_one_counter)
            match self.upgrade_one_counter:
                case 0:
                    self.upgrade_one_counter += 1
                    self.damage += 1
                    self.radius += 100
                case 1:
                    self.upgrade_one_counter += 1
                    self.damage += 1
                    self.radius += 100
                case 2:
                    self.upgrade_one_maxed = True
                    self.pierce += 2
                    self.damage += 1

    def upgrade_two(self):
        if not self.upgrade_two_maxed:
            self.update_value("2", self.upgrade_two_counter)
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.damage += 1
                    self.fire_rate -= 500
                case 1:
                    self.upgrade_two_counter += 1
                    self.damage += 1
                    self.fire_rate -= 250
                case 2:
                    self.upgrade_two_maxed = True
                    self.damage += 1
                    self.fire_rate = 20

    def upgrade_three(self):
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.damage += 2
                case 1:
                    self.upgrade_three_counter += 1
                    self.damage += 5
                case 2:
                    self.upgrade_three_maxed = True
                    self.pierce = 999999
                    self.bullet_size *= 5
                    self.fire_rate += 250
                    self.damage += 20

class CircleTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 100
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 1000  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second
        self.COL_SIZE = COL_SIZE
        self.ROW_SIZE = ROW_SIZE
        self.bullet_speed = 20
        self.pierce = 2
        self.radius = 100

    def fire(self, enemy, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        # Adjust fire rate based on speed multiplier
        adjusted_fire_rate = self.fire_rate / speed_multiplier
        if now > adjusted_fire_rate + self.last_fired:
            self.last_fired = now
            if not self.upgrade_two_maxed:
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, 0, -1, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, 0, 1, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, 1, 0, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, -1, 0, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, 0.5, 0.5, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, 0.5, -0.5, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, -0.5, 0.5, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, -0.5, -0.5, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
                if self.upgrade_three_maxed:
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, 0.25, 0.75, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, 0.25, -0.75, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, -0.25, 0.75, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, -0.25, -0.75, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, 0.75, 0.25, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, 0.75, -0.25, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, -0.75, 0.25, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, -0.75, -0.25, self.bullet_speed, self.radius, self.damage,
                               self.bullet_size, self.pierce))
            else:
                num_bullets = 20
                angle_step = 2 * math.pi / num_bullets

                angle1 = self.circle_counter * angle_step
                angle2 = 0
                if self.circle_counter + 5 < 20:
                    angle2 = (self.circle_counter + 5) * angle_step
                else:
                    angle2 = (-5 + self.circle_counter) * angle_step
                self.circle_counter += 1
                if self.circle_counter >= num_bullets:
                    self.circle_counter = 0

                dx_pos = math.cos(angle1)
                dy_pos = math.sin(angle1)
                dx_neg = math.cos(angle1) * -1
                dy_neg = math.sin(angle1) * -1
                dx_half = math.cos(angle2)
                dy_half = math.sin(angle2)
                dx_calf = math.cos(angle2) * -1
                dy_calf = math.sin(angle2) * -1
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, dx_pos, dy_pos, self.bullet_speed, self.radius, self.damage,
                           self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, dx_neg, dy_neg, self.bullet_speed, self.radius, self.damage,
                           self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, dx_half, dy_half, self.bullet_speed, self.radius, self.damage,
                           self.bullet_size, self.pierce))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, dx_calf, dy_calf, self.bullet_speed, self.radius, self.damage,
                           self.bullet_size, self.pierce))

    def upgrade_one(self):
        if not self.upgrade_one_maxed:
            self.update_value("1", self.upgrade_one_counter)
            match self.upgrade_one_counter:
                case 0:
                    self.upgrade_one_counter += 1
                    self.fire_rate /= 1.5
                case 1:
                    self.upgrade_one_counter += 1
                    self.fire_rate /= 1.5
                case 2:
                    self.fire_rate = 50
                    self.damage += 5
                    self.pierce += 1
                    self.upgrade_one_maxed = True

    def upgrade_two(self):
        if not self.upgrade_two_maxed:
            self.update_value("2", self.upgrade_two_counter)
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.pierce += 2
                case 1:
                    self.upgrade_two_counter += 1
                    self.pierce += 2
                case 2:
                    self.upgrade_two_maxed = True
                    self.bullet_speed = 10
                    self.fire_rate -= 100
                    self.radius += 150
                    self.pierce = 999999

    def upgrade_three(self):
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.damage += 2
                case 1:
                    self.upgrade_three_counter += 1
                    self.damage += 7
                case 2:
                    self.pierce = 3
                    self.upgrade_three_maxed = True

class ArcTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 500  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 500  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second

    def fire(self, enemy, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        # Adjust fire rate based on speed multiplier
        adjusted_fire_rate = self.fire_rate / speed_multiplier
        if now > adjusted_fire_rate + self.last_fired:
            self.last_fired = now
            num_bullets = 20
            angle_step = 2 * math.pi / num_bullets

            angle1 = self.circle_counter * angle_step
            angle2 = 0
            if self.circle_counter + 5 < 20:
                angle2 = (self.circle_counter + 5) * angle_step
            else:
                angle2 = (-5 + self.circle_counter) * angle_step
            self.circle_counter += 1
            if self.circle_counter >= num_bullets:
                self.circle_counter = 0

            dx_pos = math.cos(angle1)
            dy_pos = math.sin(angle1)
            dx_neg = math.cos(angle1) * -1
            dy_neg = math.sin(angle1) * -1
            dx_half = math.cos(angle2)
            dy_half = math.sin(angle2)
            dx_calf = math.cos(angle2) * -1
            dy_calf = math.sin(angle2) * -1
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, dx_pos, dy_pos, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, dx_neg, dy_neg, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
            self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_half, dy_half, self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce))
            self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_calf, dy_calf, self.bullet_speed, self.radius, self.damage,self.bullet_size, self.pierce))

    def upgrade_one(self):
        if not self.upgrade_one_maxed:
            self.update_value("1", self.upgrade_one_counter)
            match self.upgrade_one_counter:
                case 0:
                    self.upgrade_one_counter += 1
                    self.fire_rate -= 250
                case 1:
                    self.upgrade_one_counter += 1
                    self.fire_rate -= 150
                case 2:
                    self.fire_rate -= 50
                    self.upgrade_one_maxed = True

    def upgrade_two(self):
        if not self.upgrade_two_maxed:
            self.update_value("2", self.upgrade_two_counter)
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.pierce = 2
                case 1:
                    self.upgrade_two_counter += 1
                    self.pierce = 4
                case 2:
                    self.upgrade_two_maxed = True
                    self.pierce = 999999

    def upgrade_three(self):
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.damage += 2
                case 1:
                    self.upgrade_three_counter += 1
                    self.damage += 5
                case 2:
                    self.upgrade_three_maxed = True

class IceTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 115  # Short range (increased by 15%)
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 0.5  # Very low damage - focus on crowd control
        self.fire_rate = 800  # Moderate fire rate
        self.bullet_speed = 15  # Slower bullets that look more icy
        self.pierce = 1
        self.slow_intensity = 0.3  # 30% speed reduction
        self.slow_duration = 2.0   # 2 seconds slow duration
        self.area_effect = False   # Will become true after upgrade
        self.area_radius = 0       # Area effect radius

    def fire(self, enemy, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        # Adjust fire rate based on speed multiplier
        adjusted_fire_rate = self.fire_rate / speed_multiplier
        if now > adjusted_fire_rate + self.last_fired:
            self.last_fired = now
            
            if self.area_effect:
                # Area effect ice tower shoots multiple projectiles in a spread
                num_bullets = 5
                angle_offset = 0.3  # Spread angle
                base_angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
                
                for i in range(num_bullets):
                    angle = base_angle + (i - 2) * angle_offset
                    x_vec = math.cos(angle)
                    y_vec = math.sin(angle)
                    self.bullet_list.append(
                        ICEBULLET(self.x + 0.5, self.y + 0.5, x_vec, y_vec, self.bullet_speed,
                                 self.radius, self.damage, self.bullet_size, self.pierce,
                                 self.slow_intensity, self.slow_duration))
            else:
                # Single target ice bullet
                self.bullet_list.append(
                    ICEBULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                             self.radius, self.damage, self.bullet_size, self.pierce,
                             self.slow_intensity, self.slow_duration))

    def upgrade_one(self):  # Slow Enhancement Path
        if not self.upgrade_one_maxed:
            self.update_value("1", self.upgrade_one_counter)
            match self.upgrade_one_counter:
                case 0:
                    self.upgrade_one_counter += 1
                    self.slow_intensity += 0.2  # 30% -> 50% slow
                    self.slow_duration += 1.0   # 2s -> 3s duration
                case 1:
                    self.upgrade_one_counter += 1
                    self.slow_intensity += 0.2  # 50% -> 70% slow  
                    self.slow_duration += 1.0   # 3s -> 4s duration
                case 2:
                    self.upgrade_one_maxed = True
                    self.slow_intensity = 0.85  # 85% slow (near freeze)
                    self.slow_duration += 2.0   # 4s -> 6s duration

    def upgrade_two(self):  # Area Effect Path
        if not self.upgrade_two_maxed:
            self.update_value("2", self.upgrade_two_counter)
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.area_effect = True
                    self.area_radius = 80
                case 1:
                    self.upgrade_two_counter += 1
                    self.area_radius = 120
                    self.pierce += 1
                case 2:
                    self.upgrade_two_maxed = True
                    self.area_radius = 180
                    self.pierce += 2
                    self.fire_rate -= 200  # Faster firing

    def upgrade_three(self):  # Damage & Range Path
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.damage += 1  # Reduced from 2 to 1
                    self.radius += 100
                case 1:
                    self.upgrade_three_counter += 1
                    self.damage += 1.5  # Reduced from 3 to 1.5
                    self.radius += 150
                    self.fire_rate -= 100
                case 2:
                    self.upgrade_three_maxed = True
                    self.damage += 5  # Reduced from 10 to 5
                    self.pierce = 999999
                    self.bullet_size *= 2
                    self.slow_duration += 3.0  # Bonus slow duration

class FireTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 173  # Short range (increased by 15%)
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 0  # No upfront damage - purely DOT-based
        self.fire_rate = 600  # Moderate fire rate
        self.bullet_speed = 18  # Slightly slower bullets for fire effect
        self.pierce = 1
        self.burn_damage = 0.7  # DOT damage per second (very low for visible burn effect)
        self.burn_duration = 3.0  # Burn duration in seconds
        self.can_stack_burns = True  # Allow burn stacking
        self.spread_fire = False  # Fire spread effect
        self.spread_radius = 0  # Radius for fire spread
        self.multi_shot = False  # Multiple projectile shooting

    def fire(self, enemy, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        # Adjust fire rate based on speed multiplier
        adjusted_fire_rate = self.fire_rate / speed_multiplier
        if now > adjusted_fire_rate + self.last_fired:
            self.last_fired = now
            
            if self.multi_shot:
                # Fire multiple projectiles (upgrade 3 effect)
                num_bullets = 3
                angle_offset = 0.2  # Spread angle
                base_angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
                
                for i in range(num_bullets):
                    angle = base_angle + (i - 1) * angle_offset
                    x_vec = math.cos(angle)
                    y_vec = math.sin(angle)
                    
                    fire_bullet = FIREBULLET(self.x + 0.5, self.y + 0.5, x_vec, y_vec, self.bullet_speed,
                                           self.radius, self.damage, self.bullet_size, self.pierce,
                                           self.burn_damage, self.burn_duration, self.can_stack_burns)
                    
                    # Add spread properties if available
                    if self.spread_fire:
                        fire_bullet.spread_chance = 0.3
                        fire_bullet.spread_radius = self.spread_radius
                    
                    self.bullet_list.append(fire_bullet)
            else:
                # Single fire bullet
                fire_bullet = FIREBULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, 
                                       self.bullet_speed, self.radius, self.damage, self.bullet_size, self.pierce,
                                       self.burn_damage, self.burn_duration, self.can_stack_burns)
                
                # Add spread properties if available
                if self.spread_fire:
                    fire_bullet.spread_chance = 0.3
                    fire_bullet.spread_radius = self.spread_radius
                
                self.bullet_list.append(fire_bullet)

    def upgrade_one(self):  # Burn Intensity Path
        if not self.upgrade_one_maxed:
            self.update_value("1", self.upgrade_one_counter)
            match self.upgrade_one_counter:
                case 0:
                    self.upgrade_one_counter += 1
                    self.burn_damage += 0.3  # 0.7 -> 1.0 DOT damage
                    self.burn_duration += 1.0  # 3s -> 4s duration
                case 1:
                    self.upgrade_one_counter += 1
                    self.burn_damage += 0.4  # 1.0 -> 1.4 DOT damage
                    self.burn_duration += 1.0  # 4s -> 5s duration
                    self.spread_fire = True
                    self.spread_radius = 50
                case 2:
                    self.upgrade_one_maxed = True
                    self.burn_damage += 0.6  # 1.4 -> 2.0 DOT damage
                    self.burn_duration += 2.0  # 5s -> 7s duration
                    self.spread_radius = 100  # Larger spread

    def upgrade_two(self):  # Area Effect Path
        if not self.upgrade_two_maxed:
            self.update_value("2", self.upgrade_two_counter)
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.burn_damage += 0.2  # Increase DOT instead of direct damage (0.7 -> 0.9)
                    self.spread_fire = True
                    self.spread_radius = 60
                case 1:
                    self.upgrade_two_counter += 1
                    self.burn_damage += 0.3  # More DOT damage (0.9 -> 1.2)
                    self.spread_radius = 90
                    self.pierce += 1  # Can hit 2 enemies
                case 2:
                    self.upgrade_two_maxed = True
                    self.burn_damage += 0.4  # Total +0.9 DOT damage (1.2 -> 1.6)
                    self.spread_radius = 150
                    self.pierce += 2  # Can hit 4 enemies total
                    self.bullet_size *= 1.5  # Larger projectiles

    def upgrade_three(self):  # Rapid Ignition Path
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.fire_rate -= 150  # Faster fire rate
                    self.burn_damage += 0.1  # Slightly more DOT (0.7 -> 0.8)
                case 1:
                    self.upgrade_three_counter += 1
                    self.fire_rate -= 100  # Even faster
                    self.multi_shot = True  # Start firing multiple bullets
                    self.burn_damage += 0.2  # (0.8 -> 1.0)
                case 2:
                    self.upgrade_three_maxed = True
                    self.fire_rate = 150  # Very fast firing
                    self.pierce = 999999  # Piercing projectiles
                    self.burn_damage += 0.3  # Total +0.6 DOT damage (1.0 -> 1.3)
                    self.bullet_speed += 7  # Faster projectiles

def get_tower_cost(tower_type):
    val = 0
    match tower_type:
        case "basic":
            val = 300
        case "circle":
            val = 500
        case "arc":
            val = 200
        case "ice":
            val = 400
        case "fire":
            val = 350
    return val