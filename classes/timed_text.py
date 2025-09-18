import pygame

class TIMER:
    def __init__(self,font, color, seconds, x, y):
        self.font = font
        self.color = color
        self.seconds = seconds
        self.second_counter = seconds
        self.x = x
        self.y = y

        self.played_wave_timer = False
        self.last_updated_wave_timer = -1

    def count_down_text(self, screen):

        screen.blit(self.font.render("{s}".format(s = self.second_counter), True, self.color), (self.x, self.y))
        now = pygame.time.get_ticks()
        if now > self.last_updated_wave_timer + 1000:
            self.last_updated_wave_timer = now

            pygame.display.update()
            self.second_counter -=  1
        if self.second_counter <= 0:
            self.second_counter = self.seconds
            self.played_wave_timer = True
            self.last_updated_wave_timer = -1
