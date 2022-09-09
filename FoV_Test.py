import sys
import time
import pygame
import math
from pygame.locals import *
import numpy as np
import pandas as pd
from pyuc import MyWindow

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

right = 0

SIZE = 20    # THE SCALE OF THE DOTS
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('FOV TEST')

reference_color = (0, 0, 200)  # the reference dot color
test_dot_color = (200, 0, 0)
draw_line = (100, 200, 45)
temp_color = (0, 200, 0)

font1 = pygame.font.SysFont('SimHei', 24)  # 得分的字体
font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
red = (200, 30, 30)  # GAME OVER 的字体颜色
fwidth, fheight = font2.size('TEST IS OVER')
line_width = 1  # 网格线宽度
black = (0, 0, 0)  # 网格线颜色
bgcolor = (40, 40, 60)  # 背景色

# 方向，起始向右
pos_x = 1
pos_y = 0
# 如果蛇正在向右移动，那么快速点击向下向左，由于程序刷新没那么快，向下事件会被向左覆盖掉，导致蛇后退，直接GAME OVER
# b 变量就是用于防止这种情况的发生
b = True
# 范围
scope_x = (0, SCREEN_WIDTH // SIZE - 1)
scope_y = (2, SCREEN_HEIGHT // SIZE - 1)

game_over = True
start = False  #
score = 0  #
part_set = 10 # the parts been divided

division_set = 6
cal_mouse = 2 * part_set  # the number before end
last_move_time = None
pause = False  # 暂停
position_storage = []

#the parameters of the FOV testing
reference_position_x = SCREEN_WIDTH / 2
reference_position_y = SCREEN_HEIGHT / 2
length_line = SCREEN_WIDTH / 2
level_length = length_line / division_set

while True:
    # the screen color
    screen.fill(bgcolor)
    # 填充一半区域的放射线
    pygame.draw.circle(screen, reference_color, (reference_position_x, reference_position_y), 10, 0)
    for angle in np.arange(0, math.radians(180), math.radians(180/part_set)):
            pygame.draw.line(screen, black, (reference_position_x + length_line * math.cos(angle),
                                            reference_position_y + length_line * math.sin(angle)),
                            (reference_position_x - length_line * math.cos(angle),
                            reference_position_y - length_line * math.sin(angle)), line_width)
            # 画点
            for level_num in range(- division_set, 0, 1):
                pygame.draw.circle(screen, test_dot_color, (
                reference_position_x + level_num * level_length * math.cos(angle),
                reference_position_y + level_num * level_length * math.sin(angle)), 3, 0)
            for level_num in range(1, division_set + 1, 1):
                pygame.draw.circle(screen, test_dot_color, (
                reference_position_x + level_num * level_length * math.cos(angle),
                reference_position_y + level_num * level_length * math.sin(angle)), 3, 0)
    for event in pygame.event.get():

            # the usage of mouse

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos
                pygame.draw.circle(screen, temp_color, (mx, my), 3, 0)
                position_storage.append([mx, my])
                cal_mouse -= 1
            if event.type == QUIT:

                sys.exit()
    if cal_mouse == 0:
        pygame.draw.polygon(screen, draw_line, position_storage, 2)
        m = np.array(position_storage)
        if right == 1:
            np.save(
            r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Program\dot_positions_r.npy",
            m)
        else:
            np.save(
                r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Program\dot_positions_l.npy",
                m)
    if game_over:
        if start:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'TEST OVER',
                       red)
        else:
            curTime = time.time()



    print_text(screen, font1, 30, 7, f'Num: {cal_mouse}')
    print_text(screen, font1, 450, 7, f'Level: {division_set}')

    pygame.display.update()





