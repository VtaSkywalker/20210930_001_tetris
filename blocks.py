import numpy as np

class Block:
    """
        方块类

        Attributes
        ----------
        posX : int
            方块顶点所位于的x轴位置
        posY : int
            方块顶点所位于的y轴位置
            方块顶点位置定义在左下角
        blockSize : int[][]
            方块的各边边长，第一维度为x，第二维度为y
        rotateState : int
            当前所属旋转状态，0为初始状态
        rotateStateMax : int
            最大的旋转状态，超出此值后回到初始状态
        isRotateClockwise : bool
            是否为顺时针旋转，如为否，则置为逆时针旋转
        name : string
            方块种类的名称
        shape : char[][]
            方块的形状
    """
    NAME_DICT = {0:'square', 1:'triangle', 2:'z-shape', 3:'z-shape-r', 4:'bar', 5:'guai', 6:'shuai', 7:'shuai-r'}
    COLOR_DICT = {'a':(255,255,0), 'b':(255,0,255), 'c':(0,0,255), 'd':(255,0,0), 'e':(0,255,0), 'f':(0,255,255), 'g':(255,255,200), 'h':(200,255,255)}
    MAX_BLOCK_TYPE_ID = len(NAME_DICT) # 方块有多少种

    def __init__(self, typeID):
        """
            初始化方块类

            Parameters
            ----------
            typeID : int
                方块的编码，用此编码来生成不同的方块
        """
        self.rotateState = 0
        if(typeID == 0): # square, 2x2正方形
            self.blockSize = [2, 2]
            self.rotateStateMax = 0
            self.isRotateClockwise = True
            self.shape = np.array([['a', 'a'],
                                    ['a', 'a']])
        elif(typeID == 1): # triangle, 三角形
            self.blockSize = [2, 2]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['b', '\000'],
                                    ['b', 'b']])
        elif(typeID == 2): # z-shape, z型方块
            self.blockSize = [3, 3]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['\000', '\000', '\000'],
                                    ['c', 'c', '\000'],
                                    ['\000', 'c', 'c']])
        elif(typeID == 3): # z-shape-r, 反z型方块
            self.blockSize = [3, 3]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['\000', '\000', '\000'],
                                    ['\000', 'd', 'd'],
                                    ['d', 'd', '\000']])
        elif(typeID == 4): # bar, 长条
            self.blockSize = [4, 4]
            self.rotateStateMax = 1
            self.isRotateClockwise = False
            self.shape = np.array([['\000', 'e', '\000', '\000'],
                                    ['\000', 'e', '\000', '\000'],
                                    ['\000', 'e', '\000', '\000'],
                                    ['\000', 'e', '\000', '\000']])
        elif(typeID == 5): # guai, 拐棍
            self.blockSize = [3, 3]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['\000', 'f', '\000'],
                                    ['f', 'f', 'f'],
                                    ['\000', '\000', '\000']])
        elif(typeID == 6): # shuai, 甩棍
            self.blockSize = [3, 3]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['\000', '\000', '\000'],
                                    ['\000', '\000', 'g'],
                                    ['g', 'g', 'g']])
        elif(typeID == 7): # shuai-r, 反甩棍
            self.blockSize = [3, 3]
            self.rotateStateMax = 3
            self.isRotateClockwise = True
            self.shape = np.array([['\000', '\000', '\000'],
                                    ['h', '\000', '\000'],
                                    ['h', 'h', 'h']])
        self.name = Block.NAME_DICT[typeID]
        self.posX = -1
        self.posY = -1

    def rotate(self):
        """
            通过旋转矩阵的方式旋转方块
        """
        if(self.isRotateClockwise):
            if(self.rotateState == self.rotateStateMax and self.rotateStateMax != 3):
                if(self.rotateStateMax == 0):
                    pass
                elif(self.rotateStateMax == 1):
                    self.shape = np.rot90(self.shape, 1)    
            else:
                self.shape = np.rot90(self.shape, -1)
        else:
            if(self.rotateState == self.rotateStateMax and self.rotateStateMax != 3):
                if(self.rotateStateMax == 0):
                    pass
                elif(self.rotateStateMax == 1):
                    self.shape = np.rot90(self.shape, -1)
            else:
                self.shape = np.rot90(self.shape, 1)
        self.rotateState = self.rotateState + 1 if (self.rotateState != self.rotateStateMax) else 0

    def getHeight(self):
        """
            获取自己当前所占的高度

            Returns
            -------
            height : int
                该方块目前所占高度（相对于pos参考点）
        """
        height = self.blockSize[1]
        for eachLine in self.shape:
            s = ""
            for eachGrid in eachLine:
                s += eachGrid
            if(s == ""):
                height -= 1
            else:
                break
        return height
