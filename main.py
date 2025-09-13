import math
import pygame

from filereader import *
from enemy import *
from tower import *
from bullet import *
from wave import *
from button import BUTTON
from timed_text import TIMER
from upgrade import *
from tile import *

class GAME:
    # <editor-fold desc="init funcs">
    def __init__(self):
        #important stuff
        self.right_mouse_clicked = False
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1400,700))
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        #rects
        self.pink_tower = pygame.Rect(0,0,0,0)
        self.gray_tower = pygame.Rect(0,0,0,0)
        self.orange_tower = pygame.Rect(0,0,0,0)

        #bools
        self.running = True
        self.game_running = False
        self.pause_menu = False
        self.main_menu = True
        self.map_picker = False

        self.inventory_open = False
        self.upgrades_open = False
        self.mouse_clicked = False
        self.mouse_clicked_once = False
        self.move_pink_tower = False
        self.move_orange_tower = None
        self.move_gray_tower = None

        #map
        self.map_dict = get_map_data()
        self.arr = read_map(self.map_dict["0"]["file"])
        self.COL, self.ROW = len(self.arr[0]), len(self.arr)
        self.COL_SIZE, self.ROW_SIZE = self.screen.get_width()/self.COL, (self.screen.get_height()) / (self.ROW+1)

        self.start_point, self.end_point, self.END = 0, 0, 0

        self.path = []
        self.map_selection = None

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

        self.upgrade_one_color = (23, 48, 138)
        self.upgrade_one_color_hover = (23, 48, 168)

        self.upgrade_two_color = (23, 138, 48)
        self.upgrade_two_color_hover = (23, 168, 48)

        self.upgrade_three_color = (138, 48, 23)
        self.upgrade_three_color_hover = (168, 48, 23)

        self.upgrade_button_one = BUTTON(self.COL_SIZE * 1 + 1, self.ROW_SIZE * 3 + self.header_size + 1, self.COL_SIZE - 2,
                                self.ROW_SIZE - 2,
                                lambda: self.buy_upgrade_one(),
                                color_default=self.upgrade_one_color, color_hover=self.upgrade_one_color_hover)

        self.upgrade_button_two = BUTTON(self.COL_SIZE * 1 + 1, self.ROW_SIZE * 5 + self.header_size + 1,
                                         self.COL_SIZE - 2,
                                         self.ROW_SIZE - 2,
                                         lambda: self.buy_upgrade_two(),
                                         color_default=self.upgrade_two_color, color_hover=self.upgrade_two_color_hover)

        self.upgrade_button_three = BUTTON(self.COL_SIZE * 1 + 1, self.ROW_SIZE * 7 + self.header_size + 1,
                                         self.COL_SIZE - 2,
                                         self.ROW_SIZE - 2,
                                         lambda: self.buy_upgrade_three(),
                                         color_default=self.upgrade_three_color, color_hover=self.upgrade_three_color_hover)

        self.sell_tower_btn = BUTTON(self.COL_SIZE * 1, self.ROW_SIZE * 12 + self.header_size + 1, self.COL_SIZE * 2, self.ROW_SIZE * 1,
                                        lambda: self.sell_tower_button(),
                                        (225,0,0), (255,0,0), text = "Sell", text_color=(255,255,255), font=self.font)

        #enemy and wave
        self.wave_list = init_waves()
        self.wave_counter = 0
        self.enemies_spawned = 0
        self.enemy_list = []

        #tower
        self.tower_list = []
        self.tower_counter = 0
        self.tower_point_list = None
        self.cost_dict = {"basic": get_tower_cost("basic"),
                          "circle": get_tower_cost("circle"),
                          "arc": get_tower_cost("arc"),}
        self.tower_to_upgrade = None

        #colors
        self.pink_color = (250, 0, 250)
        self.gray_color = (150, 150, 150)
        self.orange_color = (250, 170, 30)
        self.tower_overlay_button_color = (196, 173, 135)
        self.tower_drag_radius_color = (50, 50, 50, 50)

        #player
        self.player_max_health = 100
        self.player_health = self.player_max_health
        self.player_money = 500
        self.score = 0
        self.highscore = 0

        #upgrade data
        self.tower_upgrade_data = get_upgrade_data()

    def get_start_and_endpoint(self):
        start_point, end_point = {"x": 0, "y": 0}, {"x": 0, "y": 0}
        end = int(len(self.path))
        for line in self.arr:
            for tile in line:
                match tile.field_type:
                    case 1:
                        start_point["x"] = tile.x
                        start_point["y"] = tile.y
                    case end:
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
    # </editor-fold>

    # <editor-fold desc="loops">
    def main_loop(self):
        while self.running:
            if self.game_running:
                self.game_loop()
            if self.pause_menu:
                self.pause_loop()
            if self.main_menu:
                self.main_menu_loop()
            if self.map_picker:
                self.map_pick_loop()

    def game_loop(self):

        while self.game_running:

            self.update_wave()

            self.draw_main_playing_field()

            if self.wave_timer.played_wave_timer:
                self.draw_enemies()
                self.spawn_enemy_from_wave()

            self.draw_towers()

            self.draw_bullets()

            self.towers_fire()

            self.check_bullet_enemy_collision()

            self.check_player_health()

            self.draw_tower_overlay()

            self.move_towers()

            self.draw_upgrade_overlay()

            self.draw_header()

            self.draw_player_health_bar()

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

    def main_menu_loop(self):
        title_screen_image = pygame.image.load("assets/img/main-menu/title_screen.png").convert()
        title_screen_image = pygame.transform.scale(title_screen_image, (self.screen.get_width(), self.screen.get_height()))

        start_game_button = BUTTON(self.screen.get_width()/2-80, self.screen.get_height()/2-100, 160, 50,
                                   lambda: self.play_game(),
                                   text = "Play", color_default=(0,225,0), color_hover=(0,255,0), font = self.font, text_color=(0,0,0))

        quit_game_button = BUTTON(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 , 160, 50,
                                   lambda: self.exit_game_button(),
                                   text="Quit", color_default=(225, 0, 0), color_hover=(255, 0, 0), font=self.font, text_color=(0,0,0))

        while self.main_menu:
            self.screen.blit(title_screen_image, (0, 0))

            start_game_button.draw_from_color(self.screen)
            start_game_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            quit_game_button.draw_from_color(self.screen)
            quit_game_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            self.delta_time = self.clock.tick(60) / 1000
            pygame.display.update()

            self.get_events()

    def map_pick_loop(self):
        title_screen_image_blurred = pygame.image.load("assets/img/main-menu/title_screen_blurred.png").convert()
        title_screen_image_blurred = pygame.transform.scale(title_screen_image_blurred, (self.screen.get_width(), self.screen.get_height()))

        select_map_button = BUTTON(self.screen.get_width()/2-150, self.screen.get_height() / 1.1, 300, 50,
                                   lambda: self.select_and_play_map(),
                                   text = "Select   Map", color_default=(0,225,0), color_hover=(0,255,0), font = self.font, text_color=(0,0,0))

        back_button = BUTTON(self.screen.get_width() / 20, self.screen.get_height() / 1.1  , 160, 50,
                                   lambda: self.back_to_main_menu(),
                                   text="Back", color_default=(225, 0, 0), color_hover=(255, 0, 0), font=self.font, text_color=(0,0,0))

        map_button_list = []
        temp_counter = 0
        square_width = self.screen.get_width() / 6
        square_height = 300
        total_squares_width = 3 * square_width
        total_gap_width = self.screen.get_width() - total_squares_width
        gap_size = total_gap_width / 4

        for i, (key, value) in enumerate(self.map_dict.items()):
            map_button_list.append(BUTTON((gap_size * (temp_counter + 1)) + (square_width * temp_counter), self.screen.get_height() / 3, square_width, square_height,
                                          lambda: self.select_map(i),
                                          color_default=(value["background_color"]), color_hover=(255, 255, 255)))
            temp_counter += 1
            if temp_counter == 3: temp_counter = 0

        while self.map_picker:
            self.screen.blit(title_screen_image_blurred, (0, 0))

            for i, button in enumerate(map_button_list):
                if i == self.map_selection:
                    pygame.draw.rect(self.screen, (0,0,0), (button.rect.x-2, button.rect.y-2, button.rect.width+4, button.rect.height+4))
                button.draw_from_color(self.screen)
                button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            select_map_button.draw_from_color(self.screen)
            select_map_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            back_button.draw_from_color(self.screen)
            back_button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

            self.delta_time = self.clock.tick(60) / 1000
            pygame.display.update()

            self.mouse_clicked_once = False
            self.get_events()

    # </editor-fold>

    # <editor-fold desc="funcs & more">
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game_button()
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
        enemy = self.wave_list[self.wave_counter].spawn_enemy(self.start_point)
        if enemy:
            enemy.on_tile = 1
            self.enemy_list.append(enemy)
            self.enemies_spawned += 1

    def update_wave(self):
        if len(self.enemy_list) <= 0 and len(self.wave_list[self.wave_counter].enemy_list) <= 0:
            self.player_money += self.wave_list[self.wave_counter].money_reward
            self.wave_counter += 1
            self.wave_timer.played_wave_timer = False

    def draw_main_playing_field(self):
        self.screen.fill((0, 0, 0))

        for line in self.arr:
            for tile in line:
                match tile.field_type:
                    case 0:
                        tile.rect = pygame.draw.rect(self.screen, self.map_dict[str(self.map_selection)]["background_color"],
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case 1:
                        tile.rect = pygame.draw.rect(self.screen, self.map_dict[str(self.map_selection)]["start_color"],
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case self.END:
                        tile.rect = pygame.draw.rect(self.screen, self.map_dict[str(self.map_selection)]["end_color"],
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case -1:
                        tile.rect = pygame.draw.rect(self.screen, self.map_dict[str(self.map_selection)]["obstacle_color"],
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE)+self.header_size, self.COL_SIZE, self.ROW_SIZE))
                    case _:
                        tile.rect = pygame.draw.rect(self.screen, self.map_dict[str(self.map_selection)]["path_color"],
                                         (tile.x * self.COL_SIZE, (tile.y * self.ROW_SIZE) + self.header_size,self.COL_SIZE, self.ROW_SIZE))

    def draw_enemies(self):
        for enemy in self.enemy_list:
            enemy.enemy_rect = pygame.draw.circle(self.screen, enemy.color, (enemy.x * self.COL_SIZE + self.COL_SIZE * 0.5,
                                                        (enemy.y * self.ROW_SIZE + self.ROW_SIZE * 0.5)+self.header_size), self.COL_SIZE // 2)

            pygame.draw.rect(self.screen, (0,0,0), ((enemy.x * self.COL_SIZE)-1, (((enemy.y+0.8) * self.ROW_SIZE)-1)+self.header_size, self.COL_SIZE+2, 12))
            pygame.draw.rect(self.screen, (255,0,0),((enemy.x * self.COL_SIZE), (enemy.y + 0.8) * self.ROW_SIZE+self.header_size, self.COL_SIZE,10))
            pygame.draw.rect(self.screen, (0,255,0),((enemy.x * self.COL_SIZE), ((enemy.y + 0.8) * self.ROW_SIZE)+self.header_size, self.COL_SIZE/enemy.health*enemy.current_health,10))

            ang = math.atan2(self.path[enemy.on_tile].y - self.path[enemy.on_tile-1].y, self.path[enemy.on_tile].x - self.path[enemy.on_tile-1].x)
            enemy.x += math.cos(ang) * enemy.movement_speed * self.delta_time
            enemy.y += math.sin(ang) * enemy.movement_speed * self.delta_time

            temp_x = self.path[enemy.on_tile].x - self.path[enemy.on_tile - 1].x
            temp_y = self.path[enemy.on_tile].y - self.path[enemy.on_tile - 1].y

            temp_x_bool = False
            temp_y_bool = False

            if temp_x < 0:
                if self.path[enemy.on_tile].x >= enemy.x:
                    temp_x_bool = True
            elif temp_x > 0:
                if self.path[enemy.on_tile].x <= enemy.x:
                    temp_x_bool = True
            elif temp_x == 0:
                temp_x_bool = True
            if temp_y < 0:
                if self.path[enemy.on_tile].y >= enemy.y:
                    temp_y_bool = True
            elif temp_y > 0:
                if self.path[enemy.on_tile].y <= enemy.y:
                    temp_y_bool = True
            elif temp_y == 0:
                temp_y_bool = True

            if temp_x_bool and temp_y_bool:
                enemy.on_tile += 1
                if enemy.on_tile == len(self.path):
                    self.player_health -= enemy.damage
                    self.enemy_list.remove(enemy)

    def draw_towers(self):
        for tower in self.tower_list:
            tower.rect = pygame.draw.circle(self.screen, tower.color,(tower.x * self.COL_SIZE + self.COL_SIZE * 0.5,
                                     (tower.y * self.ROW_SIZE + self.ROW_SIZE * 0.5)+self.header_size), self.COL_SIZE // 2)

    def draw_tower_overlay(self):
        if self.inventory_open:
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

            for line in self.arr:
                for tile in line:
                    if tile.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once and not self.upgrade_overlay.get_rect().collidepoint(pygame.mouse.get_pos()):
                        self.inventory_open = False

    def draw_upgrade_overlay(self):

        if self.upgrades_open:

            self.draw_tower_radius(self.tower_to_upgrade, self.tower_drag_radius_color)

            self.screen.blit(self.upgrade_overlay, (0, self.header_size))
            self.screen.blit(self.font.render("Upgrades", True, (0, 0, 0)), (1 * self.COL_SIZE, self.header_size))

            upgrade_one_cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["1"]["{}".format(self.tower_to_upgrade.upgrade_one_counter)]["cost"]
            upgrade_one_text = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["1"]["{}".format(self.tower_to_upgrade.upgrade_one_counter)]["text"]

            upgrade_two_cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["2"]["{}".format(self.tower_to_upgrade.upgrade_two_counter)]["cost"]
            upgrade_two_text = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["2"]["{}".format(self.tower_to_upgrade.upgrade_two_counter)]["text"]

            upgrade_three_cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["3"]["{}".format(self.tower_to_upgrade.upgrade_three_counter)]["cost"]
            upgrade_three_text = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["3"]["{}".format(self.tower_to_upgrade.upgrade_three_counter)]["text"]

            hendrick_das_ding_ist_dirty_af = 3 if self.tower_to_upgrade.upgrade_one_maxed else self.tower_to_upgrade.upgrade_one_counter
            for i in range(0, hendrick_das_ding_ist_dirty_af):
                pygame.draw.rect(self.screen, (0,255,0),(self.COL_SIZE * 2 + (i + 1) * 20, self.ROW_SIZE * 4 + self.header_size, 10, 10))

            hendrick_das_ding_ist_dirty_af_two = 3 if self.tower_to_upgrade.upgrade_two_maxed else self.tower_to_upgrade.upgrade_two_counter
            for i in range(0, hendrick_das_ding_ist_dirty_af_two):
                pygame.draw.rect(self.screen, (0, 255, 0),(self.COL_SIZE * 2 + (i + 1) * 20, self.ROW_SIZE * 6 + self.header_size, 10, 10))

            hendrick_das_ding_ist_dirty_af_three = 3 if self.tower_to_upgrade.upgrade_three_maxed else self.tower_to_upgrade.upgrade_three_counter
            for i in range(0, hendrick_das_ding_ist_dirty_af_three):
                pygame.draw.rect(self.screen, (0, 255, 0),(self.COL_SIZE * 2 + (i + 1) * 20, self.ROW_SIZE * 8 + self.header_size, 10, 10))

            if self.tower_to_upgrade.upgrade_one_maxed:
                upgrade_one_cost = "-"
                upgrade_one_text = "Max"

            if self.tower_to_upgrade.upgrade_two_maxed:
                upgrade_two_cost = "-"
                upgrade_two_text = "Max"

            if self.tower_to_upgrade.upgrade_three_maxed:
                upgrade_three_cost = "-"
                upgrade_three_text = "Max"

            if self.tower_to_upgrade.upgrade_one_counter >= 1 and self.tower_to_upgrade.upgrade_two_counter >= 1:
                upgrade_three_cost = "-"
                upgrade_three_text = "N.A."
                self.tower_to_upgrade.can_upgrade_three = False

            if self.tower_to_upgrade.upgrade_one_counter >= 1 and self.tower_to_upgrade.upgrade_three_counter >= 1:
                upgrade_two_cost = "-"
                upgrade_two_text = "N.A."
                self.tower_to_upgrade.can_upgrade_two = False

            if self.tower_to_upgrade.upgrade_two_counter >= 1 and self.tower_to_upgrade.upgrade_three_counter >= 1:
                upgrade_one_cost = "-"
                upgrade_one_text = "N.A."
                self.tower_to_upgrade.can_upgrade_one = False

            if (self.tower_to_upgrade.upgrade_one_maxed or self.tower_to_upgrade.upgrade_two_maxed) and self.tower_to_upgrade.upgrade_three_counter == 2:
                upgrade_three_cost = "-"
                upgrade_three_text = "Capped"
                self.tower_to_upgrade.can_upgrade_three = False

            if (self.tower_to_upgrade.upgrade_one_maxed or self.tower_to_upgrade.upgrade_three_maxed) and self.tower_to_upgrade.upgrade_two_counter == 2:
                upgrade_two_cost = "-"
                upgrade_two_text = "Capped"
                self.tower_to_upgrade.can_upgrade_two = False

            if (self.tower_to_upgrade.upgrade_three_maxed or self.tower_to_upgrade.upgrade_two_maxed) and self.tower_to_upgrade.upgrade_one_counter == 2:
                upgrade_one_cost = "-"
                upgrade_one_text = "Capped"
                self.tower_to_upgrade.can_upgrade_one = False

            self.tower_to_upgrade.display_upgrades()
            self.display_single_upgrade(self.upgrade_button_one, upgrade_one_cost, upgrade_one_text)
            self.display_single_upgrade(self.upgrade_button_two, upgrade_two_cost, upgrade_two_text)
            self.display_single_upgrade(self.upgrade_button_three, upgrade_three_cost, upgrade_three_text)

            self.screen.blit(self.font.render("Value: {}".format(self.tower_to_upgrade.value),True,(0,0,0)), (self.COL_SIZE, self.ROW_SIZE * 13 + self.header_size))
            self.sell_tower_btn.draw_from_color(self.screen)
            self.sell_tower_btn.check_collision(pygame.mouse.get_pos(), self.mouse_clicked)

        if self.tower_to_upgrade is not None:
            if self.tower_to_upgrade.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once and self.upgrades_open:
                self.upgrades_open = False
                self.tower_to_upgrade = None
                self.mouse_clicked_once = False

        for tower in self.tower_list:
            if tower.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once:
                self.upgrades_open = True
                self.inventory_open = False
                self.tower_to_upgrade = tower
                self.mouse_clicked_once = False
        for line in self.arr:
            for tile in line:
                if tile.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked_once and not self.upgrade_overlay.get_rect().collidepoint(pygame.mouse.get_pos()):
                    self.upgrades_open = False

    def draw_bullets(self):
        for tower in self.tower_list:
            for bullet in tower.bullet_list:
                bullet.bullet_rect = pygame.draw.circle(self.screen, (255, 0, 0), (bullet.my_x*self.COL_SIZE, (bullet.my_y*self.ROW_SIZE)+self.header_size), bullet.size)

                ang = math.atan2(bullet.y_vec, bullet.x_vec)
                bullet.my_x += math.cos(ang) * bullet.velocity * self.delta_time
                bullet.my_y += math.sin(ang) * bullet.velocity * self.delta_time

                x_d = tower.x * self.COL_SIZE + self.COL_SIZE * 0.5 - bullet.my_x * self.COL_SIZE
                y_d = tower.y * self.ROW_SIZE + self.ROW_SIZE * 0.5  - bullet.my_y * self.ROW_SIZE
                bullet.distance = math.sqrt(math.pow(x_d, 2) + math.pow(y_d, 2))

                for line in self.arr:
                    for tile in line:
                        if tile.field_type == -1 and tile.rect.colliderect(bullet.bullet_rect):
                            if bullet in tower.bullet_list: tower.bullet_list.remove(bullet)

                if bullet.distance >= tower.radius:
                    if bullet in tower.bullet_list: tower.bullet_list.remove(bullet)

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

        if self.cost_dict["circle"] <= self.player_money and self.inventory_open and self.tower_counter < 1:
            self.move_pink_tower = self.check_clicked_tower(self.pink_tower, self.move_pink_tower)
        self.click_and_drag_tower(self.move_pink_tower, self.pink_color, "circle")

        if self.cost_dict["basic"] <= self.player_money and self.inventory_open and self.tower_counter < 1:
            self.move_gray_tower = self.check_clicked_tower(self.gray_tower, self.move_gray_tower)
        self.click_and_drag_tower(self.move_gray_tower, self.gray_color, "basic")

        if self.cost_dict["arc"] <= self.player_money and self.inventory_open and self.tower_counter < 1:
            self.move_orange_tower = self.check_clicked_tower(self.orange_tower, self.move_orange_tower)
        self.click_and_drag_tower(self.move_orange_tower, self.orange_color, "arc")

        if not self.mouse_clicked or self.right_mouse_clicked:
            self.reset_moving_tower()

    def check_clicked_tower(self, tower_rect, moving_bool):
        if tower_rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_clicked:
            self.tower_counter = 1
            moving_bool = True
        return moving_bool

    def click_and_drag_tower(self, moving_bool, color, tower_type):
        if moving_bool:
            tower_rect = pygame.draw.circle(self.screen, color, pygame.mouse.get_pos(),self.COL_SIZE // 2)
            x, y = pygame.mouse.get_pos()
            x = x / self.COL_SIZE - 0.5
            y = y / self.ROW_SIZE - 1.5
            match tower_type:
                case "basic":
                    self.draw_tower_radius(BasicTower(x , y, tower_type, self.COL_SIZE, self.ROW_SIZE, color), self.tower_drag_radius_color)
                case "circle":
                    self.draw_tower_radius(CircleTower(x, y, tower_type, self.COL_SIZE, self.ROW_SIZE, color), self.tower_drag_radius_color)
                case "arc":
                    self.draw_tower_radius(ArcTower(x, y, tower_type, self.COL_SIZE, self.ROW_SIZE, color), self.tower_drag_radius_color)

            if tower_rect.colliderect(self.tower_overlay.get_rect()) and not self.mouse_clicked and self.tower_counter > 0 and self.inventory_open:
                self.reset_moving_tower()
            can_place_tower = True
            for line in self.arr:
                for tile in line:
                    if self.tower_list:
                        for tower in self.tower_list:
                            if (not tile.field_type == 0 and tower_rect.colliderect(tile.rect)) or tower_rect.colliderect(tower.rect):
                                can_place_tower = False
                                self.tower_drag_radius_color = (250, 20, 20, 50)
                            elif tile.field_type == 0 and tower_rect.colliderect(tile.rect):
                                self.tower_drag_radius_color = (50, 50, 50, 50)
                    if not tile.field_type == 0 and tower_rect.colliderect(tile.rect):
                        self.tower_drag_radius_color = (250, 20, 20, 50)
                        can_place_tower = False
                    elif tile.field_type == 0 and tower_rect.colliderect(tile.rect):
                        self.tower_drag_radius_color = (50, 50, 50, 50)

            if can_place_tower and not self.mouse_clicked and self.tower_counter > 0:
                match tower_type:
                    case "basic":
                        self.tower_list.append(
                            BasicTower(x, y, tower_type, self.COL_SIZE, self.ROW_SIZE, color))
                    case "circle":
                        self.tower_list.append(
                            CircleTower(x, y, tower_type, self.COL_SIZE, self.ROW_SIZE, color))
                    case "arc":
                        self.tower_list.append(
                            ArcTower(x, y, tower_type, self.COL_SIZE, self.ROW_SIZE, color))
                self.player_money -= self.cost_dict[tower_type]
                self.tower_counter -= 1

    def reset_moving_tower(self):
        self.move_pink_tower = False
        self.move_gray_tower = False
        self.move_orange_tower = False
        self.tower_counter = 0

    def towers_fire(self):
        for tower in self.tower_list:
            for enemy in self.enemy_list:
                x_d = tower.x * self.COL_SIZE - enemy.x * self.COL_SIZE
                y_d = tower.y * self.ROW_SIZE - enemy.y * self.ROW_SIZE
                distance = math.sqrt(math.pow(x_d,2) + math.pow(y_d,2))
                if distance < tower.radius:
                    tower.fire(enemy)

    def check_bullet_enemy_collision(self):
        for tower in self.tower_list:
            for bullet in tower.bullet_list:
                for enemy in self.enemy_list:
                    if enemy.enemy_rect.colliderect(bullet.bullet_rect):
                        if not enemy.last_hit_by == bullet:
                            enemy.current_health -= bullet.damage
                            enemy.last_hit_by = bullet
                            bullet.pierce -= 1
                            if bullet.pierce <= 0:
                                if bullet in tower.bullet_list: tower.bullet_list.remove(bullet)
                    if enemy.current_health <= 0:
                        if enemy in self.enemy_list:
                            self.player_money += enemy.kill_reward
                            self.enemy_list.remove(enemy)

    def check_player_health(self):
        if self.player_health <= 0:
            self.game_running = False
            self.running = False

    def display_single_upgrade(self, button, cost, text):
        upgrade_rect = button.draw_from_color(self.screen)
        button.check_collision(pygame.mouse.get_pos(), self.mouse_clicked_once)

        upgrade_box_text = self.font.render("{}$".format(cost), True, (255, 255, 255))
        text_rect = upgrade_box_text.get_rect(
            center=(upgrade_rect.width / 2 + upgrade_rect.x, upgrade_rect.height / 2 + upgrade_rect.y))
        self.screen.blit(upgrade_box_text, text_rect)

        upgrade_text = self.font.render("{}".format(text), True, (0, 0, 0))
        text_rect = upgrade_box_text.get_rect(
            center=(upgrade_rect.x * 2.6, upgrade_rect.height / 2 + upgrade_rect.y))
        self.screen.blit(upgrade_text, text_rect)

    def buy_upgrade_one(self):
        cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["1"][
            "{}".format(self.tower_to_upgrade.upgrade_one_counter)]["cost"]
        if cost <= self.player_money and self.upgrades_open and not self.tower_to_upgrade.upgrade_one_maxed and self.tower_to_upgrade.can_upgrade_one:
            self.tower_to_upgrade.upgrade_one()
            self.player_money -= cost

    def buy_upgrade_two(self):
        cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["2"][
            "{}".format(self.tower_to_upgrade.upgrade_two_counter)]["cost"]
        if cost <= self.player_money and self.upgrades_open and not self.tower_to_upgrade.upgrade_two_maxed and self.tower_to_upgrade.can_upgrade_two:
            self.tower_to_upgrade.upgrade_two()
            self.player_money -= cost

    def buy_upgrade_three(self):
        cost = self.tower_upgrade_data["{}".format(self.tower_to_upgrade.tower_type)]["3"][
            "{}".format(self.tower_to_upgrade.upgrade_three_counter)]["cost"]
        if cost <= self.player_money and self.upgrades_open and not self.tower_to_upgrade.upgrade_three_maxed and self.tower_to_upgrade.can_upgrade_three:
            self.tower_to_upgrade.upgrade_three()
            self.player_money -= cost

    def draw_tower_radius(self, tower, radius_color):
        circle_surface = pygame.Surface((tower.radius * 2, tower.radius * 2),pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, radius_color,(tower.radius, tower.radius), tower.radius)

        self.screen.blit(circle_surface, ((tower.x * self.COL_SIZE + (self.COL_SIZE * 0.5) - tower.radius),
                                          (tower.y * self.ROW_SIZE + (self.ROW_SIZE * 0.5) - tower.radius) + self.header_size))
    # </editor-fold>

    # <editor-fold desc="buttons">
    def overlay_button(self):
        if not self.inventory_open and not self.upgrades_open:
            self.inventory_open = True
            self.upgrades_open = False
        elif self.inventory_open and not self.upgrades_open:
            self.inventory_open = False
            self.upgrades_open = False
        elif self.upgrades_open:
            self.upgrades_open = False

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
        self.main_menu = False
        self.game_running = False
        self.pause_menu = False
        self.running = False
        self.map_picker = False

    def skip_button(self):
        self.wave_timer.second_counter = 0

    def play_game(self ):
        self.main_menu = False
        self.map_picker = True

    def sell_tower_button(self):
        for tower in self.tower_list:
            if tower == self.tower_to_upgrade:
                self.player_money += tower.value
                self.tower_list.remove(tower)
        for tower_point in self.tower_point_list:
            if tower_point["x"] == self.tower_to_upgrade.x and tower_point["y"] == self.tower_to_upgrade.y:
                tower_point["has_tower"] = False

        self.tower_to_upgrade = None
        self.upgrades_open = False

    def back_to_main_menu(self):
        self.map_picker = False
        self.main_menu = True

    def select_map(self, map_num):
        self.map_selection = map_num

    def select_and_play_map(self):
        if self.map_selection is not None:
            self.arr = read_map(self.map_dict[str(self.map_selection)]["file"])
            for i in range(len(self.arr) * len(self.arr[0])):
                for line in self.arr:
                    for tile in line:
                        if tile.field_type == (i+1):
                            self.path.append(tile)

            self.tower_point_list = self.get_tower_points()
            self.start_point, self.end_point = self.get_start_and_endpoint()
            self.END = int(len(self.path))
            self.map_picker = False
            self.game_running = True
    # </editor-fold>


pygame.init()
game = GAME()
game.main_loop()
pygame.quit()