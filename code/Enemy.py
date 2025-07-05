import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('asset/inimigo 1.png').convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))
            print("AVISO: Imagem do inimigo 'inimigo 1.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()