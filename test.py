from blocks import Block
from stage import Stage

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
    for i in range(100):
        st.slide()
        st.drawInCmd()
        print(st.currentBlock.posX, st.currentBlock.posY)

if __name__ == "__main__":
    testStage1()
