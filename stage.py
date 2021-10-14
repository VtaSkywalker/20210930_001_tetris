from numpy.core.numeric import isclose
from numpy.core.shape_base import block
import pygame
from blocks import Block
import numpy as np
import random
import copy
import os

class Stage:
    """
        游戏场景类

        Attributes
        ----------
        grids : char[][]
            用于装填各种方块的矩阵，每种字符表示一种颜色，该字符与方块属性对应
        currentBlock : Block
            当前正在操作的方块
        state : int
            游戏是否正在运行
        score : int
            游戏得分
    """
    STAGE_X = 8 # 地图宽度
    STAGE_Y = 12 # 地图高度

    def __init__(self):
        """
            初始化游戏界面，同时初始化第一个方块
        """
        self.grids = np.zeros((Stage.STAGE_Y+1, Stage.STAGE_X), dtype=str) # 注意到Y轴多了1行，这是为了判断出界
        for eachLine in self.grids:
            for eachGrid in eachLine:
                eachGrid = ""
        self.nextBlock()
        self.state = 1 # 游戏是否正在运行
        self.score = 0 # 游戏分数

    def nextBlock(self):
        """
            生成下一个方块
        """
        self.currentBlock = Block(int(random.random() * Block.MAX_BLOCK_TYPE_ID))
        self.currentBlock.posX = int(random.random() * (Stage.STAGE_X - self.currentBlock.blockSize[0] + 1))
        self.currentBlock.posY = 0

    def move(self, direction):
        """
            左右移动方块

            Parameters
            ----------
            direction : int
                移动方向，0为左，1为右
            
            Returns
            -------
            result : bool
                移动是否成功
        """
        if(direction == 0):
            if(self.isCrash(self.currentBlock.shape, [self.currentBlock.posX-1, self.currentBlock.posY])):
                return False
            else:
                self.currentBlock.posX -= 1
                return True
        elif(direction == 1):
            if(self.isCrash(self.currentBlock.shape, [self.currentBlock.posX+1, self.currentBlock.posY])):
                return False
            else:
                self.currentBlock.posX += 1
                return True

    def slide(self):
        """
            方块向下滑动一格
        """
        if(not self.isCrash(self.currentBlock.shape, [self.currentBlock.posX, self.currentBlock.posY+1])):
            self.currentBlock.posY += 1
            return True
        # 如果不能再往下移动，则应该先检查是否game over，然后（如果没有挂）再切换到下一个方块
        if(self.checkIfFail()):
            self.gameOver()
        self.score += 1 # 没有gameover时，加分
        # 如果没有game over，即可进入下一个方块，在此之前先完成之前那个方块的放置
        self.placeBlock()
        self.nextBlock()
        return False

    def placeBlock(self):
        """
            放置当前方块到grid上
        """
        blockSizeX = self.currentBlock.blockSize[0]
        blockSizeY = self.currentBlock.blockSize[1] 
        for (y, dy) in zip(range(blockSizeY), range(-self.currentBlock.blockSize[1]+1, 1)):
            for (x, dx) in zip(range(blockSizeX), range(0, self.currentBlock.blockSize[0])):
                if(self.currentBlock.shape[y][x] != "" and (self.currentBlock.posY+dy >= 0)): # 注意不要溢出！
                    self.grids[self.currentBlock.posY+dy][self.currentBlock.posX+dx] = self.currentBlock.shape[y][x]

    def downImm(self):
        """
            直接将方块下滑到底
        """
        while(self.slide()):
            pass

    def checkIfFail(self):
        """
            检查是否游戏结束
        """
        if(self.currentBlock.posY - self.currentBlock.getHeight() + 1 <= 0):
            return True
        else:
            return False

    def gameOver(self):
        """
            游戏结束
        """
        print("gameOver!")
        self.state = 0

    def checkFullRow(self):
        """
            检查并返回所有被填满的行

            Returns
            -------
            rows : list
                所有被填满的行
        """
        rows = []
        for (rowIdx, eachRow) in zip(range(Stage.STAGE_Y + 1), self.grids):
            isFull = True
            for eachGrid in eachRow:
                if(eachGrid == ""):
                    isFull = False
                    break
            if(isFull):
                rows.append(rowIdx)
        return rows

    def deleteRow(self, row):
        """
            对指定的行号所在行进行消除

            Parameters
            ----------
            row : int
                指定的那一行的行号
        """
        for Y in range(row-1, 0, -1):
            for X in range(Stage.STAGE_X):
                self.grids[Y+1][X] = self.grids[Y][X]
        for X in range(Stage.STAGE_X):
            self.grids[0][X] = ''
        self.score += 10 # 消除一行加10分

    def refresh(self):
        """
            随帧数刷新
        """
        pass

    def draw(self):
        """
            绘制当前界面
        """
        pass

    def rotate(self):
        """
            旋转方块
        """
        blockCopy = copy.copy(self.currentBlock)
        blockCopy.rotate()
        if(self.isCrash(blockCopy.shape, [blockCopy.posX, blockCopy.posY])):
            return False
        self.currentBlock.rotate()
        return True

    def isCrash(self, shape, pos):
        """
            判断方块移动是否非法

            Parameters
            ----------
            shape : char[][]
                操作后方块的形状
            pos : int[][]
                操作后方块的位置[posX, posY]
        """
        blockSizeX = self.currentBlock.blockSize[0]
        blockSizeY = self.currentBlock.blockSize[1] 
        posX = pos[0]
        posY = pos[1]
        for (y, dy) in zip(range(blockSizeY), range(-self.currentBlock.blockSize[1]+1, 1)):
            for (x, dx) in zip(range(blockSizeX), range(0, self.currentBlock.blockSize[0])):
                if(shape[y][x] != ""):
                    if(not (0 <= posX + dx < Stage.STAGE_X and posY + dy < Stage.STAGE_Y + 1)):
                        return True
                    if(0 <= posX + dx < Stage.STAGE_X and 0 <= posY + dy < Stage.STAGE_Y + 1 and self.grids[posY+dy][posX+dx] != ""):
                        return True
        return False

    def drawInCmd(self):
        """
            在命令窗画出当前界面，用于调试
        """
        os.system("clear")
        totalGrids = copy.copy(self.grids)
        blockSizeX = self.currentBlock.blockSize[0]
        blockSizeY = self.currentBlock.blockSize[1] 
        for (y, dy) in zip(range(blockSizeY), range(-self.currentBlock.blockSize[1]+1, 1)):
            for (x, dx) in zip(range(blockSizeX), range(0, self.currentBlock.blockSize[0])):
                if(Stage.STAGE_Y + 1 > self.currentBlock.posY+dy >= 0 and Stage.STAGE_X > self.currentBlock.posX+dx >= 0): # 剔除负数对显示的影响
                    if(self.currentBlock.shape[y][x] != ""): # 空白的当然不去覆盖原有的了
                        if(self.currentBlock.posY+dy >= 0): # 越界的当然不显示了
                            totalGrids[self.currentBlock.posY+dy][self.currentBlock.posX+dx] = self.currentBlock.shape[y][x]
        for eachLine in totalGrids:
            for eachGrid in eachLine:
                print("%c\t" % (eachGrid if eachGrid else ' '), end="")
            print("")
        print("")

    def drawInPygame(self, screen, pixelPerGrid, edgeSize):
        """
            在pygame界面中画出游戏画面

            screen : pygame中的screen
                游戏界面
            pixelPerGrid : int
                每个方块的像素大小
            edgeSize : int
                游戏界面边框大小
        """
        screen.fill((0,0,0))
        totalGrids = copy.copy(self.grids)
        blockSizeX = self.currentBlock.blockSize[0]
        blockSizeY = self.currentBlock.blockSize[1] 
        for (y, dy) in zip(range(blockSizeY), range(-self.currentBlock.blockSize[1]+1, 1)):
            for (x, dx) in zip(range(blockSizeX), range(0, self.currentBlock.blockSize[0])):
                if(Stage.STAGE_Y + 1 > self.currentBlock.posY+dy >= 0 and Stage.STAGE_X > self.currentBlock.posX+dx >= 0): # 剔除负数对显示的影响
                    if(self.currentBlock.shape[y][x] != ""): # 空白的当然不去覆盖原有的了
                        if(self.currentBlock.posY+dy >= 0): # 越界的当然不显示了
                            totalGrids[self.currentBlock.posY+dy][self.currentBlock.posX+dx] = self.currentBlock.shape[y][x]
        for idx_y, eachLine in zip(range(self.STAGE_Y + 1), totalGrids):
            for idx_x, eachGrid in zip(range(self.STAGE_X), eachLine):
                if(idx_y == 0):
                    continue
                if(eachGrid):
                    pygame.draw.rect(screen, Block.COLOR_DICT[eachGrid], pygame.Rect(idx_x * pixelPerGrid + edgeSize, (idx_y - 1) * pixelPerGrid + edgeSize, pixelPerGrid, pixelPerGrid))
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(idx_x * pixelPerGrid + edgeSize, (idx_y - 1) * pixelPerGrid + edgeSize, pixelPerGrid, pixelPerGrid), width=1)
