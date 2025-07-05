# Arquivo: code/Level1.py
# Define a classe para a Fase 1 do jogo.

import pygame
import random
from code.Background import Background
from code.const import WIN_HEIGHT, C_WHITE, C_BLACK
from code.Player1 import Player1
from code.Player2 import Player2
from code.Projectile import Projectile
from code.Enemy import Enemy
from code.utils import resource_path

class Level1:
    def __init__(self, window, game, game_mode):
        self.game = game
        self.window = window
        self.window_width = window.get_width()
        self.game_mode = game_mode
        
        # Configura o fundo da fase 1
        self.background_manager = Background(self.window_width, WIN_HEIGHT)
        self.background_manager.add_layer('fundo1 1 camada.png', 0.2)
        self.background_manager.add_layer('fundo 1 2 camada.png', 0.2)
        self.background_manager.add_layer('fundo 1 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 1 4 camada.png', 0.8)
        self.background_manager.add_layer('fundo 1 5 camada.png', 1.2)

        # Cria os jogadores baseado no modo de jogo
        self.player1 = Player1()
        self.player_group = pygame.sprite.Group(self.player1)
        if self.game_mode == '2P_COOP':
            self.player2 = Player2()
            self.player_group.add(self.player2)

        # Cria os grupos de sprites
        self.projectile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Define os objetivos e configurações da fase
        self.enemy_defeat_goal = 20
        self.enemies_defeated = 0
        self.enemy_spawn_interval = 1000 # 1 segundo
        self.last_enemy_spawn_time = 0
        
        # Define a música da fase
        self.music_path = resource_path('asset/menu musica.flac') # Reutilizando música do menu
        
        # Define a fonte para o placar
        self.hud_font = pygame.font.Font(None, 20)

    def spawn_enemy(self):
        """ Cria um novo inimigo do tipo 1. """
        random_y = random.randint(50, WIN_HEIGHT - 50)
        spawn_x = self.window_width + 50
        new_enemy = Enemy(x=spawn_x, y=random_y)
        self.enemy_group.add(new_enemy)

    def handle_events(self, event_list):
        """ Gerencia os inputs de tiro dos jogadores. """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # Tiro do Jogador 1
                if event.key == pygame.K_RETURN:
                    new_projectile = self.player1.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)
                
                # Tiro do Jogador 2 (apenas no modo cooperativo)
                if self.game_mode == '2P_COOP' and event.key == pygame.K_SPACE:
                    new_projectile = self.player2.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)

    def update(self):
        """ Atualiza toda a lógica da fase a cada quadro. """
        self.player_group.update()
        self.projectile_group.update()
        self.enemy_group.update()
        self.background_manager.update()

        # Verifica colisão: Projétil -> Inimigo
        collided_enemies = pygame.sprite.groupcollide(self.projectile_group, self.enemy_group, True, True)
        for enemy_list in collided_enemies.values():
            for enemy in enemy_list:
                self.enemies_defeated += 1
                self.game.current_score += enemy.points
        
        # Verifica condição de vitória (atingiu o objetivo)
        if self.enemies_defeated >= self.enemy_defeat_goal:
            print("FASE 1 COMPLETA!")
            return "NEXT_LEVEL"

        # Verifica colisão: Jogador -> Inimigo (Game Over)
        # O 'True' remove o jogador que colidiu do grupo
        if pygame.sprite.groupcollide(self.player_group, self.enemy_group, True, False):
            print("O JOGADOR MORREU!")
            return "GAME_OVER"
        
        # Spawna novos inimigos se o objetivo ainda não foi alcançado
        current_time = pygame.time.get_ticks()
        if self.enemies_defeated < self.enemy_defeat_goal and current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time
        
        return None # Continua na fase

    def draw(self):
        """ Desenha todos os elementos da fase na tela. """
        self.background_manager.draw(self.window)
        self.player_group.draw(self.window)
        self.enemy_group.draw(self.window)
        self.projectile_group.draw(self.window)

        # Desenha o placar
        score_text = f"Inimigos: {self.enemies_defeated} / {self.enemy_defeat_goal} | Score: {self.game.current_score}"
        text_surf_shadow = self.hud_font.render(score_text, True, C_BLACK)
        self.window.blit(text_surf_shadow, (12, 12))
        text_surf = self.hud_font.render(score_text, True, C_WHITE)
        self.window.blit(text_surf, (10, 10))