import pygame
from code.const import WIN_WIDTH, C_WHITE, C_YELLOW, C_BLACK

class NameInputScreen:
    def __init__(self, window):
        self.window = window
        self.title_font = pygame.font.Font(None, 48)
        self.input_font = pygame.font.Font(None, 40)
        self.current_input = ""
        self.music_path = 'asset/menu musica.flac'
        
        self.background_image = pygame.image.load('asset/menu.png').convert()
        
        self.asking_for_player = 1
        self.player1_name = ""

    def start(self, game_mode):
        self.game_mode = game_mode
        self.asking_for_player = 1
        self.current_input = ""
        self.player1_name = ""

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.current_input) > 0:
                    if self.game_mode in ['1P', '2P_COMP'] or self.asking_for_player == 2:
                        if self.asking_for_player == 1: self.player1_name = self.current_input
                        player2_name = self.current_input if self.asking_for_player == 2 else ""
                        return {'p1_name': self.player1_name, 'p2_name': player2_name}
                    else: # Modo 2P_COOP
                        self.player1_name = self.current_input
                        self.current_input = ""
                        self.asking_for_player = 2
                elif event.key == pygame.K_BACKSPACE:
                    self.current_input = self.current_input[:-1]
                else:
                    # Limita o nome a 5 caracteres.
                    if len(self.current_input) < 5:
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