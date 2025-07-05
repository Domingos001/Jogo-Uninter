# Arquivo: code/Enemy2.py
# Define a classe para o Inimigo tipo 2 (mais rápido que o primeiro).

import pygame
from code.utils import resource_path

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            # Carrega a imagem do segundo tipo de inimigo
            self.image = pygame.image.load(resource_path('asset/inimigo 2.png')).convert_alpha()
        except pygame.error:
            # Cria um quadrado roxo como fallback
            self.image = pygame.Surface((40, 40))
            self.image.fill((128, 0, 128))
            print("AVISO: Imagem do inimigo 'inimigo 2.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.points = 35

    def update(self):
        """ Atualiza a posição do inimigo a cada quadro. """
        self.rect.x -= self.speed
        
        if self.rect.right < 0:
            self.kill()