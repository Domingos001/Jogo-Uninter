
import pygame
from code.Projectile import Projectile
from code.const import WIN_HEIGHT
from code.utils import resource_path

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try:
            self.image = pygame.image.load(resource_path('asset/prota.png')).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((30, 50))
            self.image.fill((255, 0, 0))
            print("AVISO: Imagem do jogador 'prota.png' não encontrada.")

        # Pego o retângulo da imagem e defino sua posição inicial
        self.rect = self.image.get_rect(center=(100, 200))
        
        # Defino as propriedades do jogador
        self.speed = 5
        self.shoot_cooldown = 300 # Intervalo de 300ms entre os tiros
        self.last_shot_time = 0
        self.lives = 3
        self.is_alive = True

    def update(self):
        """ Atualiza a posição do jogador a cada quadro, baseado no input. """
        # Se o jogador não estiver vivo, não faço nada
        if not self.is_alive:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

    def shoot(self):
        """ Cria e retorna um novo projétil se o cooldown permitir. """
        if not self.is_alive:
            return None
            
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = now
            # Crio o projétil, passando a identificação 'P1' para saber quem atirou
            return Projectile(self.rect.right, self.rect.centery, 'P1')
        return None

    def get_hit(self):
        """ Chamado quando o jogador é atingido por um inimigo. """
        self.lives -= 1
        print(f"Jogador 1 foi atingido! Vidas restantes: {self.lives}")
        if self.lives <= 0:
            self.is_alive = False
            self.kill() # Remove o sprite do jogador dos grupos