import pygame
import random
from code.Background import Background
from code.const import WIN_HEIGHT
from code.Player import Player
from code.Enemy import Enemy
from code.Projectile import Projectile

class Level1:
    def __init__(self, window):
        self.window = window
        self.window_width = window.get_width()
        
        self.background_manager = Background(self.window_width, WIN_HEIGHT)
        self.background_manager.add_layer('fundo1 1 camada.png', 0.2)
        self.background_manager.add_layer('fundo 1 2 camada.png', 0.2)
        self.background_manager.add_layer('fundo 1 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 1 4 camada.png', 0.8)
        self.background_manager.add_layer('fundo 1 5 camada.png', 1.2)

        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.projectile_group = pygame.sprite.Group()

        self.enemy_group = pygame.sprite.Group()
        self.num_enemies_to_spawn = 40
        self.enemies_spawned = 0
        self.enemies_defeated = 0
        self.enemy_spawn_interval = 1000
        self.last_enemy_spawn_time = 0
        self.phase_completed = False
        self.music_path = 'asset/menu musica.flac' # Trocado para a musica do menu como conversamos

    def spawn_enemy(self):
        if self.enemies_spawned < self.num_enemies_to_spawn:
            random_y = random.randint(50, WIN_HEIGHT - 50)
            spawn_x = self.window_width + 50
            new_enemy = Enemy(x=spawn_x, y=random_y)
            self.enemy_group.add(new_enemy)
            self.enemies_spawned += 1

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # CORREÇÃO da sintaxe do tiro
                if event.key == pygame.K_RETURN:
                    new_projectile = self.player.shoot()
                    if new_projectile:
                        self.projectile_group.add(new_projectile)

    def update(self):
        self.player_group.update()
        self.projectile_group.update()
        
        # Apenas continua a spawnar se a fase não estiver completa
        if not self.phase_completed:
            self.background_manager.update()
            
            current_time = pygame.time.get_ticks()
            if self.enemies_spawned < self.num_enemies_to_spawn and current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
                self.spawn_enemy()
                self.last_enemy_spawn_time = current_time
            
            self.enemy_group.update()

            # Colisão Projétil -> Inimigo
            hits = pygame.sprite.groupcollide(self.projectile_group, self.enemy_group, True, True)
            if hits:
                self.enemies_defeated += len(hits)
                print(f"Inimigos derrotados: {self.enemies_defeated}/{self.num_enemies_to_spawn}")

            # Condição de vitória
            if self.enemies_defeated >= self.num_enemies_to_spawn:
                self.phase_completed = True
                print("FASE 1 COMPLETA!")
                return "NEXT_LEVEL"

            # Colisão Jogador -> Inimigo
            if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
                print("O JOGADOR MORREU!")
                return "GAME_OVER"
        
        return None

    def draw(self):
        self.background_manager.draw(self.window)
        self.player_group.draw(self.window)
        self.enemy_group.draw(self.window)
        self.projectile_group.draw(self.window)