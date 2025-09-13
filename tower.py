import math
import pygame

from upgrade import *
from bullet import *

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
        self.fire_rate = 400  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second
        self.pierce = 2
        self.value = self.cost // 2

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
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
                    self.fire_rate -= 150
                case 1:
                    self.upgrade_one_counter += 1
                    self.damage += 2
                case 2:
                    self.upgrade_one_maxed = True

    def upgrade_two(self):
        if not self.upgrade_two_maxed:
            match self.upgrade_two_counter:
                case 0:
                    self.upgrade_two_counter += 1
                    self.pierce = 2
                    self.value += self.upgrade_data[self.tower_type]["2"]["0"]["cost"] // 2
                case 1:
                    self.upgrade_two_counter += 1
                    self.pierce = 4
                    self.value += self.upgrade_data[self.tower_type]["2"]["1"]["cost"] // 2
                case 2:
                    self.upgrade_two_maxed = True
                    self.pierce = 999999
                    self.value += self.upgrade_data[self.tower_type]["2"]["2"]["cost"] // 2

    def upgrade_three(self):
        if not self.upgrade_three_maxed:
            self.update_value("3", self.upgrade_three_counter)
            match self.upgrade_three_counter:
                case 0:
                    self.upgrade_three_counter += 1
                    self.damage += 5
                case 1:
                    self.upgrade_three_counter += 1
                    self.damage += 5
                case 2:
                    self.upgrade_three_maxed = True
                    self.pierce = 999999
                    self.bullet_size *= 5

class CircleTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 250  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 500  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
            self.last_fired = now
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

class ArcTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 500  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 500  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
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
            if self.upgrade_three_maxed:
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

def get_tower_cost(tower_type):
    val = 0
    match tower_type:
        case "basic":
            val = 300
        case "circle":
            val = 500
        case "arc":
            val = 200
    return val