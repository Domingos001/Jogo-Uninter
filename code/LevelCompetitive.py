import pygame
import random
from code.Background import Background
from code.const import WIN_HEIGHT, C_WHITE, C_BLACK, C_YELLOW
from code.Player1 import Player1
from code.Player2 import Player2
from code.Enemy import Enemy
from code.Enemy2 import Enemy2
from code.Enemy3 import Enemy3

class LevelCompetitive:
    def __init__(self, window, game):
        self.game = game
        self.window = window
        self.window_width = window.get_width()

        self.background_manager = Background(self.window_width, WIN_HEIGHT)
        self.background_manager.add_layer('fundo 2 1 camada.png', 0.2)
        self.background_manager.add_layer('fundo 3 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 1 3 camada.png', 0.5)
        self.background_manager.add_layer('fundo 3 4 camada.png', 0.8)
        self.background_manager.add_layer('fundo 3 5 camada.png', 1.2)
        self.background_manager.add_layer('fundo 3 6 camada.png', 1.2)

        self.player1 = Player1()
        self.player2 = Player2()
        self.player_group = pygame.sprite.Group(self.player1, self.player2)
        
        self.projectile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.p1_score = 0
        self.p2_score = 0
        
        self.enemy_spawn_interval = 500
        self.last_enemy_spawn_time = 0
        self.music_path = 'asset/fase 2 musica.wav'
        self.hud_font = pygame.font.Font(None, 24)

        self.round_duration = 60000 
        self.start_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        random_y = random.randint(50, WIN_HEIGHT - 50)
        spawn_x = self.window_width + 50
        rand_num = random.random()
        if rand_num < 0.3: new_enemy = Enemy3(x=spawn_x, y=random_y)
        elif rand_num < 0.6: new_enemy = Enemy2(x=spawn_x, y=random_y)
        else: new_enemy = Enemy(x=spawn_x, y=random_y)
        self.enemy_group.add(new_enemy)

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    new_projectile = self.player1.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)
                if event.key == pygame.K_SPACE:
                    new_projectile = self.player2.shoot()
                    if new_projectile: self.projectile_group.add(new_projectile)

    def update(self):
        self.player_group.update()
        self.projectile_group.update()
        self.enemy_group.update()
        self.background_manager.update()
        
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.round_duration:
            print("ACABOU O TEMPO!")
            return "ROUND_OVER"

        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time
        
        for projectile in self.projectile_group:
            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemy_group, True)
            if hit_enemies:
                projectile.kill()
                for enemy in hit_enemies:
                    if projectile.owner_id == 'P1':
                        self.p1_score += enemy.points
                    elif projectile.owner_id == 'P2':
                        self.p2_score += enemy.points

        if self.player1.is_alive and pygame.sprite.spritecollide(self.player1, self.enemy_group, True):
            self.player1.get_hit()
        
        if self.player2.is_alive and pygame.sprite.spritecollide(self.player2, self.enemy_group, True):
            self.player2.get_hit()

        if not self.player1.is_alive and not self.player2.is_alive:
            return "ROUND_OVER"
            
        return None

    def draw(self):
        self.background_manager.draw(self.window)
        self.player_group.draw(self.window)
        self.enemy_group.draw(self.window)
        self.projectile_group.draw(self.window)

        p1_text = f"P1 Score: {self.p1_score} | Vidas: {self.player1.lives}"
        p2_text = f"P2 Score: {self.p2_score} | Vidas: {self.player2.lives}"
        time_left = max(0, (self.round_duration - (pygame.time.get_ticks() - self.start_time)) // 1000)
        timer_text = f"Tempo: {time_left}"

        p1_surf = self.hud_font.render(p1_text, True, C_WHITE)
        self.window.blit(p1_surf, (10, 10))
        
        p2_surf = self.hud_font.render(p2_text, True, C_WHITE)
        p2_rect = p2_surf.get_rect(top=10, right=self.window_width - 10)
        self.window.blit(p2_surf, p2_rect)

        timer_surf = self.hud_font.render(timer_text, True, C_YELLOW)
        timer_rect = timer_surf.get_rect(midtop=(self.window_width / 2, 10))
        self.window.blit(timer_surf, timer_rect)