#!/usr/bin/python3
from cProfile import label
from collections import Counter
from re import I
from tkinter import *
from random import randint
from Playground import Playground 
print (type(randint))
W= 40
N= 10


m1= Tk()
p1 = PanedWindow(m1,orient=HORIZONTAL)
p1.pack(fill=BOTH, expand=2)
c1= Canvas(p1,width=600,height=500)
p1.add(c1)
overviewPanel=PanedWindow(p1,orient=VERTICAL)
label1=Label(overviewPanel, text="Left Panel", bg="#edbc95")
levelLabel=Label(p1, text="Level:0", bg="#fffc8a")
highscoreStr=StringVar()
highscoreStr.set("Highscore:0")
highscoreLabel=Label(p1, textvariable=highscoreStr, bg="#ff4141")
overviewPanel.add(highscoreLabel)
overviewPanel.add(levelLabel)
overviewPanel.add(label1)
p1.add(overviewPanel)

highscore=0
level=0

#images:
player= PhotoImage(file="player.ppm")
white= PhotoImage(file="white.ppm")
wall= PhotoImage(file="brick2.ppm")
robot= PhotoImage(file="monster.ppm")

def drawSquare(i,j):
    c1.create_line(i*W,j*W,(i+1)*W,j*W)
    c1.create_line((i+1)*W,j*W,(i+1)*W,(j+1)*W)
    c1.create_line((i+1)*W,(j+1)*W,i*W,(j+1)*W)
    c1.create_line(i*W,j*W,i*W,(j+1)*W)

def drawGrid():
    for i in range(N):
        for j in range(N):
            drawSquare (i,j)

def drawRobot(i,j):
    global playground
    #c1.create_text(i*W+0.5*W,j*W+0.5*W,text="R")
    c1.create_image(j*W,i*W,anchor=NW,image=robot)
    pg.setFigure(i,j,"R")
    drawGrid()

def drawPlayer(i,j):
    global playground
    #c1.create_bitmap ((i+0.5)*W,(j+0.5)*W, bitmap="error")
    c1.create_image(j*W,i*W,anchor=NW,image=player)
    pg.setFigure(i,j,"P") 
    drawGrid()


def drawWall(i,j):
    global playground
    c1.create_image(j*W,i*W, anchor=NW, image=wall)
    pg.setFigure(i,j,"W")
    drawGrid()

def drawBlank(i,j):
    global playground
    #c1.create_text(i*W+0.5*W,j*W+0.5*W, text="x"  )
    img = PhotoImage(file="white.ppm")
    c1.create_image(j*W,i*W, anchor=NW, image=white)
    pg.setFigure(i,j,"B")
    drawGrid()


def initalize():
    global pg, highscore, level
    level=-1 #will be incremented in in initalizeNewLevel()
    highscore=0
    pg=Playground(N)

def initalizeNewLevel():
    global level
    level+=1
    levelLabel["text"]=f"Level:{level}"
    print(f"level:{level}")###
    nRobots=(level+1)*5
    for i in range(N):
        for j in range(N):
            drawBlank(i,j)
            pg.setFigure(i,j,"B")
    i=randint(0,N-1)
    j=randint(0,N-1)
    drawPlayer(i,j)
    #drawPlayer(randint(0,N-1),randint(0,N-1)) #alternative solution for the 3 lines

    n=0
    while n<nRobots:
        i=randint(0,N-1)
        j=randint(0,N-1)
        #print(i,j)
        if pg.getFigure(i,j) =="B":
            drawRobot(i,j)
            n=n+1
    
def movePlayer(i1,j1,i2,j2):
    if i2<0 or i2>9 or j2<0 or j2>9:
        print(f"error: you tried to move out of the field, try another move or teleport")
        return
    if pg.getFigure(i2,j2) !="B": 
        print("error:field is occupied")
        return
    if pg.getFigure(i1,j1)!="P": 
        print(f"error:player is not on ({i1},{j1} {pg.getFigure(i1,j1)})")
        return
    if abs(i1-i2)>1:
        print("error: jumps are not allowed")
        return
    if abs(j1-j2)>1:
        print("error: jumps are not allowed")
        return
    drawPlayer(i2,j2)
    drawBlank(i1,j1)

