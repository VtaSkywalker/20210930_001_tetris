from blocks import Block
from stage import Stage
<<<<<<< HEAD
import getch
=======
>>>>>>> 401a3c87250745e3551a64a022ebc68e5452375e

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
<<<<<<< HEAD
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
=======
    for i in range(100):
        st.slide()
>>>>>>> 401a3c87250745e3551a64a022ebc68e5452375e
        st.drawInCmd()
        print(st.currentBlock.posX, st.currentBlock.posY)

if __name__ == "__main__":
    testStage1()
