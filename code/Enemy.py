import pygame
from code.utils import resource_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load(resource_path('asset/inimigo 1.png')).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))
            print("AVISO: Imagem do inimigo 'inimigo 1.png' não encontrada.")

        # Pego o retângulo da imagem e defino sua posição inicial
        self.rect = self.image.get_rect(center=(x, y))
        
        # Defino os atributos deste inimigo
        self.speed = 2
        self.points = 20

    def update(self):
        """ Atualiza a posição do inimigo a cada quadro. """
        # Movimento o inimigo para a esquerda
        self.rect.x -= self.speed
        
        # Se o inimigo sair completamente da tela, eu o removo para otimizar o jogo
        if self.rect.right < 0:
            self.kill()