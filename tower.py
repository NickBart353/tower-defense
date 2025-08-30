import math

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

        match self.tower_type:
            case "basic":
                self.radius = 500  # 500 pixels
                self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                                      self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
                self.damage = 1  # 1 damage
                self.fire_rate = 300  # 5 shots per second
                self.bullet_speed = 20  # 50 pixels per second
            case "circle":
                self.radius = 500  # 500 pixels
                self.radius_rect_circle = pygame.Rect((self.x * COL_SIZE) - self.radius / 2,
                                                      self.y * ROW_SIZE - self.radius / 2, self.radius, self.radius)
                self.damage = 1  # 1 damage
                self.fire_rate = 200  # 5 shots per second
                self.bullet_speed = 20  # 50 pixels per second
            case "arc":
                self.radius = 50000 #500 pixels
                self.radius_rect_circle = pygame.Rect((self.x*COL_SIZE)-self.radius/2, self.y*ROW_SIZE-self.radius/2, self.radius, self.radius)
                self.damage = 1 #1 damage
                self.fire_rate = 100 #5 shots per second
                self.bullet_speed = 20 #50 pixels per second

    def fire(self, enemy):
        now = pygame.time.get_ticks()

        match self.tower_type:
            case "basic":
                if now > self.fire_rate + self.last_fired:
                    self.last_fired = now
                    self.bullet_list.append(
                        BULLET(self.x + 0.5, self.y + 0.5, enemy.x - self.x, enemy.y - self.y, self.bullet_speed,
                               self.radius, self.damage))

            case "circle":
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

            case "arc":
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
                    self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_pos, dy_pos, self.bullet_speed, self.radius, self.damage))
                    self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_neg, dy_neg, self.bullet_speed, self.radius, self.damage))
                    #self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_half, dy_half, self.bullet_speed, self.radius, self.damage))
                    #self.bullet_list.append(BULLET(self.x + 0.5, self.y + 0.5, dx_calf, dy_calf, self.bullet_speed, self.radius, self.damage))