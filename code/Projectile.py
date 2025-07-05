import pygame
from code.const import WIN_WIDTH

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Carrega a imagem original primeiro
            original_image = pygame.image.load('asset/bolha.png').convert_alpha()
            
            # Define o novo tamanho desejado para a bolha
            new_width = 15
            new_height = 15
            
            # Redimensiona a imagem para o novo tamanho
            self.image = pygame.transform.scale(original_image, (new_width, new_height))
            
        except pygame.error:
            # Se a imagem não for encontrada, cria um substituto
            self.image = pygame.Surface((10, 10))
            self.image.fill((0, 0, 255))
            print("AVISO: Imagem 'bolha.png' não encontrada.")

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        # Move o projétil para a direita
        self.rect.x += self.speed
        # Remove o projétil se ele sair da tela
        if self.rect.left > WIN_WIDTH:
            self.kill()