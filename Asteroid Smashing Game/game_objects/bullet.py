import pygame
from pygame.math import Vector2
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = pygame.Surface((6, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.image, GREEN, (0, 0, 6, 12))
        self.rect = self.image.get_rect(center=start_pos)
        self.vel = Vector2(0, -12)  # 提高子弹速度

    def update(self):
        self.rect.center += self.vel
        if self.rect.bottom < 0:
            self.kill()
