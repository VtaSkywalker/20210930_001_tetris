from blocks import Block
from stage import Stage
import getch

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
    st = Stage()
    st.drawInCmd()
    while(True):
        inputCh = getch.getch()
        if(inputCh == "a"):
            st.move(0)
        elif(inputCh == "d"):
            st.move(1)
        elif(inputCh == 'w'):
            st.rotate()
        elif(inputCh == 's'):
            st.downImm()
        else:
            st.slide()
        st.drawInCmd()
        print(st.currentBlock.posX, st.currentBlock.posY)

if __name__ == "__main__":
    testStage1()
