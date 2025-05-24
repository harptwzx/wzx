import pygame
import random
from pygame.math import Vector2
from config import *
from game_objects.player import Player
from game_objects.asteroid import Asteroid
from game_objects.bullet import Bullet

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("星际拓荒-终极版")
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.spawn_counter = 0
        self.fire_cooldown = 0
        self.touch_start_x = None

    def _handle_input(self):
        current_time = pygame.time.get_ticks()
        move_x = 0
        
        # 处理事件队列
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            # 触摸控制
            if event.type == pygame.FINGERDOWN:
                if event.x * SCREEN_WIDTH < SCREEN_WIDTH/2:
                    self.touch_start_x = event.x * SCREEN_WIDTH
            elif event.type == pygame.FINGERMOTION and self.touch_start_x is not None:
                current_x = event.x * SCREEN_WIDTH
                delta_x = current_x - self.touch_start_x
                move_x = delta_x / 60  # 灵敏度调节
                move_x = max(-1, min(1, move_x))
            elif event.type == pygame.FINGERUP:
                self.touch_start_x = None

        # 键盘控制
        keys = pygame.key.get_pressed()
        if not self.touch_start_x:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move_x = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move_x = 1

        self.player.handle_movement(move_x)

        # 发射控制
        can_fire = (
            (current_time - self.fire_cooldown > FIRE_COOLDOWN) and
            (self.player.ammo > 0)
        )
        if can_fire:
            # 鼠标检测
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pressed[0] and mouse_pos[0] > SCREEN_WIDTH/2:
                self._fire_bullet(current_time)

            # 键盘检测
            elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self._fire_bullet(current_time)

            # 触摸检测
            for event in pygame.event.get():
                if event.type == pygame.FINGERDOWN:
                    if event.x * SCREEN_WIDTH > SCREEN_WIDTH/2:
                        self._fire_bullet(current_time)

    def _fire_bullet(self, current_time):
        bullet = Bullet(self.player.rect.center)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)
        self.player.ammo -= 1
        self.fire_cooldown = current_time
        self.player.last_shot_time = current_time

    def _spawn_asteroids(self):
        self.spawn_counter += 1
        if self.spawn_counter > SPAWN_RATE:
            self.spawn_counter = 0
            asteroid = Asteroid(self.player.current_speed)
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)

    def _check_collisions(self):
        # 子弹碰撞检测
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(
                bullet, self.asteroids, True, pygame.sprite.collide_circle
            )
            for asteroid in hits:
                self.score += asteroid.score
                new_asteroids = asteroid.split()
                for new_asteroid in new_asteroids:
                    self.all_sprites.add(new_asteroid)
                    self.asteroids.add(new_asteroid)
                bullet.kill()
        
        # 玩家碰撞检测
        if pygame.sprite.spritecollide(
            self.player, self.asteroids, False, pygame.sprite.collide_circle
        ):
            self._game_over()

    def _draw_hud(self):
        # 行进距离
        font = pygame.font.Font(None, 36)
        distance_km = self.player.total_distance * DISTANCE_FACTOR
        text = font.render(f"里程: {distance_km:.1f} km", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH-250, 10))
        
        # 弹药显示
        for i in range(self.player.ammo):
            x = SCREEN_WIDTH - 40 - i * 15
            pygame.draw.rect(self.screen, GREEN, (x, SCREEN_HEIGHT-30, 10, 20))
        
        # 分数显示
        text = font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        # 控制区分割线
        pygame.draw.line(
            self.screen, WHITE,
            (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2
        )

    def _game_over(self):
        print(f"游戏结束! score: {self.score} 里程: {self.player.total_distance * DISTANCE_FACTOR:.1f} km")
        pygame.quit()
        quit()

    def run(self):
        while True:
            self._handle_input()
            self._spawn_asteroids()
            self.all_sprites.update()
            self._check_collisions()
            
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self._draw_hud()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
