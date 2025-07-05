import pygame
from code.const import WIN_WIDTH, C_WHITE, C_YELLOW, C_BLACK
from code.utils import resource_path

class NameInputScreen:
    def __init__(self, window):
        self.window = window
        self.title_font = pygame.font.Font(None, 48)
        self.input_font = pygame.font.Font(None, 40)
        self.current_input = ""
        self.music_path = resource_path('asset/menu musica.flac')
        
        try:
            self.background_image = pygame.image.load(resource_path('asset/menu.png')).convert()
        except pygame.error:
            self.background_image = None
            print("AVISO: Imagem de fundo da tela de nome não encontrada.")
        
        self.asking_for_player = 1
        self.player1_name = ""
        self.game_mode = '1P'

    def start(self, game_mode):
        """ Reinicia a tela para um novo input de nome. """
        self.game_mode = game_mode
        self.asking_for_player = 1
        self.current_input = ""
        self.player1_name = ""

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.current_input) > 0:
                    
                    # --- CORREÇÃO DA LÓGICA AQUI ---
                    # Este bloco finaliza a entrada de nomes se:
                    # 1. O modo for de 1 jogador.
                    # 2. Ou se já estivermos pedindo o nome do segundo jogador.
                    if self.game_mode == '1P' or self.asking_for_player == 2:
                        # Se ainda estamos no P1 (caso de 1P), guarda o nome.
                        if self.asking_for_player == 1:
                            self.player1_name = self.current_input
                        
                        # Define o nome do P2 (pode ser vazio se for modo 1P).
                        player2_name = self.current_input if self.asking_for_player == 2 else ""
                        
                        # Retorna os nomes e finaliza esta tela.
                        return {'p1_name': self.player1_name, 'p2_name': player2_name}
                    
                    else: # Se for modo 2P (Coop ou Comp) e acabamos de pegar o nome do P1.
                        # Guarda o nome do P1 e prepara para pedir o nome do P2.
                        self.player1_name = self.current_input
                        self.current_input = ""
                        self.asking_for_player = 2

                elif event.key == pygame.K_BACKSPACE:
                    self.current_input = self.current_input[:-1]
                else:
                    if len(self.current_input) < 5:
                        # Adiciona o caractere digitado ao nome atual.
                        self.current_input += event.unicode
        return None

    def draw(self):
        self.window.blit(self.background_image, (0,0))
        
        prompt_text = f"Digite o nome do Jogador {self.asking_for_player}:"
        title_surf = self.title_font.render(prompt_text, True, C_YELLOW)
        title_rect = title_surf.get_rect(center=(WIN_WIDTH / 2, 120))
        self.window.blit(title_surf, title_rect)

        input_text_surf = self.input_font.render(self.current_input, True, C_WHITE)
        input_text_rect = input_text_surf.get_rect(center=(WIN_WIDTH / 2, 200))
        self.window.blit(input_text_surf, input_text_rect)

        info_surf = self.input_font.render("Pressione ENTER para continuar", True, C_WHITE)
        info_rect = info_surf.get_rect(center=(WIN_WIDTH / 2, 300))
        self.window.blit(info_surf, info_rect)