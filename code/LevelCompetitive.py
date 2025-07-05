

import pygame
import random
from code.Background import Background
from code.const import WIN_HEIGHT, WIN_WIDTH, C_WHITE, C_YELLOW
from code.Player1 import Player1
from code.Player2 import Player2
from code.Enemy import Enemy
from code.Enemy2 import Enemy2
from code.Enemy3 import Enemy3
from code.utils import resource_path

class LevelCompetitive:
    def __init__(self, window, game):
        self.game = game
        self.window = window
        self.window_width = window.get_width()

        # Configura um fundo para a fase
        self.background_manager = Background(self.window_width, WIN_HEIGHT)
        self.background_manager.add_layer('fundo 2 1 camada.png', 0.2)
        self.background_manager.add_layer('fundo 3 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 1 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 3 4 camada.png', 0.8)
        self.background_manager.add_layer('fundo 3 5 camada.png', 1.2)
        self.background_manager.add_layer('fundo 3 6 camada.png', 1.2)

        # Cria os dois jogadores e os adiciona a um grupo de sprites
        self.player1 = Player1()
        self.player2 = Player2()
        self.player_group = pygame.sprite.Group(self.player1, self.player2)
        
        # Cria grupos para os projéteis e inimigos
        self.projectile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Contadores de score separados para cada jogador
        self.p1_score = 0
        self.p2_score = 0
        
        # Lógica de spawn de inimigos (bem rápido para ser desafiador)
        self.enemy_spawn_interval = 500 # Meio segundo
        self.last_enemy_spawn_time = 0
        
        # Define a música e a fonte para o HUD (Heads-Up Display)
        self.music_path = resource_path('asset/fase 2 musica.wav')
        self.hud_font = pygame.font.Font(None, 24)

        # Timer da partida: 1 minuto (60.000 milissegundos)
        self.round_duration = 60000
        self.start_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        """ Cria um novo inimigo de tipo aleatório. """
        random_y = random.randint(50, WIN_HEIGHT - 50)
        spawn_x = self.window_width + 50
        
        rand_num = random.random()
        if rand_num < 0.3: # 30% de chance para o inimigo 3
            new_enemy = Enemy3(x=spawn_x, y=random_y)
        elif rand_num < 0.6: # 30% de chance para o inimigo 2
            new_enemy = Enemy2(x=spawn_x, y=random_y)
        else: # 40% de chance para o inimigo 1
            new_enemy = Enemy(x=spawn_x, y=random_y)
            
        self.enemy_group.add(new_enemy)

    def handle_events(self, event_list):
        """ Gerencia os inputs de tiro dos dois jogadores. """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Tiro do Jogador 1
                    new_projectile = self.player1.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)
                
                if event.key == pygame.K_SPACE: # Tiro do Jogador 2
                    new_projectile = self.player2.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)

    def update(self):
        """ Atualiza toda a lógica da fase competitiva a cada quadro. """
        # Primeiro, verifica se o tempo da partida acabou
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.round_duration:
            print("ACABOU O TEMPO!")
            return "ROUND_OVER"

        # Atualiza todos os sprites e o fundo
        self.player_group.update()
        self.projectile_group.update()
        self.enemy_group.update()
        self.background_manager.update()
        
        # Spawna novos inimigos baseado no tempo
        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time
        
        # Verifica colisão: Projétil -> Inimigo
        for projectile in self.projectile_group:
            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemy_group, True)
            if hit_enemies:
                projectile.kill() # Remove o projétil
                for enemy in hit_enemies:
                    # Adiciona os pontos ao jogador que atirou
                    if projectile.owner_id == 'P1':
                        self.p1_score += enemy.points
                    elif projectile.owner_id == 'P2':
                        self.p2_score += enemy.points

        # Verifica colisão: Inimigo -> Jogadores (separadamente)
        if self.player1.is_alive and pygame.sprite.spritecollide(self.player1, self.enemy_group, True):
            self.player1.get_hit()
        
        if self.player2.is_alive and pygame.sprite.spritecollide(self.player2, self.enemy_group, True):
            self.player2.get_hit()

        # Se os dois jogadores perderem todas as vidas, o round também acaba
        if not self.player1.is_alive and not self.player2.is_alive:
            return "ROUND_OVER"
            
        return None # Se nada aconteceu, retorna None para continuar a partida

    def draw(self):
        """ Desenha todos os elementos da fase na tela. """
        self.background_manager.draw(self.window)
        self.player_group.draw(self.window)
        self.enemy_group.draw(self.window)
        self.projectile_group.draw(self.window)

        # Desenha o HUD (placar e informações) do modo competitivo
        p1_text = f"P1 Score: {self.p1_score} | Vidas: {self.player1.lives}"
        p2_text = f"P2 Score: {self.p2_score} | Vidas: {self.player2.lives}"
        time_left = max(0, (self.round_duration - (pygame.time.get_ticks() - self.start_time)) // 1000)
        timer_text = f"Tempo: {time_left}"

        # Placar P1 (canto superior esquerdo)
        p1_surf = self.hud_font.render(p1_text, True, C_WHITE)
        self.window.blit(p1_surf, (10, 10))
        
        # Placar P2 (canto superior direito)
        p2_surf = self.hud_font.render(p2_text, True, C_WHITE)
        p2_rect = p2_surf.get_rect(top=10, right=self.window_width - 10)
        self.window.blit(p2_surf, p2_rect)

        # Cronômetro (centro superior)
        timer_surf = self.hud_font.render(timer_text, True, C_YELLOW)
        timer_rect = timer_surf.get_rect(midtop=(self.window_width / 2, 10))
        self.window.blit(timer_surf, timer_rect)