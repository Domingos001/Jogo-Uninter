import pygame
from code.const import WIN_WIDTH

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, owner_id): # <-- Recebe o ID do dono
        super().__init__()
        self.owner_id = owner_id # <-- Guarda quem atirou ('P1' ou 'P2')
        try:
            original_image = pygame.image.load('asset/bolha.png').convert_alpha()
            new_width = 15
            new_height = 15
            self.image = pygame.transform.scale(original_image, (new_width, new_height))
        except pygame.error:
            self.image = pygame.Surface((10, 10)); self.image.fill((0, 0, 255))
            print("AVISO: Imagem 'bolha.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH:
            self.kill()