import pygame

from filereader import *
from enemy import *

class GAME:
    def __init__(self):
        self.screen = pygame.display.set_mode((1400, 700))
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0
        self.arr = read_map()
        self.COL, self.ROW = len(self.arr[0]), len(self.arr)
        self.COL_SIZE, self.ROW_SIZE = self.screen.get_width()/self.COL, self.screen.get_height()/self.ROW
        self.start_point, self.end_point = self.get_start_and_endpoint()
        self.enemy_list = [ENEMY(self.start_point.get("x"),self.start_point.get("y"))]
        self.last_updated = 0

    def get_start_and_endpoint(self):
        start_point, end_point = {"x": 0, "y": 0}, {"x": 0, "y": 0}

        for line in self.arr:
            for tile in line:
                match tile.field_type:
                    case 2:
                        start_point["x"] = tile.x
                        start_point["y"] = tile.y
                    case 3:
                        end_point["x"] = tile.x
                        end_point["y"] = tile.y
        return start_point, end_point

    def game_loop(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            for line in self.arr:
                for tile in line:
                    match tile.field_type:
                        case 0:
                            pygame.draw.rect(self.screen,"green",(tile.x * self.COL_SIZE,tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                        case 1:
                            pygame.draw.rect(self.screen, "brown",(tile.x * self.COL_SIZE,tile.y * self.ROW_SIZE , self.COL_SIZE,self.ROW_SIZE))
                        case 2:
                            pygame.draw.rect(self.screen, "blue",(tile.x * self.COL_SIZE,tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                        case 3:
                            pygame.draw.rect(self.screen, pygame.Color(250,250,0),(tile.x * self.COL_SIZE,tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
            now = pygame.time.get_ticks()
            for enemy in self.enemy_list:
                pygame.draw.circle(self.screen, pygame.Color(0,0,0),(enemy.x*self.COL_SIZE+self.COL_SIZE*0.5,enemy.y*self.ROW_SIZE+self.ROW_SIZE*0.5), self.COL_SIZE//2)

                if enemy.x == self.end_point["x"] and enemy.y == self.end_point["y"]:
                    self.running = False

                if now > get_move_interval() + self.last_updated:
                    self.last_updated = now

                    if self.arr[enemy.y][enemy.x + 1].can_collide_with and not enemy.i_came_from == "r":
                        enemy.x += 1
                        enemy.i_came_from = "l"
                    if self.arr[enemy.y][enemy.x - 1].can_collide_with and not enemy.i_came_from == "l":
                        enemy.x -= 1
                        enemy.i_came_from = "r"
                    if self.arr[enemy.y + 1][enemy.x].can_collide_with and not enemy.i_came_from == "d":
                        enemy.y += 1
                        enemy.i_came_from = "u"
                    if self.arr[enemy.y - 1][enemy.x].can_collide_with and not enemy.i_came_from == "u":
                        enemy.y -= 1
                        enemy.i_came_from = "d"

            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

pygame.init()
game = GAME()
game.game_loop()
pygame.quit()