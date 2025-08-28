import pygame

class GAME:
    def __init__(self):
        self.screen = pygame.display.set_mode((1400, 700))
        self.running = True

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()

pygame.init()
game = GAME()
game.game_loop()