from random import randint
from classes.enemy import *
from classes.batch import BATCH

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

    def spawn_enemy(self, start_dict, speed_multiplier=1.0):
        now = pygame.time.get_ticks()
        if len(self.enemy_list) > 0:
            # Adjust spawn threshold based on speed multiplier
            adjusted_threshold = self.enemy_list[0].spawn_threshold / speed_multiplier
            if now > self.last_time_spawned + adjusted_threshold:
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
            total_monsters = 10 * wave_number
            total_batches = total_monsters // (randint(5,30))

            top_end_enemy = 12
            bottom_end_enemy = 1
            top_end_threshold = 300
            bottom_end_threshold = 100
            if wave_number < 15:
                top_end_enemy = 9
                bottom_end_enemy = 4
                top_end_threshold = 300
                bottom_end_threshold = 100
            if 14 < wave_number < 20:
                top_end_enemy = 11
                bottom_end_enemy = 6
                top_end_threshold = 250
                bottom_end_threshold = 100
            if 19 < wave_number < 25:
                top_end_enemy = 13
                bottom_end_enemy = 9
                top_end_threshold = 250
                bottom_end_threshold = 80
            if 24 < wave_number < 30:
                top_end_enemy = 14
                bottom_end_enemy = 11
                top_end_threshold = 250
                bottom_end_threshold = 80
            if 29 < wave_number < 35:
                top_end_enemy = 15
                bottom_end_enemy = 12
                top_end_threshold = 200
                bottom_end_threshold = 50
            if 34 < wave_number < 40:
                top_end_enemy = 20
                bottom_end_enemy = 14
                top_end_threshold = 100
                bottom_end_threshold = 50
            if 39 < wave_number < 45:
                top_end_threshold = 50
                bottom_end_threshold = 30
            if 44 < wave_number < 50:
                top_end_threshold = 30
                bottom_end_threshold = 20
            if 49 < wave_number < 55:
                top_end_threshold = 30
                bottom_end_threshold = 15
            if 54 < wave_number < 60:
                top_end_threshold = 15
                bottom_end_threshold = 5

            for batch in range(total_batches):
                threshold = randint(bottom_end_threshold,top_end_threshold)

                enemy_type = randint(bottom_end_enemy, top_end_enemy)

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