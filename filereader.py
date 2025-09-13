import csv

from tile import TILE

def read_map():
    map_array = []
    temp_array = []
    with open("maps/map2.csv","r") as file:
        reader = csv.reader(file)
        for i, line in enumerate(reader):
            for j, tile in enumerate(line):
                temp_array.append(TILE(j, i, int(tile), False))
            map_array.append(temp_array)
            temp_array = []
    return map_array
