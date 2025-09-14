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
                self.movement_speed = 1.5
                self.color = (200,30,30)
                self.kill_reward = 1
            case 2:
                self.health = 2
                self.damage = 3
                self.movement_speed = 1.5
                self.color = (30, 30, 200)
                self.kill_reward = 2
            case 3:
                self.health = 3
                self.damage = 3
                self.movement_speed = 2
                self.color = (79, 224, 63)
                self.kill_reward = 5
            case 4:
                self.health = 5
                self.damage = 5
                self.movement_speed = 2
                self.color = (210, 70, 232)
                self.kill_reward = 5
            case 5:
                self.health = 7
                self.damage = 5
                self.movement_speed = 3
                self.color = (255, 255, 255)
                self.kill_reward = 5
            case 6:
                self.health = 10
                self.damage = 5
                self.movement_speed = 2
                self.color = (0, 0, 0)
                self.kill_reward = 6
            case 7:
                self.health = 15
                self.damage = 10
                self.movement_speed = 4
                self.color = (31, 236, 255)
                self.kill_reward = 10
            case 8:
                self.health = 3
                self.damage = 5
                self.movement_speed = 8
                self.color = (233, 255, 38)
                self.kill_reward = 5
            case 9:
                self.health = 50
                self.damage = 10
                self.movement_speed = 2
                self.color = (208, 99, 255)
                self.kill_reward = 15
            case 10:
                self.health = 100
                self.damage = 10
                self.movement_speed = 4
                self.color = (255, 51, 139)
                self.kill_reward = 15
            case 11:
                self.health = 250
                self.damage = 10
                self.movement_speed = 5
                self.color = (255, 186, 59)
                self.kill_reward = 15
            case 12:
                self.health = 500
                self.damage = 100
                self.movement_speed = 0.4
                self.color = (255, 173, 231)
                self.kill_reward = 50
            case 13:
                self.health = 1000
                self.damage = 100
                self.movement_speed = 0.2
                self.color = (203, 255, 191)
                self.kill_reward = 100
        self.current_health = self.health

def enemy_list_data():
    return {
        "0":{
            "0":{
                "ENEMY_TYPE":1,
                "AMOUNT": 15,
            },
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
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
            "1": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
        },
        "3": {
            "0": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
            "2": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
        },
        "4": {
            "0": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 3,
            },
            "3": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 15,
            },
        },
        "5": {
            "0": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 20,
            },
        },
        "6": {
            "0": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 50,
            },
        },
        "7": {
            "0": {
                "ENEMY_TYPE": 6,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 40,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
        },
        "8": {
            "0": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 40,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 6,
                "AMOUNT": 30,
            },

        },
        "9": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 30,
            },
        },
        "10": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 10,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 30,
            },
        },
        "11": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 100,
            },
            "3": {
                "ENEMY_TYPE": 11,
                "AMOUNT": 10,
            },
        },
        "12": {
            "0": {
                "ENEMY_TYPE": 10,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 11,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 12,
                "AMOUNT": 2,
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