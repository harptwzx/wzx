import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from mineblock import *

SCREEN_WIDTH = BLOCK_WIDTH * SIZE
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('扫雷')

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)

    # 加载图片资源
    img_dict = {i: pygame.transform.smoothscale(pygame.image.load(f'resources/{i}.bmp').convert(), (SIZE, SIZE)) for i in range(9)}
    img_blank = pygame.transform.smoothscale(pygame.image.load('resources/blank.bmp').convert(), (SIZE, SIZE))
    img_flag = pygame.transform.smoothscale(pygame.image.load('resources/flag.bmp').convert(), (SIZE, SIZE))
    img_ask = pygame.transform.smoothscale(pygame.image.load('resources/ask.bmp').convert(), (SIZE, SIZE))
    img_mine = pygame.transform.smoothscale(pygame.image.load('resources/mine.bmp').convert(), (SIZE, SIZE))
    img_blood = pygame.transform.smoothscale(pygame.image.load('resources/blood.bmp').convert(), (SIZE, SIZE))
    img_error = pygame.transform.smoothscale(pygame.image.load('resources/error.bmp').convert(), (SIZE, SIZE))

    # 加载笑脸按钮
    face_size = int(SIZE * 1.25)
    img_face = {
        'fail': pygame.transform.smoothscale(pygame.image.load('resources/face_fail.bmp').convert(), (face_size, face_size)),
        'normal': pygame.transform.smoothscale(pygame.image.load('resources/face_normal.bmp').convert(), (face_size, face_size)),
        'success': pygame.transform.smoothscale(pygame.image.load('resources/face_success.bmp').convert(), (face_size, face_size))
    }
    face_pos = ((SCREEN_WIDTH - face_size) // 2, (SIZE * 2 - face_size) // 2)

    bgcolor = (225, 225, 225)
    block = MineBlock()
    game_status = GameStatus.readied
    start_time = None
    elapsed_time = 0

    while True:
        screen.fill(bgcolor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
            # 游戏结束后仅允许点击笑脸按钮
            if game_status in (GameStatus.over, GameStatus.win):
                if event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if (face_pos[0] <= mouse_x <= face_pos[0] + face_size and 
                        face_pos[1] <= mouse_y <= face_pos[1] + face_size):
                        game_status = GameStatus.readied
                        block = MineBlock()
                        start_time = time.time()
                        elapsed_time = 0
                continue  # 跳过其他事件处理
            
            # 处理鼠标按下事件（双击预判）
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = (mouse_y - 2 * SIZE) // SIZE
                if 0 <= x < BLOCK_WIDTH and 0 <= y < BLOCK_HEIGHT:
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0] and buttons[2]:
                        mine = block.getmine(x, y)
                        if mine.status == BlockStatus.opened:
                            block.double_mouse_button_down(x, y)
            
            # 处理鼠标释放事件
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                
                # 点击笑脸按钮
                if (face_pos[0] <= mouse_x <= face_pos[0] + face_size and 
                    face_pos[1] <= mouse_y <= face_pos[1] + face_size):
                    game_status = GameStatus.readied
                    block = MineBlock()
                    start_time = time.time()
                    elapsed_time = 0
                    continue
                
                # 转换游戏区域坐标
                x = mouse_x // SIZE
                y = (mouse_y - 2 * SIZE) // SIZE
                if not (0 <= x < BLOCK_WIDTH and 0 <= y < BLOCK_HEIGHT):
                    continue
                
                mine = block.getmine(x, y)
                
                # 左键点击
                if event.button == 1:
                    if game_status == GameStatus.readied:
                        game_status = GameStatus.started
                        start_time = time.time()
                        elapsed_time = 0
                    
                    if mine.status == BlockStatus.normal:
                        if not block.open_mine(x, y):
                            game_status = GameStatus.over
                
                # 右键点击
                elif event.button == 3:
                    if mine.status == BlockStatus.normal:
                        mine.status = BlockStatus.flag
                    elif mine.status == BlockStatus.flag:
                        mine.status = BlockStatus.ask
                    elif mine.status == BlockStatus.ask:
                        mine.status = BlockStatus.normal

        # 绘制游戏方块
        flag_count = 0
        opened_count = 0
        for row in block.block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                status = mine.status
                if status == BlockStatus.opened:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif status == BlockStatus.ask:
                    screen.blit(img_ask, pos)
                elif status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and status == BlockStatus.flag:
                    screen.blit(img_error, pos)
                else:
                    screen.blit(img_blank, pos)

        # 更新状态栏
        print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, f'{MINE_COUNT - flag_count:02d}', red)
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, f'{elapsed_time:03d}', red)

        # 胜利条件
        if opened_count == BLOCK_WIDTH * BLOCK_HEIGHT - MINE_COUNT:
            game_status = GameStatus.win

        # 绘制笑脸按钮
        if game_status == GameStatus.over:
            screen.blit(img_face['fail'], face_pos)
        elif game_status == GameStatus.win:
            screen.blit(img_face['success'], face_pos)
        else:
            screen.blit(img_face['normal'], face_pos)

        pygame.display.update()

if __name__ == '__main__':
    main()
