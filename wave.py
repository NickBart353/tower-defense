import pygame

from enemy import *

class WAVE:
    def __init__(self, wave_number, money_reward):
        self.wave_number = wave_number
        self.enemy_list = generate_list_from_data(self.wave_number)
        self.money_reward = money_reward

        ########## WEE WOO --- ALARM --- MUSS NOCH GEMACHT WERDEN
        #self.monster_batch_order = monster_batch_order

        self.spawn_increment = 200
        self.last_time_spawned = 0
        self.batch_counter = 0
        self.pause_between_attacks = 15000

    def spawn_enemy(self, start_dict):
        now = pygame.time.get_ticks()
        if now > self.last_time_spawned + self.spawn_increment:
            if len(self.enemy_list) > 0:
                if len(self.enemy_list[0]) > 0:
                    self.last_time_spawned = now
                    enemy = self.enemy_list[0][0]
                    enemy.x = start_dict["x"]
                    enemy.y = start_dict["y"]
                    self.enemy_list[0].pop(0)
                    return enemy
                else:
                    self.enemy_list.pop(0)
                    return None
        return None

def init_waves():
    wave_list = [
        WAVE(0,500),
        WAVE(1,500),
        WAVE(2,800),
        WAVE(3, 800),
        WAVE(4, 1000),
        WAVE(5, 1000),
        WAVE(6, 1000),
        WAVE(7, 1000),
        WAVE(8, 1000),
        WAVE(9, 1000),
        WAVE(10, 1000),
        WAVE(11, 1000),
        WAVE(12, 1000),
        WAVE(13, 1000),
        WAVE(14, 1000),
        WAVE(15, 1000),
        WAVE(16, 1000),
        WAVE(17, 1000),
        WAVE(18, 1000),
        WAVE(19, 1000),
        WAVE(20, 1000),
        WAVE(21, 1000),
    ]

    return wave_list