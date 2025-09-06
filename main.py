import math
import pygame

from filereader import *
from enemy import *
from tower import *
from bullet import *
from wave import *
from button import BUTTON
from timed_text import TIMER

class GAME:
    def __init__(self):
        #important stuff
        self.right_mouse_clicked = False
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((1400,700))
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        #rects
        self.pink_tower = pygame.Rect(0,0,0,0)
        self.gray_tower = pygame.Rect(0,0,0,0)
        self.orange_tower = pygame.Rect(0,0,0,0)

        #bools
        self.running = True
        self.game_running = True
        self.inventory_open = False
        self.updates_open = False
        self.mouse_clicked = False
        self.mouse_clicked_once = False
        self.move_pink_tower = False
        self.move_orange_tower = None
        self.move_gray_tower = None
        self.pause_menu = False

        #map
        self.arr = read_map()
        self.COL, self.ROW = len(self.arr[0]), len(self.arr)
        self.COL_SIZE, self.ROW_SIZE = self.screen.get_width()/self.COL, (self.screen.get_height()) / (self.ROW+1)
        self.start_point, self.end_point = self.get_start_and_endpoint()

        #ui
        self.sidebar_size = self.COL_SIZE*6
        self.tower_overlay = pygame.Surface((self.sidebar_size, self.screen.get_height()), pygame.SRCALPHA)
        self.tower_overlay.fill((255, 255, 255, 180))
        self.upgrade_overlay = pygame.Surface((self.sidebar_size, self.screen.get_height()), pygame.SRCALPHA)
        self.upgrade_overlay.fill((255, 255, 255, 180))

        self.header_size = self.ROW_SIZE

        #fonts
        self.font = pygame.font.Font("assets/font/Enchanted Land.otf",40)

        #animations
        self.wave_timer = TIMER(self.font, (0,0,0), 15, self.screen.get_width()/4*3, 5)

        #buttons
        self.tower_overlay_button = BUTTON(1,1,self.COL_SIZE - 2,self.header_size - 2,
                                           lambda: self.overlay_button(),
                                           color_default = (230, 203, 158), color_hover = (196, 173, 135))

        self.pause_menu_button = BUTTON(self.screen.get_width()-self.COL_SIZE+1,1,self.COL_SIZE - 2,self.header_size - 2,
                                        lambda: self.pause_button(),
                                        color_default = (230, 203, 158), color_hover = (196, 173, 135))

        self.skip_timer_button = BUTTON(self.screen.get_width()/4*2.8,1,self.COL_SIZE - 2,self.header_size - 2,
                                        lambda: self.skip_button(),
                                        color_default = (100, 100, 100), color_hover = (150, 150, 150))

        #enemy and wave
        self.wave_list = init_waves()
        self.wave_counter = 0
        self.enemies_spawned = 0
        self.enemy_list = []

        #tower
        self.tower_list = []
        self.tower_counter = 0
        self.tower_point_list = self.get_tower_points()
        self.cost_dict = {"basic": get_tower_cost("basic"),
                          "circle": get_tower_cost("circle"),
                          "arc": get_tower_cost("arc"),}
        self.tower_to_upgrade = None

        #colors
        self.pink_color = (250, 0, 250)
        self.gray_color = (150, 150, 150)
        self.orange_color = (250, 170, 30)
        self.tower_overlay_button_color = (196, 173, 135)

        #player
        self.player_max_health = 100
        self.player_health = self.player_max_health
        self.player_money = 500
        self.score = 0
        self.highscore = 0

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
                if tile.field_type == 0:
                        tower_point_list.append({"x": tile.x, "y": tile.y, "has_tower": False})
        return tower_point_list

    def main_loop(self):
        while self.running:
            if self.game_running:
                self.game_loop()
            if self.pause_menu:
                self.pause_loop()

    def game_loop(self):

        while self.game_running:

            self.update_wave()

            self.draw_main_playing_field()

            if self.wave_timer.played_wave_timer:
                self.draw_enemies()
                self.spawn_enemy_from_wave()

            self.draw_towers()

            self.draw_bullets()

            self.draw_header()

            self.towers_fire()

            self.check_bullet_enemy_collision()

            self.draw_player_health_bar()

            if self.inventory_open:
                self.draw_tower_overlay()

            self.draw_upgrade_overlay()

            self.move_towers()

            if not self.wave_timer.played_wave_timer:
                self.wave_timer.count_down_text(self.screen)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000

            #reset variables FUNC SOON
            self.mouse_clicked_once = False

            self.get_events()

    def pause_loop(self):
        menu_rect = pygame.Rect(self.screen.get_width()/2-100,self.screen.get_height()/2-200,200,400)
        continue_button = BUTTON(self.screen.get_width()/2-80, self.screen.get_height()/2-180, 160, 30,
                                 lambda: self.continue_button(),
                                 color_default = (0,255,0), color_hover = (0,200,0), text = "Continue", font=self.font, text_color=(0,0,0))

        exit_game_button = BUTTON(self.screen.get_width()/2-80, self.screen.get_height()/2+150, 160, 30,
                                 lambda: self.exit_game_button(),
                                 color_default = (255,0,0), color_hover = (200,0,0), text = "Exit", font=self.font, text_color=(0,0,0))

        while self.pause_menu:

            pygame.draw.rect(self.screen, (255,255,255),menu_rect)

            continue_button.draw_from_color(self.screen)
            continue_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            exit_game_button.draw_from_color(self.screen)
            exit_game_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            pygame.display.update(menu_rect)
            self.delta_time = self.clock.tick(60) / 1000

            self.get_events()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_button()
                if event.key == pygame.K_TAB:
                    self.overlay_button()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked_once = True
                    self.mouse_clicked = True
                if event.button == 3:
                    self.right_mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_clicked = False
                if event.button == 3:
                    self.right_mouse_clicked = False

    def spawn_enemy_from_wave(self):
        if len(self.wave_list[self.wave_counter].enemy_list) > 0:
            enemy = self.wave_list[self.wave_counter].spawn_enemy(self.start_point)
            if enemy:
                self.enemy_list.append(enemy)
                self.enemies_spawned += 1

    def update_wave(self):
        if len(self.enemy_list) <= 0 and len(self.wave_list[self.wave_counter].enemy_list) <= 0:
            self.wave_counter += 1
            self.wave_timer.played_wave_timer = False
            self.player_money += self.wave_list[self.wave_counter].money_reward

    def draw_main_playing_field(self):
        self.screen.fill((0, 0, 0))

        for line in self.arr:
            for tile in line:
                match tile.field_type:
                    case 0:
                        pygame.draw.rect(self.screen, (0,120,30),
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case 1:
                        pygame.draw.rect(self.screen, (115, 72, 23),
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case 2:
                        pygame.draw.rect(self.screen, (0,0,200),
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case 3:
                        pygame.draw.rect(self.screen, (250, 250, 0),
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))

    def draw_enemies(self):
        now = pygame.time.get_ticks()
        for enemy in self.enemy_list:
            enemy.enemy_rect = pygame.draw.circle(self.screen, (0, 0, 0), (enemy.x * self.COL_SIZE + self.COL_SIZE * 0.5,
                                                        (enemy.y * self.ROW_SIZE + self.ROW_SIZE * 0.5)+self.header_size), self.COL_SIZE // 2)
            pygame.draw.rect(self.screen, (0,0,0), ((enemy.x * self.COL_SIZE)-1, (((enemy.y+0.8) * self.ROW_SIZE)-1)+self.header_size, self.COL_SIZE+2, 12))
            pygame.draw.rect(self.screen, (255,0,0),((enemy.x * self.COL_SIZE), (enemy.y + 0.8) * self.ROW_SIZE+self.header_size, self.COL_SIZE,10))
            pygame.draw.rect(self.screen, (0,255,0),((enemy.x * self.COL_SIZE), ((enemy.y + 0.8) * self.ROW_SIZE)+self.header_size, self.COL_SIZE/enemy.health*enemy.current_health,10))

            if enemy.x == self.end_point["x"] and enemy.y == self.end_point["y"]:
                self.player_health -= enemy.damage
                self.enemy_list.remove(enemy)

            if now > enemy.movement_interval + enemy.last_time_moved:
                enemy.last_time_moved = now

                if self.arr[enemy.y][enemy.x + 1].can_collide_with and not enemy.i_came_from == "r":
                    enemy.x += 1
                    enemy.i_came_from = "l"
                    continue
                if self.arr[enemy.y][enemy.x - 1].can_collide_with and not enemy.i_came_from == "l":
                    enemy.x -= 1
                    enemy.i_came_from = "r"
                    continue
                if self.arr[enemy.y + 1][enemy.x].can_collide_with and not enemy.i_came_from == "d":
                    enemy.y += 1
                    enemy.i_came_from = "u"
                    continue
                if self.arr[enemy.y - 1][enemy.x].can_collide_with and not enemy.i_came_from == "u":
                    enemy.y -= 1
                    enemy.i_came_from = "d"
                    continue

    def draw_towers(self):
        for tower in self.tower_list:
            tower.rect = pygame.draw.circle(self.screen, tower.color,(tower.x * self.COL_SIZE + self.COL_SIZE * 0.5,
                                     (tower.y * self.ROW_SIZE + self.ROW_SIZE * 0.5)+self.header_size), self.COL_SIZE // 2)

    def draw_tower_overlay(self):
        self.screen.blit(self.tower_overlay, (0, self.header_size))

        temp_pink_tower = TOWER(1 * self.COL_SIZE, 4 * self.ROW_SIZE, "circle", self.COL_SIZE, self.ROW_SIZE, self.pink_color)
        temp_gray_tower = TOWER(1 * self.COL_SIZE, 5 * self.ROW_SIZE, "basic", self.COL_SIZE, self.ROW_SIZE, self.gray_color)
        temp_orange_tower = TOWER(1 * self.COL_SIZE, 6 * self.ROW_SIZE, "arc", self.COL_SIZE, self.ROW_SIZE, self.orange_color)

        self.pink_tower = temp_pink_tower.draw(self.screen, self.COL_SIZE // 2)
        self.gray_tower = temp_gray_tower.draw(self.screen, self.COL_SIZE // 2)
        self.orange_tower = temp_orange_tower.draw(self.screen, self.COL_SIZE // 2)

        self.screen.blit(self.font.render("{}".format(temp_pink_tower.cost),True,(0,0,0)),(2 * self.COL_SIZE, 3.5 * self.ROW_SIZE))
        self.screen.blit(self.font.render("{}".format(temp_gray_tower.cost), True, (0, 0, 0)), (2 * self.COL_SIZE, 4.5 * self.ROW_SIZE))
        self.screen.blit(self.font.render("{}".format(temp_orange_tower.cost), True, (0, 0, 0)),(2 * self.COL_SIZE, 5.5 * self.ROW_SIZE))

    def draw_upgrade_overlay(self):

        if self.updates_open:
            self.screen.blit(self.upgrade_overlay, (0, self.header_size))
            self.screen.blit(self.font.render("Upgrades", True, (0,0,0)), (1 * self.COL_SIZE, self.header_size))

        if self.tower_to_upgrade is not None:
            if self.tower_to_upgrade.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once and self.updates_open:
                self.updates_open = False
                self.tower_to_upgrade = None
                self.mouse_clicked_once = False

        for tower in self.tower_list:
            if tower.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once and not self.updates_open:
                self.updates_open = True
                self.inventory_open = False
                self.tower_to_upgrade = tower
                self.mouse_clicked_once = False

    def draw_bullets(self):
        for tower in self.tower_list:
            for bullet in tower.bullet_list:
                bullet.bullet_rect = pygame.draw.circle(self.screen, (255, 0, 0), (bullet.my_x*self.COL_SIZE, (bullet.my_y*self.ROW_SIZE)+self.header_size), self.COL_SIZE // 6)

                ang = math.atan2(bullet.y_vec, bullet.x_vec)
                bullet.my_x += math.cos(ang) * bullet.velocity * self.delta_time
                bullet.my_y += math.sin(ang) * bullet.velocity * self.delta_time

                bullet.distance -= bullet.velocity/2

                if bullet.distance <= 0:
                    tower.bullet_list.remove(bullet)

    def draw_header(self):

        pygame.draw.rect(self.screen, (128, 106, 70),(0,0,self.screen.get_width(),self.header_size))

        self.tower_overlay_button.draw_from_color(self.screen)
        self.tower_overlay_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

        self.pause_menu_button.draw_from_color(self.screen)
        self.pause_menu_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

        if not self.wave_timer.played_wave_timer:
            self.skip_timer_button.draw_from_color(self.screen)
            self.skip_timer_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

        self.screen.blit(self.font.render("{m}$".format(m = self.player_money), True, (0,0,0)),
                         (self.screen.get_width()/4*0.8, 5))
        self.screen.blit(self.font.render("Wave {c}".format(c = self.wave_counter+1), True, (255, 255, 255)),
                         (self.screen.get_width()/4*0.3, 5))

    def draw_player_health_bar(self):
        pygame.draw.rect(self.screen, (0, 0, 0),(self.screen.get_width()/2 - 102, self.header_size/4-2, 204, self.header_size/2+4))
        pygame.draw.rect(self.screen, (255, 0, 0),(self.screen.get_width()/2 - 100, self.header_size/4, 200, self.header_size/2))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.screen.get_width()/2 - 100, self.header_size/4, 200 / self.player_max_health * self.player_health, self.header_size/2))

    def move_towers(self):

        if self.cost_dict["circle"] <= self.player_money:
            self.move_pink_tower = self.check_clicked_tower(self.pink_tower, self.move_pink_tower)
            self.click_and_drag_tower(self.move_pink_tower, self.pink_color, "circle")

        if self.cost_dict["basic"] <= self.player_money:
            self.move_gray_tower = self.check_clicked_tower(self.gray_tower, self.move_gray_tower)
            self.click_and_drag_tower(self.move_gray_tower, self.gray_color, "basic")

        if self.cost_dict["arc"] <= self.player_money:
            self.move_orange_tower = self.check_clicked_tower(self.orange_tower, self.move_orange_tower)
            self.click_and_drag_tower(self.move_orange_tower, self.orange_color, "arc")

        if not self.mouse_clicked or self.right_mouse_clicked:
            self.reset_moving_tower()

    def check_clicked_tower(self, tower_rect, moving_bool):
        if tower_rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked:
            self.tower_counter = 1
            moving_bool = True
        return moving_bool

    def click_and_drag_tower(self, moving_bool, color, turret_type):
        if moving_bool:
            tower_rect = pygame.draw.circle(self.screen, color, pygame.mouse.get_pos(),self.COL_SIZE // 2)
            for tower_point in self.tower_point_list:
                if tower_rect.colliderect((tower_point["x"] * self.COL_SIZE, tower_point["y"] * self.ROW_SIZE+self.header_size, self.COL_SIZE,self.ROW_SIZE)) and not self.mouse_clicked and self.tower_counter > 0:
                    if not tower_point["has_tower"]:
                        self.tower_list.append(TOWER(tower_point["x"], tower_point["y"],turret_type, self.COL_SIZE, self.ROW_SIZE, color))
                        self.player_money -= self.cost_dict[turret_type]
                        self.tower_counter -= 1
                        tower_point["has_tower"] = True
                    else:
                        self.reset_moving_tower()

    def reset_moving_tower(self):
        self.move_pink_tower = False
        self.move_gray_tower = False
        self.move_orange_tower = False
        self.tower_counter = 0

    def towers_fire(self):
        for tower in self.tower_list:
            for enemy in self.enemy_list:
                if tower.radius_rect_circle.colliderect(enemy.enemy_rect):
                    tower.fire(enemy)

    def check_bullet_enemy_collision(self):
        for tower in self.tower_list:
            for bullet in tower.bullet_list:
                for enemy in self.enemy_list:
                    if enemy.enemy_rect.colliderect(bullet.bullet_rect):
                        enemy.current_health -= bullet.damage
                        if bullet in tower.bullet_list: tower.bullet_list.remove(bullet)
                    if enemy.current_health <= 0:
                        if enemy in self.enemy_list: self.enemy_list.remove(enemy)

    def overlay_button(self):
        if not self.inventory_open:
            self.inventory_open = True
            self.updates_open = False
        elif self.inventory_open:
            self.inventory_open = False

    def pause_button(self):
        if self.pause_menu:
            self.pause_menu = False
            self.game_running = True
        else:
            self.pause_menu = True
            self.game_running = False

    def continue_button(self):
        self.pause_menu = False
        self.game_running = True

    def exit_game_button(self):
        self.pause_menu = False
        self.running = False

    def skip_button(self):
        self.wave_timer.second_counter = 0


pygame.init()
game = GAME()
game.main_loop()
pygame.quit()