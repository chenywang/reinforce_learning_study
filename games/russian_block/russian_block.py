# -*- coding: utf-8 -*-
# 俄罗斯方块
import pygame
import random
import time
from pygame.locals import *

from config.config import PROJECT_PATH

pygame.init()
# pygame.key.set_repeat(1, 100)    #重复输入模式
# 窗口
screen = pygame.display.set_mode((660, 520), 0, 32)

image_path = PROJECT_PATH + '/games/russian_block/'

# 静态界面（背景、色块等）
interface = pygame.image.load(image_path + 'interface.jpg').convert()
gameover = pygame.image.load(image_path + 'GAME_OVER.jpg').convert()

# 方块名称、颜色、初始位置
squares_dict = {0: 'z_left', 1: 'z_right', 2: 'long', 3: 'cross', 4: 'rect', 5: 'l_left', 6: 'l_right'}
'''color_dict用于实例化的时候生成颜色标记'''
color_dict = {'z_left': 1, 'z_right': 2, 'long': 3, 'cross': 4, 'rect': 5, 'l_left': 6, 'l_right': 7}
'''color_sheet用于表示颜色标记对应的颜色RGB'''
color_sheet = {1: (231, 63, 136), 2: (192, 219, 64), 3: (168, 201, 206), 4: (143, 111, 161), 5: (254, 252, 66),
               6: (59, 140, 170), 7: (249, 159, 15)}
init_pos_dict = {'z_left': [(4, 1), (5, 1), (5, 2), (6, 2)],
                 'z_right': [(7, 1), (6, 1), (6, 2), (5, 2)],
                 'long': [(4, 2), (5, 2), (6, 2), (7, 2)],
                 'cross': [(5, 1), (6, 1), (7, 1), (6, 2)],
                 'rect': [(5, 1), (6, 1), (5, 2), (6, 2)],
                 'l_left': [(4, 1), (5, 1), (6, 1), (6, 2)],
                 'l_right': [(7, 1), (6, 1), (5, 1), (5, 2)]}


# 碰撞检测系统(装饰器，对squares类内的方法进行装饰）
def pp_test(cls):
    class new_class:
        def __init__(self, name, color, now_pos, flag, stop_flag):
            self.wrapper = cls(name, color, now_pos, flag, stop_flag)
            self.name = self.wrapper.name
            self.color = self.wrapper.color
            self.now_pos = self.wrapper.now_pos
            self.flag = self.wrapper.flag
            self.stop_flag = self.wrapper.stop_flag

        def TURN(self):
            temp = self.wrapper.now_pos
            temp1 = self.wrapper.flag
            self.wrapper.TURN()
            for i in self.wrapper.now_pos:
                if area[i[1]][i[0]] == 1:
                    self.wrapper.now_pos = temp
                    self.wrapper.flag = temp1
            self.now_pos = self.wrapper.now_pos
            self.flag = self.wrapper.flag

        def LEFT(self):
            temp = self.wrapper.now_pos
            self.wrapper.LEFT()
            for i in self.wrapper.now_pos:
                if area[i[1]][i[0]] == 1:
                    self.wrapper.now_pos = temp
            self.now_pos = self.wrapper.now_pos

        def RIGHT(self):
            temp = self.wrapper.now_pos
            self.wrapper.RIGHT()
            for i in self.wrapper.now_pos:
                if area[i[1]][i[0]] == 1:
                    self.wrapper.now_pos = temp
            self.now_pos = self.wrapper.now_pos

        def DOWN(self):
            temp = self.wrapper.now_pos
            self.wrapper.DOWN()
            for i in self.wrapper.now_pos:
                if area[i[1]][i[0]] == 1:
                    self.wrapper.now_pos = temp
                    self.wrapper.stop_flag = 1
            self.now_pos = self.wrapper.now_pos
            self.stop_flag = self.wrapper.stop_flag

    return new_class


