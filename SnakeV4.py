import time
from tkinter import *
from tkinter import messagebox

import numpy as np
import pandas as pd


class Board:
    def __init__(self):
        # Initialize Variables
        try:
            self.df = pd.DataFrame(data=pd.read_csv(r'SnakeSave.csv'))
        except:
            self.df = pd.DataFrame({'Score': [0] * 10, 'Name': ['Empty'] * 10})
            self.df.to_csv(r'SnakeSave.csv')
        self.delGridBack = []
        self.size = 60; #Default = 100
        self.gridWidth = 2;
        self.bestScore = self.df['Score'][0]
        self.moveNum = 0
        self.scoreSave = 2
        self.score = 3
        self.root = Tk()
        self.screenW = self.root.winfo_screenwidth()
        self.screenH = self.root.winfo_screenheight()
        # self.r = (self.screenH - 150) // 100
        self.r = (self.screenH - 150) // self.size
        # self.c = self.screenW // 100
        self.c = self.screenW // self.size
        self.board = np.array([[0 for i in range(self.c)] for j in range(self.r)])
        self.rSnake = []
        self.cSnake = []
        self.rcSnake = []
        self.rFood = []
        self.cFood = []
        self.loss = 0
        self.origin()
        self.direction = 'right'
        # self.bgColor = "white"
        self.bgColor = "#888888"
        self.fgColor = "Black"
        # self.fgColor = "#404040"
        # self.font = "Nirmala UI bold"
        self.font = "Helvetica Neue Bold"

        # Declared Spectrum Color Vals
        self.redNum = 30
        self.greenNum = 100
        self.blueNum = 200
        self.redVar = 6
        self.greenVar = 12
        # self.blueVar = -21
        self.blueVar = 0
        self.spectrumNum = []
        for i in range(7):
            self.spectrumColor()

        # Tkinter
        self.root.configure(background=self.bgColor)
        self.width = self.size * self.c
        # self.width = 100 * self.c
        self.height = self.size * self.r
        # self.height = 100 * self.r
        self.widthCenter = int(self.screenW / 2 - self.width / 2)
        self.heightCenter = int(self.screenH / 2.3 - self.height / 2)
        geoNum = str(self.width) + "x" + str(self.height + 130) + "+" + str(self.widthCenter) \
                 + "+" + str(self.heightCenter)
        self.root.attributes("-fullscreen", True)
        self.root.geometry(geoNum)
        self.root.focus_force()
        self.root.title("Snake")
        self.borderWidth = 2
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background=self.bgColor,
                             highlightbackground=self.bgColor)
        self.setUI()

        # key bindings
        self.root.bind('<Left>', self.left)
        self.root.bind('<Right>', self.right)
        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.down)
        self.root.bind('<a>', self.left)
        self.root.bind('<d>', self.right)
        self.root.bind('<w>', self.up)
        self.root.bind('<s>', self.down)
        self.root.bind('<Escape>', self.escape)

        timeStart = time.time()
        while self.loss == 0:

            self.move()
            self.setUI()

            timeDif = time.time() - timeStart
            # print(timeDif)
            try:
                time.sleep(.1 - timeDif)
            except:
                pass
            timeStart = time.time()

        self.scoreboard()

    def gridBack(self, rIndex, cIndex):
        # self.canvas.delete(self.delGridBack)
        self.delGridBack = self.canvas.create_rectangle(self.gridWidth + self.size * cIndex,
                                                        self.gridWidth + self.size * rIndex,
                                                        self.size - self.gridWidth + self.size * cIndex,
                                                        self.size - self.gridWidth + self.size * rIndex,
                                                        outline=self.fgColor, fill="#000000",
                                                        width=self.borderWidth)

    def gridSnake(self, rIndex, cIndex, colorIndex):
        self.canvas.create_rectangle(self.gridWidth + self.size * cIndex, self.gridWidth + self.size * rIndex,
                                     self.size - self.gridWidth + self.size * cIndex,
                                     self.size - self.gridWidth + self.size * rIndex, outline=self.fgColor,
                                     fill=self.spectrumNum[-colorIndex - 1],
                                     width=self.borderWidth)

    def gridFood(self, rIndex, cIndex):
        self.canvas.create_rectangle(self.gridWidth + self.size * cIndex, self.gridWidth + self.size * rIndex,
                                     self.size - self.gridWidth + self.size * cIndex,
                                     self.size - self.gridWidth + self.size * rIndex,
                                     outline=self.fgColor, fill="#ff0909", width=self.borderWidth)

    def titleWidget(self):
        titleLabel = Label(self.root, text="Snake", fg=self.fgColor, background=self.bgColor)
        titleLabel.config(font=(self.font, 70))
        titleLabel.grid(row=0, column=1)

    def scoreWidget(self):
        scoreLabel = Label(self.root, text="Score: " + str(self.scoreSave), fg=self.fgColor,
                           background=self.bgColor)
        scoreLabel.config(font=(self.font, 50))
        scoreLabel.grid(row=0, column=0, sticky="S")

    def rightWidget(self):
        rightLabel = Label(self.root, text="Best: " + str(self.bestScore), fg=self.fgColor,
                           background=self.bgColor)
        rightLabel.config(font=(self.font, 50))
        rightLabel.grid(row=0, column=2, sticky="S")

    def setUI(self):  # (Not Bad)
        self.canvas.delete("all")
        for rIndex, r in enumerate(self.board, start=0):
            for cIndex, c in enumerate(r, start=0):
                if self.board[rIndex][cIndex] == 0:
                    self.gridBack(rIndex, cIndex)
                if self.board[rIndex][cIndex] == 1:
                    i = self.rcSnake.index([rIndex, cIndex])
                    self.gridSnake(rIndex, cIndex, i)
                if self.board[rIndex][cIndex] == 2:
                    self.gridFood(rIndex, cIndex)
        # Makes tkinter grid same width throughout
        if self.score != self.scoreSave:
            self.scoreSave = self.score
            self.scoreWidget()
            self.rightWidget()
        if self.moveNum == 0:
            self.root.grid_columnconfigure((0, 1, 2), weight=1, uniform="fred")
            self.rightWidget()
            self.titleWidget()
            self.canvas.grid(row=1, column=0, columnspan=3)
        self.root.update()

    def messageBoxFunc(self):
        x = messagebox.askyesno("You Lost", "You got a score of " +
                                str(self.scoreSave) + ". \nWould you like to play again?")
        if x == 0:
            sys.exit()
        else:
            self.root.destroy()
            main()

    def scoreboard(self):
        newNameLabel = []

        def submitText(event):
            textInput = newNameLabel.get()
            TopNames[newIndex] = textInput
            df = pd.DataFrame({'Score': TopScores, 'Name': TopNames})
            df.to_csv(r'SnakeSave.csv')
            self.messageBoxFunc()

        TopScores = self.df['Score'].values.tolist()
        TopNames = self.df['Name'].values.tolist()
        newIndex = 10000
        for iIndex, I in enumerate(TopScores):
            if self.score > I:
                TopScores.insert(iIndex, self.score)
                TopNames.insert(iIndex, "PlaceHolder")
                TopScores.pop(len(TopScores) - 1)
                TopNames.pop(len(TopNames) - 1)
                newIndex = iIndex
                break
        if newIndex == 10000:
            self.messageBoxFunc()
        else:
            scoreWindow = Toplevel()
            scoreWindow.title("New High Score")
            scoreWindow.grid_columnconfigure((0, 1, 2), weight=1, uniform="fred")
            scoreWindow.configure(background=self.bgColor)
            titleLabel = Label(scoreWindow, text="Leaderboards", fg=self.fgColor, background=self.bgColor)
            titleLabel.config(font=(self.font, 40))
            titleLabel.grid(row=0, column=0, columnspan=3)
            for iIndex, i in enumerate(TopScores):
                scoreLabel = Label(scoreWindow, text=str(i), fg=self.fgColor, background=self.bgColor)
                scoreLabel.config(font=(self.font, 20))
                scoreLabel.grid(row=iIndex + 1, column=0)
                if iIndex == newIndex:
                    newNameLabel = Entry(scoreWindow, width=12, fg=self.fgColor, background=self.bgColor,
                                         justify=CENTER)
                    newNameLabel.config(font=(self.font, 20))
                    newNameLabel.grid(row=iIndex + 1, column=1, columnspan=2)
                    newNameLabel.focus()
                    scoreWindow.bind('<Return>', submitText)
                else:
                    nameLabel = Label(scoreWindow, text=str(TopNames[iIndex]), fg=self.fgColor,
                                      background=self.bgColor)
                    nameLabel.config(font=(self.font, 20))
                    nameLabel.grid(row=iIndex + 1, column=1, columnspan=2)
            scoreWindow.update()
            scoreWindowHeight = scoreWindow.winfo_height()
            scoreWindowWidth = scoreWindow.winfo_width()
            scoreWindowWidthCenter = int(self.screenW / 2 - scoreWindowWidth / 2)
            scoreWindowHeightCenter = int(self.screenH / 2 - scoreWindowHeight / 2)
            geoNum = str(scoreWindowWidth) + "x" + str(scoreWindowHeight) + "+" + str(scoreWindowWidthCenter) \
                     + "+" + str(scoreWindowHeightCenter)
            scoreWindow.geometry(geoNum)
            scoreWindow.lift()
            scoreWindow.mainloop()

    # Places food randomly on board (Optimized)
    def food(self, num=1):
        for i in range(num):
            self.rFood = round(np.random.uniform(0, self.r - 1))
            self.cFood = round(np.random.uniform(0, self.c - 1))
            while self.board[self.rFood][self.cFood] != 0:
                self.rFood = round(np.random.uniform(0, self.r - 1))
                self.cFood = round(np.random.uniform(0, self.c - 1))
            self.board[self.rFood][self.cFood] = 2

    # Places snake in middle of board at start 0 (Optimized
    def origin(self):
        self.rHead = int(round((self.r - 1) / 2))
        self.cHead = int(round((self.c - 1) / 2))
        for i in range(-2, 1):
            self.rSnake.append(self.rHead)
            self.cSnake.append(self.cHead + i)
            self.rcSnake.append([self.rHead, self.cHead + i])
        self.food(4)

    # Moves snake in direction (Optimized)
    def move(self):
        self.moveNum += 1
        move = self.direction
        self.lastDirection = move
        if move == 'left':
            self.cHead -= 1
            if self.cHead == -1:
                self.cHead = self.c - 1
        if move == 'right':
            self.cHead += 1
            if self.cHead == self.c:
                self.cHead = 0
        if move == 'down':
            self.rHead += 1
            if self.rHead == self.r:
                self.rHead = 0
        if move == 'up':
            self.rHead -= 1
            if self.rHead == -1:
                self.rHead = self.r - 1
        # Adjusts List of snake places
        self.rSnake.append(self.rHead)
        self.cSnake.append(self.cHead)
        self.rcSnake.append([self.rHead, self.cHead])

        if self.board[self.rHead][self.cHead] == 0:
            self.board[self.rSnake[0]][self.cSnake[0]] = 0
            self.rSnakeEnd = self.rSnake[0]
            self.cSnakeEnd = self.cSnake[0]
            del (self.rSnake[0])
            del (self.cSnake[0])
            del (self.rcSnake[0])
        elif self.board[self.rHead][self.cHead] == 1:
            self.loss = 1
            # Updates Board
            del (self.rSnake[-1])
            del (self.cSnake[-1])
            del (self.rcSnake[-1])
        else:
            self.food()

        # Set Initial Board
        self.board[self.rHead][self.cHead] = 1
        self.score = len(self.rSnake)
        if self.score > self.bestScore:
            self.bestScore = self.score
        self.spectrumColor()
        self.moveNum += 1

    # Makes rainbow snake
    def spectrumColor(self):
        self.redNum += self.redVar
        self.greenNum += self.greenVar
        self.blueNum += self.blueVar
        if self.redNum > 255:
            self.redVar *= -1
            self.redNum += self.redVar
        if self.redNum < 0:
            self.redVar *= -1
            self.redNum += self.redVar
        if self.greenNum > 255:
            self.greenVar *= -1
            self.greenNum += self.greenVar
        if self.greenNum < 0:
            self.greenVar *= -1
            self.greenNum += self.greenVar
        if self.blueNum > 255:
            self.blueVar *= -1
            self.blueNum += self.blueVar
        if self.blueNum < 0:
            self.blueVar *= -1
            self.blueNum += self.blueVar
        self.redNum = int(self.greenNum / 2)  # Temp

        self.spectrumNum.append('#%02x%02x%02x' % (self.redNum, self.greenNum, self.blueNum))

    # Takes arrow inputs
    def left(self, event):
        if self.lastDirection != 'right':
            self.direction = 'left'

    def right(self, event):
        if self.lastDirection != 'left':
            self.direction = 'right'

    def up(self, event):
        if self.lastDirection != 'down':
            self.direction = 'up'

    def down(self, event):
        if self.lastDirection != 'up':
            self.direction = 'down'

    def escape(self, event):
        self.root.destroy()


def main():
    Board()


if __name__ == "__main__":
    main()
