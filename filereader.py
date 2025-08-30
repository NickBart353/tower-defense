import csv

from tile import TILE

def read_map():
    map_array = []
    temp_array = []
    with open("maps/map1.csv","r") as file:
        reader = csv.reader(file)
        for i, line in enumerate(reader):
            for j, tile in enumerate(line):
                match tile:
                    case "0":
                        temp_array.append(TILE(j, i, int(tile), False))
                    case "1":
                        temp_array.append(TILE(j, i, int(tile), True))
                    case "2":
                        temp_array.append(TILE(j, i, int(tile), True))
                    case "3":
                        temp_array.append(TILE(j, i, int(tile), True))

            map_array.append(temp_array)
            temp_array = []
    return map_array