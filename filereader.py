import csv

from tile import TILE

def read_map():
    map_array = []
    temp_array = []
    with open("maps/map1.csv","r") as file:
        reader = csv.reader(file)
        line_counter = 0
        for line in reader:
            num_counter = 0
            for tile in line:
                match tile:
                    case "0":
                        temp_array.append(TILE(num_counter, line_counter, int(tile), False))
                    case "1":
                        temp_array.append(TILE(num_counter, line_counter, int(tile), True))
                    case "2":
                        temp_array.append(TILE(num_counter, line_counter, int(tile), True))
                    case "3":
                        temp_array.append(TILE(num_counter, line_counter, int(tile), True))

                num_counter += 1
            map_array.append(temp_array)
            temp_array = []
            line_counter += 1
    return map_array