# Arquivo: code/Enemy3.py
# Define a classe para o Inimigo tipo 3 (com movimento de onda).

import pygame
import math
from code.utils import resource_path

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load(resource_path('asset/inimigo 3.png')).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 255))
            print("AVISO: Imagem do inimigo 'inimigo 3.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        
        # Atributos específicos deste inimigo
        self.speed_x = 3 # Velocidade horizontal
        self.points = 40
        
        # Variáveis para controlar o movimento de onda (senoide)
        self.base_y = y
        self.angle = 0
        self.amplitude = 40
        self.frequency = 0.05

    def update(self):
        """ Atualiza a posição do inimigo com movimento de onda. """
        self.rect.x -= self.speed_x
        
        self.angle += self.frequency
        self.rect.centery = self.base_y + math.sin(self.angle) * self.amplitude


        if self.rect.right < 0:
            self.kill()