# 方块系统
@pp_test  # 碰撞检测装饰器
class squares:
    def __init__(self, name, color, now_pos, flag, stop_flag):
        self.name = name
        self.color = color
        self.now_pos = now_pos
        self.flag = flag
        self.stop_flag = stop_flag

    # 方块的旋转操作
    def TURN(self):
        global now_pos
        now_pos = self.now_pos
        # z_left的两种状态
        if self.name == 'z_left':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (2, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (1, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (0, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, 0)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[2][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (-2, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (-1, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (1, 0)
                self.flag -= 1
        # z_right的两种状态
        elif self.name == 'z_right':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (-2, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (-1, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (0, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (1, 0)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[2][0] == 10:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (-1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (2, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (1, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, 0)
                self.flag -= 1
        # long的两种状态
        elif self.name == 'long':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (2, -2)
                now_pos[1] = Pos(self.now_pos[1]) + (1, -1)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 0)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, 1)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[2][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (2, 0)
                    self.now_pos = now_pos
                elif now_pos[2][0] == 2:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                elif now_pos[2][0] == 10:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (-1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (-2, 2)
                now_pos[1] = Pos(self.now_pos[1]) + (-1, 1)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 0)
                now_pos[3] = Pos(self.now_pos[3]) + (1, -1)
                self.flag -= 1
        # cross的四种状态
        elif self.name == 'cross':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (1, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (-1, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, -1)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[2][0] == 10:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (-1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (1, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (-1, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (1, -1)
                self.flag += 1
            elif self.flag == 2:
                now_pos[0] = Pos(self.now_pos[0]) + (-1, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (1, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (1, 1)
                self.flag += 1
            elif self.flag == 3:
                if now_pos[2][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (-1, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (1, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, 1)
                self.flag -= 3
        # rect无变化
        elif self.name == 'rect':
            pass
        # l_left的四种状态
        elif self.name == 'l_left':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (2, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (1, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (-1, 0)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[2][0] == 10:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (-1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (1, 2)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 1)
                now_pos[2] = Pos(self.now_pos[2]) + (-1, 0)
                now_pos[3] = Pos(self.now_pos[3]) + (0, -1)
                self.flag += 1
            elif self.flag == 2:
                now_pos[0] = Pos(self.now_pos[0]) + (-2, 0)
                now_pos[1] = Pos(self.now_pos[1]) + (-1, -1)
                now_pos[2] = Pos(self.now_pos[2]) + (0, -2)
                now_pos[3] = Pos(self.now_pos[3]) + (1, -1)
                self.flag += 1
            elif self.flag == 3:
                if now_pos[2][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (-1, -1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (1, 1)
                now_pos[3] = Pos(self.now_pos[3]) + (0, 2)
                self.flag -= 3
        # l_right的四种状态
        elif self.name == 'l_right':
            if self.flag == 0:
                now_pos[0] = Pos(self.now_pos[0]) + (-1, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (1, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (0, -2)
                self.flag += 1
            elif self.flag == 1:
                if now_pos[3][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (-2, 0)
                now_pos[1] = Pos(self.now_pos[1]) + (-1, 1)
                now_pos[2] = Pos(self.now_pos[2]) + (0, 2)
                now_pos[3] = Pos(self.now_pos[3]) + (1, 1)
                self.flag += 1
            elif self.flag == 2:
                now_pos[0] = Pos(self.now_pos[0]) + (1, -2)
                now_pos[1] = Pos(self.now_pos[1]) + (0, -1)
                now_pos[2] = Pos(self.now_pos[2]) + (-1, 0)
                now_pos[3] = Pos(self.now_pos[3]) + (0, 1)
                self.flag += 1
            elif self.flag == 3:
                if now_pos[2][0] == 1:  # 贴墙位移
                    now_pos = Pos(self.now_pos) + (1, 0)
                    self.now_pos = now_pos
                now_pos[0] = Pos(self.now_pos[0]) + (1, 1)
                now_pos[1] = Pos(self.now_pos[1]) + (0, 0)
                now_pos[2] = Pos(self.now_pos[2]) + (-1, -1)
                now_pos[3] = Pos(self.now_pos[3]) + (-2, 0)
                self.flag -= 3
        self.now_pos = now_pos

    # 方块的向左操作
    def LEFT(self):
        now_pos = Pos(self.now_pos) + (-1, 0)
        self.now_pos = now_pos

    # 方块的向右操作
    def RIGHT(self):
        now_pos = Pos(self.now_pos) + (1, 0)
        self.now_pos = now_pos

    # 方块的下降操作
    def DOWN(self):
        now_pos = Pos(self.now_pos) + (0, 1)
        self.now_pos = now_pos


# 虚拟寄存坐标系（对应游戏显示区，边界和有方块的坐标，在area中值为1，无方块为0）坐标转换，返回方块在窗口内的实际位置
area = []
for i in range(25):
    area.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
area.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
'''建立12*26的虚拟坐标系（其中头三行用于存放顶部越界的方块,然后左右下有一圈1，代表边界，此坐标系只存放已经stop的方块）'''


def stop_pos_to_area(obj):
    for i in obj.now_pos:
        area[i[1]][i[0]] = 1  # 方块虚拟坐标系横轴x，纵轴y，存入列表的话，xy需要互换


'''将方块stop时的位置写进area'''


def now_pos_to_temp_area(obj):
    global temp_area
    temp_area = []
    for i in range(25):
        temp_area.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    temp_area.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for i in obj.now_pos:
        temp_area[i[1]][i[0]] = 1


'''将移动中方块的动态位置写进temp_area'''
# 颜色标记系统
'''绘制方块的时候发现没法上颜色，无奈，只能在开一个标记颜色的坐标系'''
stop_color = []
for i in range(25):
    stop_color.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
stop_color.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
'''建立12*26的虚拟坐标系（其中头三行用于存放顶部越界的方块,然后左右下有一圈1，代表边界，此坐标系只存放已经stop的方块）'''


def color_to_stop_color(obj):
    for i in obj.now_pos:
        stop_color[i[1]][i[0]] = obj.color  # 方块虚拟坐标系横轴x，纵轴y，存入列表的话，xy需要互换


'''将方块stop时的颜色写进stop_color'''


def color_to_temp_color(obj):
    global temp_color
    temp_color = []
    for i in range(25):
        temp_color.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    temp_color.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for i in obj.now_pos:
        temp_color[i[1]][i[0]] = obj.color


'''将移动中方块的颜色写进temp_color'''


# 将颜色和位置（方块的状态）存进rect_box
def area_to_rect_box():
    rect_box = []
    c1 = -1
    for i in area:
        c1 += 1
        c2 = -1
        for j in i:
            c2 += 1
            if j == 1 and c1 > 2 and c2 != 0 and c2 != 11 and c1 != 25:  # c1 > 2才开始计入rect_box,头三行不需要画
                rect_box.append((stop_color[c1][c2], (20 * (c2 - 1) + 40, 20 * (c1 - 3) + 40, 20, 20)))
    c3 = -1
    for k in temp_area:
        c3 += 1
        c4 = -1
        for l in k:
            c4 += 1
            if l == 1 and c3 > 2 and c4 != 0 and c4 != 11 and c3 != 25:
                rect_box.append((temp_color[c3][c4], (20 * (c4 - 1) + 40, 20 * (c3 - 3) + 40, 20, 20)))
    return rect_box


'''将area中值为1的坐标(边界除外），转换为实际坐标，并生成rect格式，存入rect_box中'''


# 消除系统
def remove():
    v = -1
    for i in area:
        v += 1
        result = 0
        for j in i:
            result += j
        if result == 12 and v != 25:
            del area[v]
            area.insert(0, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            del stop_color[v]
            stop_color.insert(0, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            global score
            score += 1
            level_just()


# game over系统
def game_over():
    result = 0
    for i in area[2]:
        result += i
    if result > 2:
        global game_over
        game_over = 1


# 方块位置运算系统，用于运算方块的position
class Pos:
    def __init__(self, pos):  # ob_pos = Pos([(x1, y1), (x2,y2), (x3, y3), (x4, y4)])
        self.len = len(pos)
        self.pos = pos

    def __add__(self, pair):
        if type(self.pos[0]) != int:
            return list((self.pos[i][0] + pair[0], self.pos[i][1] + pair[1]) for i in range(self.len))
        else:
            return list((self.pos[0] + pair[0], self.pos[1] + pair[1]))


# 音乐系统

# 计分系统（挂在消除系统里，每次消除的时候score+1)
score = 0

# 计时系统
start_time = time.clock()


def TIME():
    over_time = time.clock()
    used_time = over_time - start_time
    global time_sec, time_min, time_hour
    time_sec = int(used_time % 60)
    time_min = int((used_time // 60) % 60)
    time_hour = int((used_time // 60) // 60)


# 等级系统(挂在消除系统里，每次消除后，计分，判断等级，不同等级速度不同)
level_list = [511, 255, 127, 63, 31]
level = level_list[0]


def level_just():
    global level
    if score < 10:
        level = level_list[0]
    elif score < 20:
        level = level_list[1]
    elif score < 30:
        level = level_list[2]
    elif score < 40:
        level = level_list[3]
    elif score < 50:
        level = level_list[4]


# 下一个方块预览图
surface_z_left = pygame.image.load(image_path + 'surface_z_left.png').convert_alpha()
surface_z_right = pygame.image.load(image_path + 'surface_z_right.png').convert_alpha()
surface_long = pygame.image.load(image_path + 'surface_long.png').convert_alpha()
surface_cross = pygame.image.load(image_path + 'surface_cross.png').convert_alpha()
surface_rect = pygame.image.load(image_path + 'surface_rect.png').convert_alpha()
surface_l_left = pygame.image.load(image_path + 'surface_l_left.png').convert_alpha()
surface_l_right = pygame.image.load(image_path + 'surface_l_right.png').convert_alpha()
next_square = {'z_left': surface_z_left,
               'z_right': surface_z_right,
               'long': surface_long,
               'cross': surface_cross,
               'rect': surface_rect,
               'l_left': surface_l_left,
               'l_right': surface_l_right}

# 动态文字、图形（右侧菜单显示的分数、时间、等级、下一个）
score_font = pygame.font.SysFont('tahoma.ttf', 40)
level_font = pygame.font.SysFont('tahoma.ttf', 40)
time_font = pygame.font.SysFont('tahoma.ttf', 40)


# 画出
def draw(obj, next_name):
    now_pos_to_temp_area(obj)
    color_to_temp_color(obj)
    # 画界面、文字、按钮
    screen.blit(interface, (0, 0))
    score_surface = score_font.render('{0}'.format(score), True, (0, 0, 0))  # 因为分数是动态的，所以每次画之前刷新一遍surface
    screen.blit(score_surface, (300, 100))
    TIME()
    time_surface = time_font.render('{0:0>2}:{1:0>2}:{2:0>2}'.format(time_hour, time_min, time_sec), True, (0, 0, 0))
    screen.blit(time_surface, (480, 100))
    level_surface = level_font.render('{0}'.format(level_list.index(level)), True,
                                      (0, 0, 0))  # 因为等级是动态的，所以每次画之前刷新一遍surface
    screen.blit(level_surface, (480, 340))
    screen.blit(next_square[next_name], (280, 330))
    new_rect_box = area_to_rect_box()
    for i in new_rect_box:
        pygame.draw.rect(screen, color_sheet[i[0]], i[1], 0)
    pygame.display.update()


# 初始化第一个方块
next_name = squares_dict[random.randint(0, 6)]


def main():
    while True:
        global next_name
        this_name = next_name
        next_name = squares_dict[random.randint(0, 6)]
        dynamic_square = squares(this_name, color_dict[this_name], init_pos_dict[this_name], flag=0, stop_flag=0)
        draw(dynamic_square, next_name)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        dynamic_square.LEFT()
                        draw(dynamic_square, next_name)
                    elif event.key == K_RIGHT:
                        dynamic_square.RIGHT()
                        draw(dynamic_square, next_name)
                    elif event.key == K_UP:
                        dynamic_square.TURN()
                        draw(dynamic_square, next_name)
                    elif event.key == K_DOWN:
                        dynamic_square.DOWN()
                        draw(dynamic_square, next_name)
            while int(pygame.time.get_ticks()) & level == 1:  # 每当时间循环到1的时候就下降一格
                dynamic_square.DOWN()
                draw(dynamic_square, next_name)
                break
            if dynamic_square.stop_flag == 1:  # 如果stop_flag = 1，则方块落地，记录位置和颜色，判断是否需要消除，或者GAME OVER，然后跳过本次循环，开始下一方块
                stop_pos_to_area(dynamic_square)
                color_to_stop_color(dynamic_square)
                remove()
                game_over()
                break
        if game_over == 1:
            break
    screen.blit(gameover, (0, 0))
    pygame.display.update()


if __name__ == '__main__':
    main()

'''碰撞检测在TURN时会失效_____bug
l_left在turn时出现bug_____bug（2次了，原因尚不明确）
刚开始的下降不稳定，有时候会一次下降两格_____bug
持续按键还未实现_____func
还没有暂停功能_____func
消除的动画还没有加_____cool
画面贴图还没做_____cool
音乐还没有加_____cool
最高分功能还没有____func
开始界面_____func'''
