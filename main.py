import pygame

from filereader import *
from enemy import *
from tower import *

class GAME:
    def __init__(self):
        #important stuff
        self.screen = pygame.display.set_mode((1400, 700))
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        #rects
        self.moving_pink_tower = None
        self.move_pink_tower = None

        #bools
        self.running = True
        self.game_running = True
        self.inventory_open = False
        self.mouse_clicked = False

        #map
        self.arr = read_map()
        self.COL, self.ROW = len(self.arr[0]), len(self.arr)
        self.COL_SIZE, self.ROW_SIZE = self.screen.get_width()/self.COL, self.screen.get_height()/self.ROW
        self.start_point, self.end_point = self.get_start_and_endpoint()
        self.tower_point_list = self.get_tower_points()

        #enemy
        self.enemy_list = [ENEMY(self.start_point.get("x"),self.start_point.get("y"), 10)]
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

    def get_tower_points(self):
        tower_point_list = []

        for line in self.arr:
            for tile in line:
                if tile.field_type == 4:
                        tower_point_list.append({"x": tile.x, "y": tile.y})
        return tower_point_list

    def main_loop(self):
        while self.running:
            if self.game_running:
                self.game_loop()


    def game_loop(self):
        while self.game_running:
            self.screen.fill((0, 0, 0))

            for line in self.arr:
                for tile in line:
                    match tile.field_type:
                        case 0:
                            pygame.draw.rect(self.screen,"green",(tile.x * self.COL_SIZE, tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                        case 1:
                            pygame.draw.rect(self.screen, "brown",(tile.x * self.COL_SIZE, tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                        case 2:
                            pygame.draw.rect(self.screen, "blue",(tile.x * self.COL_SIZE, tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                        case 4:
                            pygame.draw.rect(self.screen, "white",(tile.x * self.COL_SIZE, tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))
                            if tile.tower:
                                match tile.tower.tower_type:
                                    case "basic":
                                        pygame.draw.circle(self.screen, (255,0,255),(tile.x*self.COL_SIZE+self.COL_SIZE*0.5,tile.y*self.ROW_SIZE+self.ROW_SIZE*0.5), self.COL_SIZE//2)
                        case 3:
                            pygame.draw.rect(self.screen, (250,250,0),(tile.x * self.COL_SIZE, tile.y * self.ROW_SIZE, self.COL_SIZE,self.ROW_SIZE))

            now = pygame.time.get_ticks()
            for enemy in self.enemy_list:
                pygame.draw.circle(self.screen, (0,0,0),(enemy.x*self.COL_SIZE+self.COL_SIZE*0.5,enemy.y*self.ROW_SIZE+self.ROW_SIZE*0.5), self.COL_SIZE//2)

                if enemy.x == self.end_point["x"] and enemy.y == self.end_point["y"]:
                    enemy.x = self.start_point["x"]
                    enemy.y = self.start_point["y"]

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

            if self.inventory_open:

                overlay = pygame.Surface((self.screen.get_width()/4,self.screen.get_height()), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 180))
                self.screen.blit(overlay, (0,0))

                pink_tower_loc = (1* self.COL_SIZE,2* self.ROW_SIZE)
                pink_tower = pygame.draw.circle(self.screen, (250,0,250), pink_tower_loc,self.COL_SIZE//2)

                if pink_tower.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked:
                    self.move_pink_tower = True

                if self.move_pink_tower:
                    self.moving_pink_tower = pygame.draw.circle(self.screen, (250, 0, 250), pygame.mouse.get_pos(), self.COL_SIZE // 2)
                    for tower_point in self.tower_point_list:

                        if self.moving_pink_tower.colliderect((tower_point["x"]*self.COL_SIZE,tower_point["y"]*self.ROW_SIZE,self.COL_SIZE,self.ROW_SIZE)) and not self.mouse_clicked:
                            self.arr[tower_point["y"]][tower_point["x"]].tower = TOWER(tower_point["x"],tower_point["y"], "basic")

                if not self.mouse_clicked:
                    self.move_pink_tower = False

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if not self.inventory_open:
                            self.inventory_open = True
                        else:
                            self.inventory_open = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_clicked = False

pygame.init()
game = GAME()
game.main_loop()
pygame.quit()