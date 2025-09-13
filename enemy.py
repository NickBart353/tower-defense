import pygame
class ENEMY:
    def __init__(self, enemy_type, x = 0, y = 0):
        self.x = x
        self.y = y
        self.enemy_rect = pygame.Rect(0,0,0,0)
        self.last_time_moved = 0
        self.last_hit_by = None

        match enemy_type:
            case 1:
                self.health = 1
                self.damage = 1
                self.movement_speed = 2
                self.color = (200,30,30)
                self.kill_reward = 2
            case 2:
                self.health = 2
                self.damage = 3
                self.movement_speed = 2
                self.color = (30, 30, 200)
                self.kill_reward = 5
        self.current_health = self.health

def enemy_list_data():
    return {
        "0":{
            "0":{
                "ENEMY_TYPE":1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 10,
            }

        },
        "1":{
            "0":{
                "ENEMY_TYPE":1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "2": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "3": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "4": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "5": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "6": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "7": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "8": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "9": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "10": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "11": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "12": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "13": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "14": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "15": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "16": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "17": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "18": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "19": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "20": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
    }

def generate_list_from_data(wave_num):
    wave_list = []
    enemy_data = enemy_list_data()
    for wave_num_key, enemy_list in enemy_data.items():
        if str(wave_num) == wave_num_key:
            for enemy_batch_num, enemy_obj in enemy_list.items():
                temp_enemy_list = []
                for i in range(0, enemy_obj["AMOUNT"]):

                    temp_enemy_list.append(ENEMY(int(enemy_obj["ENEMY_TYPE"]),0,0,))
                wave_list.append(temp_enemy_list)
            break

    return wave_list