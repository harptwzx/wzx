import pygame
from pygame.math import Vector2
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._create_ship_shape()
        self.pos = Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT-50)
        self.rect = self.image.get_rect(center=self.pos)
        self.base_speed = PLAYER_SPEED
        self.current_speed = 0
        self.total_distance = 0
        self.ammo = MAX_AMMO
        self.last_shot_time = 0
        self.radius = 15

    def _create_ship_shape(self):
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, PLAYER_SHAPE, width=2)
        pygame.draw.line(self.image, RED, (12, 35), (18, 35), 3)

    def handle_movement(self, move_x):
        # 惯性运动系统
        target_speed = move_x * self.base_speed
        self.current_speed += (target_speed - self.current_speed) * 0.15
        self.pos.x += self.current_speed
        self.pos.x = max(30, min(SCREEN_WIDTH-30, self.pos.x))  # 保留边界
        self.rect.center = self.pos
        self.total_distance += abs(self.current_speed)

    def update(self):
        if self.ammo < MAX_AMMO:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > AMMO_RECHARGE_TIME * 1000:
                self.ammo += 1
                self.last_shot_time = current_time
