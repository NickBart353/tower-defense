import pygame

from random import randint
from enemy import *
from batch import BATCH

class WAVE:
    wave_number_counter = 0
    def __init__(self, money_reward):
        self.wave_number = WAVE.wave_number_counter

        #self.enemy_list = generate_list_from_data(self.wave_number)
        self.enemy_list = generate_list_from_wave_num(self.wave_number)

        WAVE.wave_number_counter += 1
        self.money_reward = money_reward

        self.spawn_increment = 500
        self.last_time_spawned = 0
        self.batch_counter = 0
        self.pause_between_attacks = 15000

    def spawn_enemy(self, start_dict):
        now = pygame.time.get_ticks()
        if len(self.enemy_list) > 0:
            if now > self.last_time_spawned + self.enemy_list[0].spawn_threshold:
                if len(self.enemy_list[0].enemies) > 0:
                    self.last_time_spawned = now
                    enemy = self.enemy_list[0].enemies[0]
                    enemy.x = start_dict["x"]
                    enemy.y = start_dict["y"]
                    self.enemy_list[0].enemies.pop(0)
                    return enemy
                else:
                    self.enemy_list.pop(0)
                    return None
        return None

def generate_list_from_wave_num(wave_number):
    batch_list = []
    match wave_number:
        case 0:
            batch_list.append(BATCH(1,20,500))
        case 1:
            batch_list.append(BATCH(1, 10, 500))
            batch_list.append(BATCH(2, 20, 500))
        case 2:
            batch_list.append(BATCH(1, 10, 500))
            batch_list.append(BATCH(2, 20, 500))
        case 3:
            batch_list.append(BATCH(1, 10, 400))
            batch_list.append(BATCH(3, 10, 500))
            batch_list.append(BATCH(2, 20, 200))
        case 4:
            batch_list.append(BATCH(4, 20, 400))
            batch_list.append(BATCH(3, 15, 300))
        case 5:
            batch_list.append(BATCH(4, 10, 400))
            batch_list.append(BATCH(5, 15, 400))
            batch_list.append(BATCH(3, 20, 100))
        case 6:
            batch_list.append(BATCH(6, 10, 300))
            batch_list.append(BATCH(5, 10, 400))
            batch_list.append(BATCH(6, 5, 400))
        case 7:
            batch_list.append(BATCH(6, 15, 200))
            batch_list.append(BATCH(6, 20, 400))
        case 8:
            batch_list.append(BATCH(2, 25, 50))
            batch_list.append(BATCH(5, 30, 400))
            batch_list.append(BATCH(7, 10, 400))
        case 9:
            batch_list.append(BATCH(8, 15, 300))
            batch_list.append(BATCH(7, 30, 400))
            batch_list.append(BATCH(9, 5, 400))
        case _:
            total_monsters = 20 * wave_number
            if wave_number < 20:
                total_monsters -= 50
            total_batches = total_monsters // (randint(5,30))

            top_end_enemy = 1
            bottom_end_enemy = 1
            if wave_number < 20:
                top_end_enemy = 10
                bottom_end_enemy = 3
            if 20 < wave_number < 30:
                top_end_enemy = 12
                bottom_end_enemy = 5
            if 30 < wave_number:
                top_end_enemy = 13
                bottom_end_enemy = 6

            has_enemy_twelve = False
            has_enemy_thirteen = False

            for batch in range(total_batches):
                threshold = randint(100,400)

                enemy_type = randint(bottom_end_enemy, top_end_enemy)

                while ((enemy_type >= 12 and wave_number < 40 and (batch + 1) == total_batches and 3 < total_monsters)
                       or (enemy_type == 12 and has_enemy_twelve)
                       or (enemy_type == 13 and has_enemy_thirteen)):
                    enemy_type = randint(bottom_end_enemy, top_end_enemy)

                while ((enemy_type >= 12 and (batch + 1) == total_batches and 15 < total_monsters)
                       or (enemy_type == 12 and has_enemy_twelve)
                        or enemy_type == 13 and has_enemy_thirteen):
                    enemy_type = randint(bottom_end_enemy, top_end_enemy)

                if enemy_type >= 12 and wave_number < 40:
                    match enemy_type:
                        case 12:
                            has_enemy_twelve = True
                        case 13:
                            has_enemy_thirteen = True
                    amount = randint(1, 3)
                elif enemy_type >= 12:
                    match enemy_type:
                        case 12:
                            has_enemy_twelve = True
                        case 13:
                            has_enemy_thirteen = True
                    amount = randint(5,15)
                else:
                    amount = randint(20,80)

                if amount > total_monsters:
                    amount = total_monsters
                    batch_list.append(BATCH(enemy_type, amount, threshold))
                    break

                if batch == total_batches and amount < total_monsters:
                    amount = total_monsters

                total_monsters -= amount

                batch_list.append(BATCH(enemy_type, amount, threshold))

    return batch_list

def init_waves():
    wave_list = [
        WAVE(500),
        WAVE(500),
        WAVE(800),
        WAVE(800),
        ]
    for i in range(196):
        wave_list.append(WAVE(1000+i))

    return wave_list