import pygame
from code.Projectile import Projectile
from code.const import WIN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('asset/prota.png').convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((30, 50))
            self.image.fill((255, 0, 0))
            print("AVISO: Imagem do jogador 'prota.png' não encontrada.")

        self.rect = self.image.get_rect(center=(100, 240))
        self.speed = 5
        self.shoot_cooldown = 300 # Milissegundos entre os tiros
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()

        # CORREÇÃO da sintaxe do movimento
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = now
            # O tiro sai da direita do jogador
            projectile = Projectile(self.rect.right, self.rect.centery)
            return projectile
        return None