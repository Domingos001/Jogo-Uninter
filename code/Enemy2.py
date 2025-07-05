import pygame

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('asset/inimigo 2.png').convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((40, 40))
            self.image.fill((128, 0, 128))
            print("AVISO: Imagem do inimigo 'inimigo2.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.points = 35

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()