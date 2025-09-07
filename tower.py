import math
from unittest import case

import pygame

from bullet import *

class TOWER:
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.bullet_list = []
        self.last_fired = -1
        self.circle_counter = 0
        self.color = color
        self.rect = pygame.Rect(0,0,0,0)
        self.upgrade_one_counter = 0
        self.upgrade_two_counter = 0
        self.upgrade_three_counter = 0
        self.cost = get_tower_cost(self.tower_type)

    def fire(self, enemy):
        pass

    def draw(self, screen, radius):
        return pygame.draw.circle(screen,self.color, (self.x, self.y),radius)

    def display_upgrades(self):
        pass

    def upgrade_one(self):
        pass
    def upgrade_two(self):
        pass
    def upgrade_three(self):
        pass

class BasicTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 500  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 300  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
            self.last_fired = now
            if self.upgrade_one_counter > 0:
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x + 0.35, enemy.y - self.y + 0.35, self.bullet_speed,
                           self.radius, self.damage))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x - 0.35, enemy.y - self.y - 0.35, self.bullet_speed,
                           self.radius, self.damage))
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                           self.radius, self.damage))
            else:
                self.bullet_list.append(
                    BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                           self.radius, self.damage))

    def upgrade_one(self):
        match self.upgrade_one_counter:
            case 0:
                self.upgrade_one_counter += 1
            case 1:
                self.upgrade_one_counter += 1
                self.damage += 2
            case 2:
                self.upgrade_one_counter += 1
                self.fire_rate -= 150

    def upgrade_two(self):
        pass
    def upgrade_three(self):
        pass

class CircleTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 500  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 200  # 5 shots per second
        self.bullet_speed = 20  # 50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()
        if now > self.fire_rate + self.last_fired:
            self.last_fired = now
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, 0, -1, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, 0, 1, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, 1, 0, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, -1, 0, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, 0.5, 0.5, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, 0.5, -0.5, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, -0.5, 0.5, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, -0.5, -0.5, self.bullet_speed, self.radius, self.damage))

class ArcTower(TOWER):
    def __init__(self, x, y, tower_type, COL_SIZE, ROW_SIZE, color):
        super().__init__(x, y, tower_type, COL_SIZE, ROW_SIZE, color)
        self.radius = 50000  # 500 pixels
        self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                              self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
        self.damage = 1  # 1 damage
        self.fire_rate = 100  # 5 shots per second
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
                BULLET(self.x + 0.5, self.y + 0.5, dx_pos, dy_pos, self.bullet_speed, self.radius, self.damage))
            self.bullet_list.append(
                BULLET(self.x + 0.5, self.y + 0.5, dx_neg, dy_neg, self.bullet_speed, self.radius, self.damage))
            # self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_half, dy_half, self.bullet_speed, self.radius, self.damage))
            # self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_calf, dy_calf, self.bullet_speed, self.radius, self.damage))


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