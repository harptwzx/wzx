import pygame
import random
import math
from pygame.math import Vector2
from config import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, player_speed_x):
        super().__init__()
        self.size = random.choice([3,3,2])
        self.radius = ASTEROID_SIZES[self.size]["radius"]
        self.score = ASTEROID_SIZES[self.size]["score"]
        self._create_shape()
        
        # 动态速度系统
        speed_boost = abs(player_speed_x) * 0.4
        self.vel = Vector2(
            random.uniform(-1.5, 1.5),  # 横向随机速度
            BASE_ASTEROID_SPEED + speed_boost
        )
        self.rect = self.image.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), -self.radius)
        )

    def _create_shape(self):
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        points = []
        num_points = random.randint(6, 12)
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            variance = random.uniform(0.7, 1.3)
            x = self.radius + self.radius * math.cos(angle) * variance
            y = self.radius + self.radius * math.sin(angle) * variance
            points.append((x, y))
        pygame.draw.polygon(self.image, WHITE, points, width=2)

    def update(self):
        self.rect.center += self.vel
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def split(self):
        if self.size > 1:
            new_asteroids = []
            for _ in range(2):
                new_asteroid = Asteroid(0)  # 分裂时不继承速度
                new_asteroid.size = self.size - 1
                new_asteroid.radius = ASTEROID_SIZES[new_asteroid.size]["radius"]
                new_asteroid.score = ASTEROID_SIZES[new_asteroid.size]["score"]
                new_asteroid._create_shape()
                new_asteroid.rect.center = self.rect.center
                new_asteroid.vel = Vector2(
                    random.uniform(-3, 3),
                    self.vel.y * 1.2 + random.uniform(0, 1)
                )
                new_asteroids.append(new_asteroid)
            return new_asteroids
        return []
