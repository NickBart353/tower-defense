import pygame

from enemy import *

class WAVE:
    def __init__(self, wave_number, enemy_list, money_reward):
        self.wave_number = wave_number
        self.enemy_list = enemy_list
        self.money_reward = money_reward
        self.spawn_increment = 200
        self.last_time_spawned = 0
        self.pause_between_attacks = 15000

    def spawn_enemy(self, start_dict):
        now = pygame.time.get_ticks()
        if now > self.last_time_spawned + self.spawn_increment and len(self.enemy_list) > 0:
            self.last_time_spawned = now
            enemy = self.enemy_list[0]
            enemy.x = start_dict["x"]
            enemy.y = start_dict["y"]
            self.enemy_list.pop(0)
            return enemy
        else:
            return None

def init_waves():
    waves = [WAVE(0,get_enemy_list(0),2000),
             WAVE(1,get_enemy_list(0),2000),
             WAVE(2,get_enemy_list(0),2000),
             WAVE(3, get_enemy_list(0), 2000),
             WAVE(4, get_enemy_list(0), 2000),
             WAVE(5, get_enemy_list(0), 2000),
             WAVE(6, get_enemy_list(0), 2000),
             WAVE(7, get_enemy_list(0), 2000),
             WAVE(8, get_enemy_list(0), 2000),

             ]

    return waves