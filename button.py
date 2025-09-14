import pygame

class BUTTON:
    def __init__(self, start_x, start_y, width, height, code, color_default = None, color_hover = None, img = None, img_list = None, text = None, font = None, text_color = None):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.code = code
        self.color_default = color_default
        self.color_hover = color_hover
        if img is not None:
            self.img = img
            self.img = pygame.transform.scale(self.img, (self.width, self.height))
        else:
            self.img = None
        self.img_list = img_list
        self.text = text
        self.font = font
        self.text_color = text_color
        self.rect = pygame.Rect(self.start_x, self.start_y, self.width, self.height)
        self.hovered = False
        self.clicked = False

    def draw_from_color(self,screen):
        if not self.hovered:
            rect = pygame.draw.rect(screen, self.color_default, self.rect)
        else:
            rect = pygame.draw.rect(screen, self.color_hover, self.rect)

        if self.text and self.font and self.text_color:
            centered_text = self.font.render(self.text, True, self.text_color)
            text_rect = centered_text.get_rect(center=(self.width/2 + self.start_x, self.height/2 + self.start_y))
            screen.blit(centered_text, text_rect)

        return rect

    def draw_from_image(self, screen):
        if not self.hovered:
            self.img.set_alpha(255)
        else:
            self.img.set_alpha(200)
            pygame.draw.rect(screen, (0, 0, 0), (self.start_x - 2, self.start_y - 2, self.width + 4, self.height + 4))

        screen.blit(self.img, (self.start_x, self.start_y))

        if self.text and self.font and self.text_color:
            centered_text = self.font.render(self.text, True, self.text_color)
            text_rect = centered_text.get_rect(center=(self.width/2 + self.start_x, self.height/2 + self.start_y))
            screen.blit(centered_text, text_rect)

        rect = pygame.Rect(self.rect)

        return rect


    def check_collision(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            self.code()