def isLevelOver():
    for i in range(N):
        for j in range(N):
            if pg.getFigure(i,j)=="R":
                return False
    print("level over")
    return True 

def countRobots():
    count=0
    for i in range(N):
        for j in range(N):
            if pg.getFigure(i,j)=="R":
                count=count+1
    return count
                
            #print("You have won!")

def updateHighscore():
    highscoreStr.set(f"Highscore:{highscore}")

def newLevel():
    if isLevelOver():
        initalizeNewLevel()
        




def searchPlayerPosition():
    for i in range(N):
        for j in range(N):
            if pg.getFigure(i,j)=="P":
                return i,j

def teleport():
    while True: 
        i=randint(0,N-1)
        j=randint(0,N-1)
        if pg.getFigure(i,j) =="B":    
            i1,i2=searchPlayerPosition()
            drawBlank(i1,i2)
            drawPlayer(i,j)
            return

def moveRobots():
    global highscore
    print("move robots")
    ip,jp=searchPlayerPosition()
    for i in range(N):
        for j in range(N):
# move from field0 to field1
# +------+------+
# |field0|field1|   field0 and field1 hold the content before the robot move
# +------+------+
#     ----->            
            field0= pg.getFigure(i,j) # The content of the field at move source.
            if field0[0]=="R": 
                i1,j1=preMoveRobot(i,j,ip,jp)
                field1= pg.getFigure(i1,j1) # The content of the field at move destination.
                if field1=="P":
                    gameOver()
                if field1=="W":
                    highscore+= 1
                    if (len(field0)==1): pg.setFigure(i,j,'B')
                    else: pg.setFigure(i,j,fieldi[1:]) # remove the leading 'R'
                    continue
                if field1=="B":
                    if len(field0)==1: pg.setFigure(i,j,'B')
                    else: pg.setFigure(i,j,field0[1:]) # remove the leading 'R'
                    pg.setFigure(i1,j1,'r') # Lowercase 'r' indicates, that this field is occupied by a robot after its move.
                    continue
                # all other cases: R, Rr, r, rr
                if len(field0)==1: pg.setFigure(i,j,'B')
                else: pg.setFigure(i,j,field0[1:]) # remove the leading 'R'
                pg.setFigure(i1,j1,field1+'r') # we append lowercase r
                continue
    pg.printPlayground() ###
    for i in range(N):
        for j in range(N):
            field= pg.getFigure(i,j)
            if field=='B':
                drawBlank(i,j)
                continue
            if field=='W': # seems to be not necessary
                drawWall(i,j)
                continue
            if field=='P': # seems to be not necessary
                drawPlayer(i,j)
                continue
            if len(field)>1:
                drawWall(i,j)
                highscore+= len(field)
                continue
            if field=='r':
                drawRobot(i,j)
                
    print(f"{highscore}")


def gameOver():
    print(f"Game Over\nhighscore: {highscore}\nlevel:{level}")
    
    # raise Exception("_")###
    exit()


def preMoveRobot(i,j,ip,jp):
    if i==ip: i1=i
    if i>ip: i1=i-1
    if i<ip: i1=i+1
    if j==jp: j1=j
    if j>jp: j1=j-1
    if j<jp: j1=j+1
    return([i1,j1])
    """drawBlank(i,j)
    if playground[i1][j1]=="P": gameOver()
    if playground[i1][j1]=="R": drawWall()
    drawRobot(i1,j1)
    """

def isSafe(i,j):
    x=i
    i=j
    j=x
    for i1 in[i-1,i,i+1]:
        for j1 in[j-1,j,j+1]:
            if j1>=0 and j1<=9 and i1>=0 and i1<=9 and pg.getFigure(i,j)=="R":
                return False
    return True

