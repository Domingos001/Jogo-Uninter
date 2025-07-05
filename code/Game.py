import pygame
import sqlite3
from datetime import date
from code.Menu import Menu
from code.Level1 import Level1
from code.Level2 import Level2
from code.Level3 import Level3
from code.ScoreScreen import ScoreScreen
from code.NameInputScreen import NameInputScreen
from code.LevelCompetitive import LevelCompetitive
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.utils import resource_path

class Game:
    def __init__(self):
        pygame.init() # Inicializo o Pygame
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT)) # Crio a janela do jogo
        self.state = 'MENU' # Defino o estado inicial do jogo como o menu
        self.clock = pygame.time.Clock() # Crio um objeto para controlar a taxa de quadros

        self.player1_name = "" # Variável para armazenar o nome do jogador 1
        self.player2_name = "" # Variável para armazenar o nome do jogador 2
        self.current_score = 0 # Variável para armazenar a pontuação atual do jogador
        self.high_scores = [] # Lista para armazenar os melhores placares

        # Utilizo a função resource_path para obter o caminho correto do banco de dados
        self.db_path = resource_path('highscore.db')
        self.init_database() # Inicializo o banco de dados se ele não existir
        self.load_scores() # Carrego os melhores placares do banco de dados

        self.game_mode = '1P' # Defino o modo de jogo inicial como 1 jogador

    def init_database(self):
        conn = sqlite3.connect(self.db_path) # Conecto ao banco de dados
        cursor = conn.cursor() # Crio um cursor para executar comandos SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date_saved TEXT NOT NULL
            );
        ''') # Crio a tabela de high scores se ela não existir
        conn.commit() # Salvo as alterações no banco de dados
        conn.close() # Fecho a conexão com o banco de dados

    def load_scores(self):
        conn = sqlite3.connect(self.db_path) # Conecto ao banco de dados
        cursor = conn.cursor() # Crio um cursor
        cursor.execute("SELECT name, score, date_saved FROM high_scores ORDER BY score DESC LIMIT 5") # Seleciono os 5 melhores placares
        results = cursor.fetchall() # Busco todos os resultados
        conn.close() # Fecho a conexão
        self.high_scores = [{'name': name, 'score': score, 'date': date_saved} for name, score, date_saved in results] # Formato os resultados em uma lista de dicionários

    def save_scores(self):
        player_names = self.player1_name # Começo com o nome do jogador 1
        if self.game_mode == '2P_COOP' and self.player2_name:
            player_names += f" & {self.player2_name}" # Adiciono o nome do jogador 2 se estiver no modo cooperativo

        if player_names:
            today_date = date.today().strftime('%d/%m/%Y') # Obtenho a data de hoje
            conn = sqlite3.connect(self.db_path) # Conecto ao banco de dados
            cursor = conn.cursor() # Crio um cursor
            cursor.execute("INSERT INTO high_scores (name, score, date_saved) VALUES (?, ?, ?)",
                        (player_names, self.current_score, today_date)) # Insiro o novo score
            conn.commit() # Salvo as alterações
            conn.close() # Fecho a conexão
            self.load_scores() # Recarrego os scores para atualizar a lista

    def start_new_game(self):
        self.current_score = 0 # Reseto a pontuação atual
        return (Level1(self.window, self, self.game_mode),
                Level2(self.window, self, self.game_mode),
                Level3(self.window, self, self.game_mode),
                LevelCompetitive(self.window, self)) # Retorno as instâncias das fases

    def run(self):
        menu = Menu(self.window) # Crio a instância do menu
        name_input_screen = NameInputScreen(self.window) # Crio a instância da tela de entrada de nome
        score_screen = ScoreScreen(self.window, self.high_scores) # Crio a instância da tela de scores
        level1, level2, level3, level_comp = self.start_new_game() # Inicializo as fases
        
        current_music = None # Variável para controlar a música atual

        while True:
            events = pygame.event.get() # Obtenho a lista de eventos
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit() # Finalizo o Pygame
                    quit() # Finalizo o programa

            self.window.fill((0, 0, 0)) # Preencho a tela com preto

            if self.state == 'MENU':
                if current_music != menu.music_path:
                    pygame.mixer.music.load(menu.music_path); pygame.mixer.music.play(-1)
                    current_music = menu.music_path
                menu.draw() # Desenho o menu
                chosen_option = menu.handle_events(events) # Verifico se alguma opção foi escolhida
                if chosen_option:
                    if chosen_option == 'NEW GAME 1P':
                        self.game_mode = '1P'
                        name_input_screen.start(self.game_mode)
                        self.state = 'INPUT_NAME'
                    elif chosen_option == 'NEW GAME 2P - COOPERATIVE':
                        self.game_mode = '2P_COOP'
                        name_input_screen.start(self.game_mode)
                        self.state = 'INPUT_NAME'
                    elif chosen_option == 'NEW GAME 2P - COMPETITIVE':
                        self.game_mode = '2P_COMP'
                        name_input_screen.start(self.game_mode)
                        self.state = 'INPUT_NAME'
                    elif chosen_option == 'SCORE':
                        self.load_scores()
                        score_screen.high_scores = self.high_scores
                        self.state = 'SCORE_SCREEN'
                    elif chosen_option == 'EXIT':
                        break

            elif self.state == 'INPUT_NAME':
                if current_music != name_input_screen.music_path:
                    pygame.mixer.music.load(name_input_screen.music_path); pygame.mixer.music.play(-1)
                    current_music = name_input_screen.music_path
                name_input_screen.draw() # Desenho a tela de entrada de nome
                player_names = name_input_screen.handle_events(events) # Obtenho os nomes dos jogadores
                if player_names:
                    self.player1_name = player_names['p1_name']
                    self.player2_name = player_names['p2_name']
                    level1, level2, level3, level_comp = self.start_new_game()
                    if self.game_mode == '2P_COMP':
                        self.state = 'LEVEL_COMPETITIVE'
                    else:
                        self.state = 'LEVEL_1'

            elif self.state == 'LEVEL_COMPETITIVE':
                if current_music != level_comp.music_path:
                    pygame.mixer.music.load(level_comp.music_path); pygame.mixer.music.play(-1)
                    current_music = level_comp.music_path
                level_comp.handle_events(events) # Lida com os eventos do modo competitivo
                new_state = level_comp.update() # Atualiza o estado do modo competitivo
                if new_state == "ROUND_OVER":
                    level_comp = LevelCompetitive(self.window, self) # Reinicio o modo competitivo
                    self.state = 'MENU'
                level_comp.draw() # Desenho o modo competitivo

            elif self.state in ['LEVEL_1', 'LEVEL_2', 'LEVEL_3']:
                if self.state == 'LEVEL_1': current_level = level1
                elif self.state == 'LEVEL_2': current_level = level2
                else: current_level = level3

                if current_music != current_level.music_path:
                    pygame.mixer.music.load(current_level.music_path); pygame.mixer.music.play(-1)
                    current_music = current_level.music_path

                current_level.handle_events(events) # Lida com os eventos da fase atual
                new_state = current_level.update() # Atualiza o estado da fase atual

                if new_state:
                    if new_state == 'NEXT_LEVEL':
                        if self.state == 'LEVEL_1': self.state = 'LEVEL_2'
                        elif self.state == 'LEVEL_2': self.state = 'LEVEL_3'
                    else: # GAME_OVER ou VICTORY
                        self.save_scores()
                        self.state = 'MENU'
                current_level.draw() # Desenho a fase atual

            elif self.state == 'SCORE_SCREEN':
                if current_music != score_screen.music_path:
                    pygame.mixer.music.load(score_screen.music_path); pygame.mixer.music.play(-1)
                    current_music = score_screen.music_path
                score_screen.draw() # Desenho a tela de scores
                if score_screen.handle_events(events) == 'MENU':
                    self.state = 'MENU'

            pygame.display.update() # Atualizo a tela
            self.clock.tick(60) # Limito a taxa de quadros para 60 FPS

        print("Fim de Jogo!")