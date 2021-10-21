>很快，研究生的生活就已经过去了一个多月。在这一个多月的时间里，除了困难难度的学术课程，进度总是推不太动的课题，常常上不去的睡眠质量，以及时好时崩的心态之外，生活中似乎就已经没有什么别的元素了。~~你看这个人，才一个月就醉了，真的是太逊了~~
>因为有些时候，心态实在是太逊了，所以这样下去可不行，~~只好拿去河边烤了~~必须得做点调控。这个时候就想起了《不务正业的日常》这个系列：是时候写点新的好玩的东西了！
>至于具体要写的是什么东西……正好在那几天的时候和同学聊到过俄罗斯方块~~（失败会不断地积累，而成功却总是转瞬即逝）~~，并且也回想起了去年这个时候csapp的老师也提到过这个，所以，就决定是你了……
>至于语言选用，因为本人使用的编程语言相对较少，所以就按照惯例，继续使用Python……

# 编写思路（初步设想）

## 类的划分

关于这个项目，在建立好文件夹后，最开始想到的事就是类的划分

俄罗斯方块可以有哪些类？对于这个问题，脑袋里面第一个蹦出来的就是“方块类”：在整个游戏界面中，主要内容就是这样的方块一直往下掉，然后再进行各种相应的操作。与之对应的便是“游戏界面类”，此类应该包括各种游戏机制的判断，游戏状态的变换，以及对方块的各种使用

初步设想出的类图如下所示：

![](/home/caimx/codes/20210930_001_tetris/类图.png)

## 方块类

### 基本属性

方块类具有的基本属性包括在游戏中的所处位置，方块对应的矩阵大小，当前方块所处的旋转状态，方块最大能达到的旋转状态（主要用于只旋转一次的长条），顺时针还是逆时针旋转，方块的名字和方块的形状（方块的形状是由矩阵表示的，用空字符和字母表示方块的图像）

### 方法

方块本身具有旋转的功能，作用实际上就是让自己做一次矩阵旋转

另一方面，方块还具有获取自身高度的方法，这将有利于在游戏中判断下落的方块是否超出了上边界（是否游戏结束）

## 游戏界面类

### 基本属性

游戏界面类主要是要保存当前的方块堆积情况的，这个利用二维数组存储即可，在数组中，空字符表示没有方块，各种不同的字符表示不同种类的方块

除了保存方块堆积的情况，还应该再单独保存当前正在下落的那个方块，这样隔离出来将有利于方块的移动以及判断各种碰撞

### 方法

方法包括切换到下一个方块，左右移动方块，向下移动一次，将方块固定到方块堆积的数组中，直接向下移动到底，检查是否游戏结束，游戏结束时触发的事件，检查是否有被填满的行，删除被填满的行，刷新界面，绘制界面，旋转当前的方块和检测对方块的一个操作是否合法（假设方块接下来如期发生相应的变换，把这个变换后的形态放到数组中，看看是否会有重叠的现象）

# 代码实现

## 方块类

首先是从方块类开始实现的。在方块类初始化的时候，主要是要定义这个方块的形状，大小，和旋转的相关属性。位置信息在游戏界面类的相应方法中再进行确定：

```python
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
```

而方块的旋转就是很简单的矩阵旋转了：

```python
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
```

获取自身的高度时，需要注意排除底层和顶层的空行所带来的影响：

```python
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
```

由此便完成了方块类的编写

## 游戏界面类

初始化游戏界面时，生成数组，并生成第一个方块：

```python
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
```

方块的横向位置是随机产生的，这样更增加了游戏的随机性

方块左右移动时，需要判断是否被卡住或出界，这样的判断统一交给一个函数isCrash进行，在这里只需要对其进行调用即可：

```python
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
```

方块向下滑动一格的判断方式同理，只不过要注意判断有没有滑到底，滑到底后还要判断是否游戏结束：

```python
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
```

方块在滑到底后，就可以将其固定住了：

```python
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
```

游戏中应该还有一个功能：直接将方块一次性滑到最底部：

```python
def downImm(self):
    """
        直接将方块下滑到底
    """
    while(self.slide()):
        pass
```

关于判读游戏是否结束，只要检查当前操作的方块顶部是否超出了游戏的上边界：

```python
def checkIfFail(self):
    """
        检查是否游戏结束
    """
    if(self.currentBlock.posY - self.currentBlock.getHeight() + 1 <= 0):
        return True
    else:
        return False
```

游戏结束后，置状态变量为0，表示游戏未在运行：

```python
def gameOver(self):
    """
        游戏结束
    """
    print("gameOver!")
    self.state = 0
```

关于如何检查有哪些行被填满，以及删除指定的行号，只涉及到对堆积数组的简单操作：

```python
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
```

方块旋转，同样只要判断是否能转即可：

```python
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
```

在前面一直被调用的，判断方块移动（或）变换是否非法的方法。这个方法耗费的时间最长，因为涉及到了很多种情况的判断，以及坐标的计算。感觉一半的时间都花在了这上面……

```python
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
```

## 主循环

有了前面的两个类，只要写一个游戏循环就可以运行了。循环的逻辑很简单，就是隔一段时间方块自动下滑一次，如果玩家按下了特定的按键就会触发特定的操作，游戏结束后弹出相应信息并退出游戏。在这里使用的是pygame来作为图形界面：

```python
def startGame():
    pygame.init()
    st = Stage()
    pixelPerGrid = 50
    edgeSize = 10
    width = pixelPerGrid * st.STAGE_X + 2 * edgeSize
    height = pixelPerGrid * st.STAGE_Y + 2 * edgeSize
    screen = pygame.display.set_mode((width, height))
    i = 0
    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_a):
                    st.move(0)
                elif(event.key == pygame.K_d):
                    st.move(1)
                elif(event.key == pygame.K_w):
                    st.rotate()
                elif(event.key == pygame.K_s):
                    st.downImm()
        # 判断是否消除某一行
        rows = st.checkFullRow()
        for eachRow in rows:
            st.deleteRow(eachRow)
        # 500ms下滑一格
        if(i >= 500 / 10):
            st.slide()
            i = 0
        # 重新绘制画面
        st.drawInPygame(screen, pixelPerGrid, edgeSize)
        pygame.time.delay(10)
        i += 1
        pygame.display.update()
        # 游戏结束，停下来
        if(st.state == 0):
            print("score: %d" % st.score)
            result = tkinter.messagebox.showinfo(title = '游戏结束！',message='得分：%d' % st.score)
            exit(0)
```

至此，简易的俄罗斯方块便完成了

# 成果展示



# 总结

本次写程序总计花费了两次~~天文编程与软件~~Ubuntu基础教学课程（四节连上）+一个下午的时间（PS：旁边的大佬总共只用了四节课就完成了……），速度还是有些慢的。感觉目前还是没有摸清游戏编程的核心逻辑，还有很大的优化空间……

# 代码链接

https://github.com/VtaSkywalker/20210930_001_tetris

