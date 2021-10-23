from numpy import e
from blocks import Block
from stage import Stage
import pygame

def testBlockRotate():
    for i in range(5):
        b = Block(i)        
        print(0)
        print(b.shape)
        print(b.getHeight())
        for j in range(5):
            b.rotate()
            print(j+1)
            print(b.shape)
            print(b.getHeight())

def testStage1():
    pygame.init()
    st = Stage()
    st.drawInCmd()
    screen = pygame.display.set_mode((320, 240))
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
                st.drawInCmd()
        # 判断是否消除某一行
        rows = st.checkFullRow()
        for eachRow in rows:
            st.deleteRow(eachRow)
        # 500ms下滑一格
        if(i >= 500 / 10):
            st.slide()
            i = 0
        st.drawInCmd()
        pygame.time.delay(10)
        i += 1

if __name__ == "__main__":
    testStage1()
