

import pygame
from code.utils import resource_path

class Background:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.layers = []
        
        self.scroll_speed = 1

    def add_layer(self, image_path, speed_multiplier):
        """ Adiciona uma nova camada de fundo à lista. """
        try:
            caminho_completo = resource_path(f'asset/{image_path}')
            image = pygame.image.load(caminho_completo).convert_alpha()
            original_width, original_height = image.get_size()
            new_height = self.window_height
            new_width = int(original_width * (new_height / original_height))
            image = pygame.transform.scale(image, (new_width, new_height))
            
            # Guardo a camada e suas propriedades em um dicionário
            layer = {
                'image': image,
                'speed': self.scroll_speed * speed_multiplier,
                'x_pos': 0,
                'width': image.get_width()
            }
            self.layers.append(layer)
        except pygame.error:
            # Se a imagem não for encontrada, exibo um aviso no terminal
            print(f"AVISO: Imagem de camada de fundo não encontrada em {image_path}")

    def update(self):
        """ Atualiza a posição de cada camada para criar o movimento. """
        for layer in self.layers:
            # Movimento a camada para a esquerda de acordo com sua velocidade
            layer['x_pos'] -= layer['speed']
            # Se a imagem saiu completamente da tela, reseto sua posição
            # Isso cria o efeito de "esteira rolante" infinita.
            if layer['x_pos'] <= -layer['width']:
                layer['x_pos'] = 0

    def draw(self, window):
        """ Desenha todas as camadas na tela. """
        for layer in self.layers:
            # Desenho a imagem na sua posição atual
            window.blit(layer['image'], (layer['x_pos'], 0))
            # Desenho a mesma imagem logo em seguida para preencher o espaço vazio
            window.blit(layer['image'], (layer['x_pos'] + layer['width'], 0))