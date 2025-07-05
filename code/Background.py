import pygame

class Background:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height # Guarda a altura
        self.layers = []
        self.scroll_speed = 1

    def add_layer(self, image_path, speed_multiplier):
        """ Adiciona uma nova camada de fundo. """
        try:
            caminho_completo = f'asset/{image_path}'
            image = pygame.image.load(caminho_completo).convert_alpha()
            
            original_width, original_height = image.get_size()
            
            
            new_height = self.window_height
            new_width = int(original_width * (new_height / original_height))
            image = pygame.transform.scale(image, (new_width, new_height))
            
            layer = {
                'image': image,
                'speed': self.scroll_speed * speed_multiplier,
                'x_pos': 0,
                'width': image.get_width()
            }
            self.layers.append(layer)
        except pygame.error:
            print(f"AVISO: Imagem de camada de fundo não encontrada em {image_path}")

    def update(self):
        """ Atualiza a posição de cada camada para criar o movimento. """
        for layer in self.layers:
            layer['x_pos'] -= layer['speed']
            if layer['x_pos'] <= -layer['width']:
                layer['x_pos'] = 0

    def draw(self, window):
        """ Desenha todas as camadas na tela. """
        for layer in self.layers:
            window.blit(layer['image'], (layer['x_pos'], 0))
            window.blit(layer['image'], (layer['x_pos'] + layer['width'], 0))