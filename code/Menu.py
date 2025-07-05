import pygame
from pygame import Surface, Rect # <-- CORREÇÃO: Removi 'Font' desta linha
from pygame.font import SysFont # <-- Usaremos SysFont para criar as fontes
from code.const import WIN_WIDTH, C_WHITE, MENU_OPTION, C_YELLOW
from code.utils import resource_path

class Menu:
    def __init__(self, window):
        self.window = window
        # Carrega a imagem de fundo do menu
        self.surf = pygame.image.load(resource_path('asset/menu.png')).convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        
        # Guarda a opção selecionada no menu
        self.selected_option = 0
        
        # Cria as fontes que serão usadas para o texto
        self.title_font = SysFont("Lucida Sans Typewriter", 70)
        self.option_font = SysFont("Lucida Sans Typewriter", 20)
        
        # Define o caminho da música do menu
        self.music_path = resource_path('asset/fase 1 musica.mp3')

    def draw(self):
        """ Desenha todos os elementos do menu na tela. """
        self.window.blit(self.surf, self.rect)
        
        # Desenha o título do jogo
        self.menu_text(self.title_font, "Bubble", C_WHITE, (WIN_WIDTH / 2, 70))
        self.menu_text(self.title_font, "Beam", C_WHITE, (WIN_WIDTH / 2, 120))

        # Desenha as opções do menu, destacando a selecionada
        for i, option in enumerate(MENU_OPTION):
            color = C_YELLOW if i == self.selected_option else C_WHITE
            self.menu_text(self.option_font, option, color, (WIN_WIDTH / 2, 200 + 25 * i))

    def handle_events(self, event_list):
        """ Verifica os inputs do jogador para navegar no menu. """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(MENU_OPTION)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(MENU_OPTION)
                elif event.key == pygame.K_RETURN:
                    # Retorna a string da opção escolhida quando o jogador aperta Enter
                    return MENU_OPTION[self.selected_option]
        return None

    def menu_text(self, font, text: str, text_color: tuple, text_center_pos: tuple):
        """ Uma função para desenhar texto centralizado na tela. """
        # CORREÇÃO: Removi a anotação de tipo 'Font' que causava o erro
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)