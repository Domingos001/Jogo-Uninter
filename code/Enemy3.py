import pygame
import math

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            
            self.image = pygame.image.load('asset/inimigo 3.png').convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 255))
            print("AVISO: Imagem do inimigo 'inimigo3.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 3
        self.base_y = y
        self.angle = 0
        self.amplitude = 40
        self.frequency = 0.05
        self.points = 40

    def update(self):
        self.rect.x -= self.speed_x
        self.angle += self.frequency
        self.rect.centery = self.base_y + math.sin(self.angle) * self.amplitude
        if self.rect.right < 0:
            self.kill()