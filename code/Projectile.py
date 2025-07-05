# Arquivo: code/Projectile.py
# Define a classe para os projéteis disparados pelos jogadores.

import pygame
from code.const import WIN_WIDTH
from code.utils import resource_path

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, owner_id):
        # Chamo o construtor da classe pai (Sprite)
        super().__init__()
        
        # Guardo a identificação de quem atirou ('P1' ou 'P2')
        # Isso é crucial para o modo competitivo
        self.owner_id = owner_id
        
        try:
            # Utilizo a função resource_path para encontrar a imagem da bolha
            original_image = pygame.image.load(resource_path('asset/bolha.png')).convert_alpha()
            # Redimensiono a imagem para um tamanho adequado
            new_width = 15
            new_height = 15
            self.image = pygame.transform.scale(original_image, (new_width, new_height))
        except pygame.error:
            # Se a imagem não for encontrada, crio uma superfície azul como fallback
            self.image = pygame.Surface((10, 10))
            self.image.fill((0, 0, 255))
            print("AVISO: Imagem 'bolha.png' não encontrada.")

        # Pego o retângulo da imagem e defino sua posição inicial
        self.rect = self.image.get_rect(center=(x, y))
        
        # Defino a velocidade do projétil
        self.speed = 10

    def update(self):
        """ Atualiza a posição do projétil a cada quadro. """
        # Movimento o projétil para a direita
        self.rect.x += self.speed
        
        # Se o projétil sair da tela pela direita, eu o removo para não consumir memória
        if self.rect.left > WIN_WIDTH:
            self.kill()