# -*- coding:utf-8 -*-
import random
from tkinter import *

mine = 100  # 代表地雷
Pro = 20  # 放大比例


class Sweep:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.degree = 100
        self.count = 0
        self.live = True
        self.map = [[0 for col in range(width)] for row in range(height)]
        self.dist = [[0 for col in range(self.width)] for row in range(self.height)]

        for i in range(self.degree):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.map[x][y] = mine

        for row in range(0, width):
            for col in range(0, height):
                if self.map[row][col] != mine:
                    cnt = 0
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            try:
                                if self.map[i][j] == mine and i > -1 and i < width and j > -1 and j < height:
                                    cnt += 1
                            except:
                                continue
                    self.map[row][col] = cnt
        self.SetWindows()

    def SetWindows(self):
        # 设置窗口
        self.w = Tk()
        self.w.title(" 扫雷")
        self.w.resizable(width=False, height=False)

        # 布置画布
        self.c = Canvas(self.w, width=self.width * Pro, height=self.height * Pro, bg='white')
        self.c.place(x=0, y=0)
        self.c.grid(row=0, column=0, sticky=W)

        # 绑定按钮
        self.w.bind("<Button-1>", self.callback1)
        self.w.bind("<Button-3>", self.callback2)
        self.w.bind("<Double-Button>", self.callback3)
        self.showmap()

    def showmap(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.c.create_rectangle(j * Pro, i * Pro, j * Pro + Pro, i * Pro + Pro, \
                                        fill='white', outline='black', width=2, tags=('all'))

    def Death(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.map[i][j] == mine:
                    self.c.create_rectangle(i * Pro, j * Pro, i * Pro + Pro, j * Pro + Pro, \
                                            fill='red', outline='black', width=2, tags=('all'))
                else:
                    self.c.create_rectangle(i * Pro, j * Pro, i * Pro + Pro, j * Pro + Pro, \
                                            fill='gray', outline='black', width=2, tags=('all'))
        self.c.create_text((self.width / 2) * Pro, (self.height / 2) * Pro, text='You Are Death', font=('Times', 35))

    def win(self):
        self.c.create_text((self.width / 2) * Pro, (self.height / 2) * Pro, text='You Are Winner', font=('Times', 35))

    def Blank(self, row, col):
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if x > -1 and x < self.width and y > -1 and y < self.height and self.map[x][y] != mine:
                    self.c.create_rectangle(x * Pro, y * Pro, x * Pro + Pro, y * Pro + Pro, \
                                            fill='gray', outline='black', width=2, tags=('all'))
                    if self.map[x][y] != 0:
                        t = str(self.map[x][y])
                        self.c.create_text(x * Pro + 10, y * Pro + 10, text=t)

    def showzero(self, row, col):
        Q = [0 for col in range(1000)]
        Q[1] = row;
        Q[2] = col
        length = 2

        while length != 0:
            y = Q[length];
            length -= 1
            x = Q[length];
            length -= 1
            # print(length)

            self.Blank(x, y)
            try:
                if x + 1 < self.width and self.map[x + 1][y] == 0 and self.dist[x + 1][y] == 0:
                    length += 1;
                    Q[length] = x + 1
                    length += 1;
                    Q[length] = y
                    self.dist[x + 1][y] = 1

                if x - 1 < self.width and self.map[x - 1][y] == 0 and self.dist[x - 1][y] == 0:
                    length += 1;
                    Q[length] = x - 1
                    length += 1;
                    Q[length] = y
                    self.dist[x - 1][y] = 1

                if y + 1 < self.height and self.map[x][y + 1] == 0 and self.dist[x][y + 1] == 0:
                    length += 1;
                    Q[length] = x
                    length += 1;
                    Q[length] = y + 1
                    self.dist[x][y + 1] = 1

                if y - 1 < self.height and self.map[x][y - 1] == 0 and self.dist[x][y - 1] == 0:
                    length += 1;
                    Q[length] = x
                    length += 1;
                    Q[length] = y - 1
                    self.dist[x][y - 1] = 1
            except:
                continue

    def callback1(self, event):
        if self.live == True:
            x = event.x // Pro;
            y = event.y // Pro
            # print(x,y,self.map[x][y])
            if self.map[x][y] == mine:
                self.c.create_rectangle(x * Pro, y * Pro, x * Pro + Pro, y * Pro + Pro, \
                                        fill='red', outline='black', width=2, tags=('all'))

                self.live = False
                self.Death()
            else:
                if self.map[x][y] != 0:
                    self.c.create_rectangle(x * Pro, y * Pro, x * Pro + Pro, y * Pro + Pro, \
                                            fill='gray', outline='black', width=2, tags=('all'))
                    t = str(self.map[x][y])
                    self.c.create_text(x * Pro + 10, y * Pro + 10, text=t)
                    self.dist[x][y] = 1
                else:
                    self.showzero(x, y)
        if self.count == self.degree:
            self.win()

    def callback2(self, event):
        if self.live == True:
            x = event.x // Pro;
            y = event.y // Pro
            if self.dist[x][y] == 2:
                self.c.create_rectangle(x * Pro, y * Pro, x * Pro + Pro, y * Pro + Pro, \
                                        fill='white', outline='black', width=2, tags=('all'))
                if self.map[x][y] == mine:
                    self.count -= 1
                self.dist[x][y] = 0
            else:
                self.dist[x][y] = 2
                if self.map[x][y] == mine:
                    self.count += 1
                self.c.create_rectangle(x * Pro, y * Pro, x * Pro + Pro, y * Pro + Pro, \
                                        fill='black', outline='black', width=2, tags=('all'))
        if self.count == self.degree:
            self.win()

    def callback3(self, event):
        row = event.x // Pro;
        col = event.y // Pro
        '''#print(row,col)
        for x in range(row-1,row+2):
            for y in range(col-1,col+2):
                if x>-1 and x<self.width and y>-1 and y<self.height:
                    self.c.create_rectangle(x*Pro,y*Pro,x*Pro+Pro,y*Pro+Pro,\
                       fill='green',outline='black',width=2,tags=('all','temp'))
        time.sleep(2)

        cnt = self.c.find_withtag('temp')
        for i in range(0,len(cnt)):
            self.c.delete(cnt[i])'''


def main():
    one = Sweep(20, 20)


if __name__ == "__main__":
    main()
