import pygame
from stage import *
import tkinter
import tkinter.messagebox

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

if __name__ == "__main__":
    while(True):
        startGame()
