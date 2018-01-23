#請先安裝pypiwin32套件
import time
import win32gui
import os
from tkinter import *

Width = 900
Height = 900
Duration = 1 / 240
DisplayFrequency = 2
BarLocation = Height * 5 / 6
Speed = 3

TotalBrickX = 8
TotalBrickY = 6

BrickLength = 60
BrickHeight = 23

class Ball:
    def __init__(self, canvas, x, y, radius = 7, color = 'red'):
        self.speed = Speed
        self.canvas = canvas
        self.id = self.canvas.create_oval(x, y, x + radius * 2, y + radius * 2, fill = color)
        self.xDirection = 0
        self.yDirection = self.speed
        self.radius = radius

    def move(self, barV, barXLeft, barXRight, bricks):
        position = self.canvas.coords(self.id)
        if position[1] <= 0:
            self.yDirection *= -1
        elif position[3] > Height:
            lose = GameOver(self.canvas)
            lose.gameOver('~~您失敗了!再接再厲...!~~')
        elif position[1] <= BarLocation + self.radius and position[3] >= BarLocation - self.radius:
            xLoc = (position[0] + position[2]) / 2
            if xLoc >= barXLeft and xLoc <= barXRight and self.yDirection > 0:
                self.xDirection += barV
                if abs(self.xDirection)  >= self.speed:
                    if self.xDirection > 0:
                        self.xDirection = self.speed - 1
                    else:
                        self.xDirection = -self.speed + 1
                self.yDirection = -(self.speed ** 2 - self.xDirection ** 2) ** (1/2)
        if position[0] <= 0 or position[2] > Width:
            self.xDirection *= -1
        #碰到磚塊的判斷及處理
        for brick in bricks:
            result = brick.isCollideed(position)
            if result != -1:
                if result == 0:
                    self.xDirection = -1 * abs(self.xDirection)
                elif result == 1:
                    self.yDirection = -1 * abs(self.yDirection)
                elif result == 2:
                    self.xDirection = abs(self.xDirection)
                elif result == 3:
                    self.yDirection = abs(self.yDirection)
                bricks.remove(brick)

        if bricks.__len__() == 0:
            win = GameOver(self.canvas)
            win.gameOver('~~恭喜獲勝...!~~')
            
        self.canvas.move(self.id, self.xDirection, self.yDirection)

class Bar:
    def __init__(self, canvas, x, y, length = Width / 4, height = 2, color ='black'):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle((Width - length) / 2, y - height / 2, (Width + length) / 2, y + height / 2, fill = color)
        self.length = length
    def move(self, x):
        v = x - self.canvas.coords(self.id)[0] - self.length / 2
        self.canvas.move(self.id, v, 0)
        return v

    def getLocation(self):
        return self.canvas.coords(self.id)

class GameOver:
    def __init__(self, canvas):
        self.canvas = canvas

    def gameOver(self, text, color = 'red'):
        self.canvas.create_text(Width / 2, Height / 2, text = text, fill = color, font={'Times New Roman', 70})
        self.canvas.bind_all('<KeyPress>', self.exitDelegate)
        self.canvas.bind_all('<Button-1>', self.exitDelegate)
        while(True):
            self.canvas.update();
            time.sleep(Duration);

    def exitDelegate(self, evt):
        os._exit(0)


class Bricks:
    def __init__(self, canvas, x, y, length = BrickLength, height = BrickHeight, color ='grey'):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x , y, x + length, y + height, fill = color)

    def isCollideed(self, location):
        myLocation = self.canvas.coords(self.id)
        side = -1
        if location[0] <= myLocation[2] and myLocation[0] < location[2] and location[1] <= myLocation[3] and myLocation[1] < location[3]:
            x = (location[0] + location[2]) / 2
            y = (location[1] + location[3]) / 2
            distance = Width + Height
            for i in range(0, 2):
                if abs(x - myLocation[i * 2]) <= distance:
                    side = i * 2
                    distance = abs(x - myLocation[side])
                if abs(y - myLocation[i * 2 + 1]) <= distance:
                    side = i * 2 + 1
                    distance = abs(y - myLocation[side])
            canvas.delete(self.id)
        return side

tk = Tk()
tk.title("打磚塊")
tk.resizable = (0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width = Width, height = Height, bd = 0)
canvas.pack()
canvas.update_idletasks()
ball = Ball(canvas, Width / 2, Height * 3 / 5)
bar = Bar(canvas, Width / 2, BarLocation)
bricks = []
for x in range(TotalBrickX):
    for y in range(TotalBrickY):
        bricks.append(Bricks(canvas, ((Width - (BrickLength + 20) * TotalBrickX)) / 2 + (BrickLength + 20) * x, BrickHeight * 4 + (BrickHeight + 10) * y))

class DelayStart:
    def __init__(self):
        self.start = False
    def gameStart(self, evt):
        self.start = True

delay = DelayStart()
canvas.bind_all('<Button-1>', delay.gameStart)
while delay.start == False:
    canvas.update()
while True:
    canvas.update()
    for i in range(DisplayFrequency):
        mouseX, mouseY = win32gui.GetCursorPos()
        barV = bar.move(mouseX - tk.winfo_x())
        barLoc = bar.getLocation()
        ball.move(barV, barLoc[0], barLoc[2], bricks)
        time.sleep(Duration)