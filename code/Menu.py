import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.const import WIN_WIDTH, C_WHITE, MENU_OPTION, C_YELLOW

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('asset/menu.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        
        self.selected_option = 0
        self.title_font = pygame.font.SysFont("Lucida Sans Typewriter", 70)
        self.option_font = pygame.font.SysFont("Lucida Sans Typewriter", 20)
        
        # --- CORREÇÃO AQUI ---
        # Forçando a tocar a música da fase 1 no menu.
        self.music_path = 'asset/fase 1 musica.mp3'

    def draw(self):
        self.window.blit(self.surf, self.rect)
        
        self.menu_text(self.title_font, "Bubble", C_WHITE, (WIN_WIDTH / 2, 70))
        self.menu_text(self.title_font, "Beam", C_WHITE, (WIN_WIDTH / 2, 120))

        for i, option in enumerate(MENU_OPTION):
            color = C_YELLOW if i == self.selected_option else C_WHITE
            self.menu_text(self.option_font, option, color, (WIN_WIDTH / 2, 200 + 25 * i))

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(MENU_OPTION)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(MENU_OPTION)
                elif event.key == pygame.K_RETURN:
                    return MENU_OPTION[self.selected_option]
        return None

    def menu_text(self, font: Font, text: str, text_color: tuple, text_center_pos: tuple):
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)