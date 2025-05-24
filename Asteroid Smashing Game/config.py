import pygame

# 屏幕设置
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 玩家设置
PLAYER_SPEED = 3
PLAYER_SHAPE = [(15, 0), (5, 30), (25, 30)]  # 竖版飞船

# 弹药系统
MAX_AMMO = 6
AMMO_RECHARGE_TIME = 2  # 秒/每发
FIRE_COOLDOWN = 200     # 毫秒，发射间隔

# 小行星设置
ASTEROID_SIZES = {
    3: {"radius": 40, "score": 20},
    2: {"radius": 25, "score": 50},
    1: {"radius": 15, "score": 100}
}
SPAWN_RATE = 45
BASE_ASTEROID_SPEED = 1.5
DISTANCE_FACTOR = 0.1   # 距离换算系数

# 触摸控制
TOUCH_DEADZONE = 20
MAX_TOUCH_POWER = 100
