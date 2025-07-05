import pygame
from code.const import WIN_WIDTH, C_WHITE, C_YELLOW, C_BLACK

class ScoreScreen:
    def __init__(self, window, high_scores):
        self.window = window
        self.high_scores = high_scores
        self.header_font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)
        self.music_path = 'asset/menu musica.flac'
        
        try:
            self.background_image = pygame.image.load('asset/fundo 2 1 camada.png').convert()
        except pygame.error:
            self.background_image = None
            print("AVISO: Imagem de fundo da tela de score não encontrada.")

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return "MENU"
        return None

    def draw(self):
        if self.background_image:
            self.window.blit(self.background_image, (0,0))
        

        # 1. Título Geral
        title_surf = self.header_font.render("Melhores Pontuações", True, C_YELLOW)
        title_rect = title_surf.get_rect(center=(WIN_WIDTH / 2, 60))
        self.window.blit(title_surf, title_rect)

        # 2. Cabeçalhos das Colunas
        header_y = 120
        col_name_x = 120
        col_score_x = WIN_WIDTH / 2
        col_date_x = WIN_WIDTH - 120

        # Cabeçalho "Nome"
        name_header_surf = self.score_font.render("Nome", True, C_YELLOW)
        name_header_rect = name_header_surf.get_rect(center=(col_name_x, header_y))
        self.window.blit(name_header_surf, name_header_rect)

        # Cabeçalho "Score"
        score_header_surf = self.score_font.render("Score", True, C_YELLOW)
        score_header_rect = score_header_surf.get_rect(center=(col_score_x, header_y))
        self.window.blit(score_header_surf, score_header_rect)

        # Cabeçalho "Data"
        date_header_surf = self.score_font.render("Data", True, C_YELLOW)
        date_header_rect = date_header_surf.get_rect(center=(col_date_x, header_y))
        self.window.blit(date_header_surf, date_header_rect)

        # 3. Lista de Scores
        if not self.high_scores:
            info_surf = self.score_font.render("Nenhum score registrado", True, C_WHITE)
            info_rect = info_surf.get_rect(center=(WIN_WIDTH / 2, 220))
            self.window.blit(info_surf, info_rect)
        else:
            for i, score_entry in enumerate(self.high_scores):
                # Posição Y para cada linha da tabela
                row_y = 170 + i * 40
                
                # Coluna do Nome do jogador
                name_surf = self.score_font.render(f"{i+1}. {score_entry['name']}", True, C_WHITE)
                name_rect = name_surf.get_rect(midleft=(50, row_y))
                self.window.blit(name_surf, name_rect)

                # Coluna da Pontuação
                score_surf = self.score_font.render(str(score_entry['score']), True, C_WHITE)
                score_rect = score_surf.get_rect(center=(col_score_x, row_y))
                self.window.blit(score_surf, score_rect)

                # Coluna da Data
                date_surf = self.score_font.render(score_entry['date'], True, C_WHITE)
                date_rect = date_surf.get_rect(center=(col_date_x, row_y))
                self.window.blit(date_surf, date_rect)

        
        info_surf = self.info_font.render("Pressione qualquer tecla para voltar", True, C_WHITE)
        info_rect = info_surf.get_rect(center=(WIN_WIDTH / 2, 400))
        self.window.blit(info_surf, info_rect)