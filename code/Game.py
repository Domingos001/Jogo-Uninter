import pygame
from code.const import WIN_HEIGHT, WIN_WIDTH

from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self, ):
        menu = Menu(self.window)
        menu.run()