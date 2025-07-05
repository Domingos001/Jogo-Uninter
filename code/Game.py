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

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.state = 'MENU'
        self.clock = pygame.time.Clock()
        
        self.player1_name = ""
        self.player2_name = ""
        self.current_score = 0
        self.high_scores = []
        
        self.db_path = 'highscore.db'
        self.init_database()
        self.load_scores()
        
        self.game_mode = '1P'

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date_saved TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

    def load_scores(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, score, date_saved FROM high_scores ORDER BY score DESC LIMIT 5")
        results = cursor.fetchall()
        conn.close()
        self.high_scores = [{'name': name, 'score': score, 'date': date_saved} for name, score, date_saved in results]

    def save_scores(self):
        player_names = self.player1_name
        if self.game_mode == '2P_COOP' and self.player2_name:
            player_names += f" & {self.player2_name}"
        
        if player_names:
            today_date = date.today().strftime('%d/%m/%Y')
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO high_scores (name, score, date_saved) VALUES (?, ?, ?)", 
                        (player_names, self.current_score, today_date))
            conn.commit()
            conn.close()
            self.load_scores()

    def start_new_game(self):
        self.current_score = 0
        return (Level1(self.window, self, self.game_mode), 
                Level2(self.window, self, self.game_mode), 
                Level3(self.window, self, self.game_mode),
                LevelCompetitive(self.window, self))

    def run(self):
        menu = Menu(self.window)
        name_input_screen = NameInputScreen(self.window)
        score_screen = ScoreScreen(self.window, self.high_scores)
        level1, level2, level3, level_comp = self.start_new_game()
        
        current_music = None

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.window.fill((0, 0, 0))

            if self.state == 'MENU':
                if current_music != menu.music_path:
                    pygame.mixer.music.load(menu.music_path); pygame.mixer.music.play(-1)
                    current_music = menu.music_path
                menu.draw()
                chosen_option = menu.handle_events(events)
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
                name_input_screen.draw()
                player_names = name_input_screen.handle_events(events)
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
                level_comp.handle_events(events)
                new_state = level_comp.update()
                if new_state == "ROUND_OVER":
                    print("ROUND OVER! Voltando ao menu.")
                    level_comp = LevelCompetitive(self.window, self) # Reinicia a fase
                    self.state = 'MENU'
                level_comp.draw()

            elif self.state in ['LEVEL_1', 'LEVEL_2', 'LEVEL_3']:
                if self.state == 'LEVEL_1': current_level = level1
                elif self.state == 'LEVEL_2': current_level = level2
                else: current_level = level3
                
                if current_music != current_level.music_path:
                    pygame.mixer.music.load(current_level.music_path); pygame.mixer.music.play(-1)
                    current_music = current_level.music_path
                
                current_level.handle_events(events)
                new_state = current_level.update()
                
                if new_state:
                    if new_state == 'NEXT_LEVEL':
                        if self.state == 'LEVEL_1': self.state = 'LEVEL_2'
                        elif self.state == 'LEVEL_2': self.state = 'LEVEL_3'
                    else: # GAME_OVER ou VICTORY
                        self.save_scores()
                        self.state = 'MENU'
                current_level.draw()
            
            elif self.state == 'SCORE_SCREEN':
                if current_music != score_screen.music_path:
                    pygame.mixer.music.load(score_screen.music_path); pygame.mixer.music.play(-1)
                    current_music = score_screen.music_path
                score_screen.draw()
                if score_screen.handle_events(events) == 'MENU':
                    self.state = 'MENU'

            pygame.display.update()
            self.clock.tick(60)
        
        print("Fim de Jogo!")