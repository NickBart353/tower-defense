import csv

from tile import TILE

def read_map(map_location):
    map_array = []
    temp_array = []
    with open("{}".format(map_location), "r") as file:
        reader = csv.reader(file)
        for i, line in enumerate(reader):
            for j, tile in enumerate(line):
                temp_array.append(TILE(j, i, int(tile), False))
            map_array.append(temp_array)
            temp_array = []
    return map_array

def get_map_data():
    return {
        "0":{
            "name": "Grasslands",
            "name_val": "grass",
            "file": "maps/grass.csv",
            "background_color": (0,120,30),
            "path_color": (115, 72, 23),
            "start_color": (250, 250, 0),
            "end_color": (36, 32, 22),
            "obstacle_color": (158, 158, 158),
        },
        "1":{
            "name": "Snowy Mountains",
            "name_val": "snow",
            "file": "maps/snow.csv",
            "background_color": (201, 230, 255),
            "path_color": (150, 207, 255),
            "start_color": (108, 245, 192),
            "end_color": (64, 108, 184),
            "obstacle_color": (95, 152, 245),
        },
        # "2": {
        #     "name": "Dunes",
        #     "name_val": "desert",
        #     "file": "maps/desert.csv",
        #     "background_color": (252, 218, 78),
        #     "path_color": (255, 249, 181),
        #     "start_color": (255, 164, 28),
        #     "end_color": (153, 149, 103),
        #     "obstacle_color": (255, 247, 0),
        # },
        "2": {
            "name": "Dunes",
            "name_val": "desert",
            "file": "maps/desert.csv",
            "background_color": (244, 228, 188),
            "path_color": (205, 170, 125),
            "start_color": (95, 158, 160),
            "end_color": (200, 80, 50),
            "obstacle_color": (139, 125, 107),
        },
    }