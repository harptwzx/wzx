import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_HEIGHT = HEIGHT - 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "gray": (83, 83, 83),
    "blue": (63, 63, 163),
    "red": (163, 63, 63),
    "green": (63, 163, 63)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()

# Dinosaur configurations
DINO_CONFIGS = [
    {
        "name": "Standard",
        "color": "gray",
        "gravity": 0.8,
        "jump_strength": -16,
        "speed_mod": 1.0,
        "scale": 1.0
    },
    {
        "name": "Light",
        "color": "blue",
        "gravity": 0.6,
        "jump_strength": -18,
        "speed_mod": 1.2,
        "scale": 0.9
    },
    {
        "name": "Heavy",
        "color": "red",
        "gravity": 1.0,
        "jump_strength": -16,
        "speed_mod": 1.5,
        "scale": 1.2
    }
]

# Game states
STATE_SELECT = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.base_size = (60, 80)
        self.scale = config["scale"]
        
        self.image = pygame.Surface(
            (int(self.base_size[0]*self.scale), 
            int(self.base_size[1]*self.scale)),
            pygame.SRCALPHA
        )
        self._draw_dino()
        
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_HEIGHT
        self.hitbox = pygame.Rect(
            self.rect.x + 15*self.scale,
            self.rect.y + 20*self.scale,
            30*self.scale,
            60*self.scale
        )
        self.velocity = 0
        self.gravity = config["gravity"]
        self.jump_strength = config["jump_strength"]
        self.on_ground = True

    def _draw_dino(self):
        color = COLORS[self.config["color"]]
        scale = self.scale
        pygame.draw.rect(self.image, color, (15*scale, 20*scale, 30*scale, 40*scale))
        pygame.draw.rect(self.image, color, (35*scale, 0, 20*scale, 20*scale))
        pygame.draw.rect(self.image, WHITE, (45*scale, 5*scale, 5*scale, 5*scale))
        pygame.draw.rect(self.image, color, (15*scale, 60*scale, 10*scale, 20*scale))
        pygame.draw.rect(self.image, color, (35*scale, 60*scale, 10*scale, 20*scale))

    def jump(self):
        if self.on_ground:
            self.velocity = self.jump_strength
            self.on_ground = False

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity = 0
            self.on_ground = True
        
        self.hitbox.x = self.rect.x + 15*self.scale
        self.hitbox.y = self.rect.y + 20*self.scale

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        self._draw_cactus()
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_HEIGHT
        self.rect.x = WIDTH + random.randint(50, 200)
        self.hitbox = pygame.Rect(10, 10, 15, 50)
        self.speed = speed

    def _draw_cactus(self):
        pygame.draw.rect(self.image, COLORS["green"], (10, 10, 15, 50))
        pygame.draw.rect(self.image, COLORS["green"], (5, 30, 15, 15))
        pygame.draw.rect(self.image, COLORS["green"], (15, 20, 10, 20))

    def update(self):
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 10
        self.hitbox.y = self.rect.y + 10
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.state = STATE_SELECT
        self.selected_config = None
        self.dino = None
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.base_speed = 7
        self.current_speed = 7
        self.last_speed_increase = 0

    def draw_selection_screen(self):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 48)
        title = font.render("Choose Your Dino", True, BLACK)
        screen.blit(title, (WIDTH//2-120, 20))  # 上移标题

        start_x = 50
        box_width = 200
        for i, config in enumerate(DINO_CONFIGS):
            x = start_x + i*(box_width+50)
            y = 100  # 上移选择框
            
            border_color = COLORS[config["color"]] 
            if self.selected_config == config:
                border_color = (255, 215, 0)
                pygame.draw.rect(screen, (255, 255, 0), (x-15, y-15, 230, 230))
            
            pygame.draw.rect(screen, border_color, (x-10, y-10, 200, 200), 5)
            
            preview = pygame.Surface((100, 100), pygame.SRCALPHA)
            temp_dino = Dinosaur(config)
            temp_dino.rect.center = (50, 50)
            preview.blit(temp_dino.image, temp_dino.rect)
            screen.blit(preview, (x+50, y+20))
            
            info_font = pygame.font.Font(None, 24)  # 缩小字体
            texts = [
                f"Name: {config['name']}",
                f"Weight: {config['gravity']*10:.1f}",
                f"Jump: {abs(config['jump_strength'])}",
                f"Speed: {config['speed_mod']*100}%",
                f"Size: {config['scale']*100}%"
            ]
            for j, text in enumerate(texts):
                txt = info_font.render(text, True, BLACK)
                screen.blit(txt, (x+10, y + 120 + j*18))  # 调整行间距

        tip_font = pygame.font.Font(None, 28)
        tip = tip_font.render("Click to select and start", True, BLACK)
        screen.blit(tip, (WIDTH//2-140, HEIGHT-70))  # 上移提示文字

    def handle_selection_click(self, pos):
        start_x = 50
        box_width = 200
        for i in range(len(DINO_CONFIGS)):
            x = start_x + i*(box_width+50)
            y = 100  # 保持与draw方法一致
            rect = pygame.Rect(x-10, y-10, 200, 200)
            if rect.collidepoint(pos):
                self.selected_config = DINO_CONFIGS[i]
                self.start_game()
                return True
        return False

    def start_game(self):
        if self.selected_config:
            self.dino = Dinosaur(self.selected_config)
            self.all_sprites.add(self.dino)
            self.current_speed = self.base_speed * self.selected_config["speed_mod"]
            self.state = STATE_PLAYING

    def spawn_obstacle(self):
        if random.random() < 0.02 and len(self.obstacles) < 2:
            cactus = Cactus(self.current_speed)
            self.obstacles.add(cactus)
            self.all_sprites.add(cactus)

    def check_collision(self):
        for cactus in self.obstacles:
            if self.dino.hitbox.colliderect(cactus.hitbox):
                self.state = STATE_GAMEOVER
                return

    def update_score(self):
        self.score += 0.1
        if self.score - self.last_speed_increase >= 50:
            self.current_speed += 1 * self.selected_config["speed_mod"]
            self.last_speed_increase = self.score
            for cactus in self.obstacles:
                cactus.speed = self.current_speed

    def reset(self):
        self.__init__()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.state == STATE_SELECT:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_selection_click(event.pos)
                
                elif self.state == STATE_PLAYING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.dino.jump()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == STATE_GAMEOVER:
                    self.reset()

            if self.state == STATE_SELECT:
                self.draw_selection_screen()
            
            elif self.state == STATE_PLAYING:
                self.spawn_obstacle()
                self.all_sprites.update()
                self.check_collision()
                self.update_score()

                screen.fill(WHITE)
                pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 3)
                
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Score: {int(self.score)}", True, BLACK)
                speed_text = font.render(f"Speed: {self.current_speed:.1f}", True, BLACK)
                screen.blit(score_text, (10, 10))
                screen.blit(speed_text, (10, 40))
                
                self.all_sprites.draw(screen)

            elif self.state == STATE_GAMEOVER:
                screen.fill(WHITE)
                font = pygame.font.Font(None, 48)
                text = font.render(f"Final Score: {int(self.score)}", True, BLACK)
                screen.blit(text, (WIDTH//2-100, HEIGHT//2-50))
                
                restart_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+20, 200, 50)
                pygame.draw.rect(screen, (200, 200, 200), restart_rect)
                pygame.draw.rect(screen, BLACK, restart_rect, 2)
                text = font.render("Click to Restart", True, BLACK)
                screen.blit(text, (WIDTH//2-70, HEIGHT//2+35))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()