def safeTeleport():
    print("safe Teleport")
    counter=0
    while True: 
        counter=counter+1
        if counter>2*N*N: 
            print("no safe position found")
            return
        i=randint(0,N-1)
        j=randint(0,N-1)
        if pg.getFigure(i,j) =="B" and isSafe(i,j):
            i1,i2=searchPlayerPosition()
            drawBlank(i1,i2)
            drawPlayer(i,j)
            return

def handlePlayerKey(K):
    if K=="KP_4" or K=="4":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i,j-1)
    if K=="KP_8" or K=="8":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i-1,j)
    if K=="KP_6" or K=="6":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i,j+1)
    if K=="KP_2" or K=="2":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j)
    if K=="KP_7" or K=="7":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i-1,j-1)
    if K=="KP_3" or K=="3":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j+1)
    if K=="KP_9" or K=="9":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i-1,j+1)
    if K=="KP_1" or K=="1":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j-1)
    if K=="KP_5" or K=="5":
        pass # don't move
    if K=="s":
        safeTeleport()
    if K=="t":
        teleport()
    
"""def test1():
    for i in range(0,1):
        for j in range(0,1):
            playground[i][j]="B"
    playground[0][0]="P"
    playground[1][0]="R"
    printplayground()
    print(isSafe(0,0))
"""


playerKeys=[str(i) for i in range(1,10)]+[f"KP_{i}"for i in range(1,10)]+["t","s"]

def keyhandler(eve):
    print(eve.keysym)
    K=eve.keysym
    if K in playerKeys:
        handlePlayerKey(K)
        moveRobots()
        updateHighscore()


    if K=="m":
        moveRobots()
    isLevelOver()
    newLevel()

    #print(type(eve))
c1.bind_all('<Key>', keyhandler)


def testInitialize():
    global N
    N= 5
    initalize()
    for i in range(N):
        for j in range(N):
            drawBlank(i,j)
def test1():
    testInitialize()
    drawPlayer(0,4)
    drawRobot(0,0)
    drawRobot(0,1)
    drawRobot(1,0)
    mainloop()
    exit()

def test2():
    testInitialize()
    drawPlayer(1,4)
    drawRobot(0,0)
    drawRobot(1,0)
    drawRobot(1,1)
    drawRobot(2,0)
    mainloop()
    exit()

def test3():
    testInitialize()
    drawPlayer(1,0)
    drawRobot(0,4)
    drawRobot(1,3)
    drawRobot(1,4)
    drawRobot(2,4)
    mainloop()
    exit()

def test4():
    testInitialize()
    drawPlayer(1,0)
    drawRobot(0,3)
    drawRobot(0,4)
    drawRobot(1,3)
    drawRobot(1,4)
    drawRobot(2,3)
    drawRobot(2,4)
    mainloop()
    exit()
    
def test5():
    testInitialize()
    drawPlayer(1,0)
    drawRobot(0,3)
    drawRobot(0,4)
    drawRobot(1,3)
    drawRobot(1,4)
    drawRobot(2,3)
    drawRobot(2,4)
    drawRobot(4,4)
    mainloop()
    exit()
    
def test6():
    testInitialize()
    drawPlayer(4,0)
    drawRobot(0,3)
    drawRobot(0,4)
    drawRobot(1,3)
    drawRobot(1,4)
    drawRobot(2,3)
    drawRobot(2,4)
    drawRobot(4,4)
    mainloop()
    exit()

def test7():
    testInitialize()
    drawPlayer(2,2)
    for i in range(5):
        drawRobot(0,i)
        drawRobot(4,i)
        drawRobot(i,0)
        drawRobot(i,4)
    mainloop()
    exit()
    
test1()    

    

"""

#drawRobot(i,j)
initalize()
initalizeNewLevel()
print(searchPlayerPosition())
#drawWall(3,3)
pg.printPlayground()
#drawPlayer(2,2)
#drawWall(3,3)
#drawBlank(5,5)
drawGrid()
i,j=searchPlayerPosition()
#movePlayer(i,j,i+2,j+2)
#drawSquare (14,15)

#drawBlank(1,1)

mainloop()
"""
