import pygame
from code.Menu import Menu
from code.Level1 import Level1
from code.const import WIN_WIDTH, WIN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.state = 'MENU'
        self.clock = pygame.time.Clock()

    def run(self):
        menu = Menu(self.window)
        level1 = Level1(self.window)
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
                    pygame.mixer.music.load(menu.music_path)
                    pygame.mixer.music.play(-1)
                    current_music = menu.music_path
                
                menu.draw()
                chosen_option = menu.handle_events(events)
                
                if chosen_option:
                    if chosen_option == 'NEW GAME 1P':
                        self.state = 'LEVEL_1'
                    elif chosen_option == 'EXIT':
                        break

            elif self.state == 'LEVEL_1':
                if current_music != level1.music_path:
                    pygame.mixer.music.load(level1.music_path)
                    pygame.mixer.music.play(-1)
                    current_music = level1.music_path

                # Passa os eventos para a fase 1 lidar com o tiro
                level1.handle_events(events) 
                
                # O update da fase agora pode retornar um novo estado
                new_state = level1.update() 
                if new_state:
                    self.state = new_state # Ex: 'GAME_OVER' ou 'NEXT_LEVEL'
                    # Aqui você adicionaria a lógica para o que fazer nesses casos
                    if new_state == 'GAME_OVER' or new_state == 'NEXT_LEVEL':
                        print(f"Mudando para o estado: {new_state}")
                        # Por enquanto, vamos voltar ao menu
                        level1 = Level1(self.window) # Reinicia a fase
                        self.state = 'MENU'

                level1.draw()

            pygame.display.update()
            self.clock.tick(60)
        
        print("Fim de Jogo!")