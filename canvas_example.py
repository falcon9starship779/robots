#!/usr/bin/python3
from collections import Counter
from re import I
from tkinter import *
from random import randint
from Playground import Playground 
print (type(randint))
W= 40
N= 10


m1= Tk()
w1= Canvas(m1,width=500,height=500)
w1.pack()


#images:
player= PhotoImage(file="/home/tm/praktikum/python/player.ppm")
white= PhotoImage(file="/home/tm/praktikum/python/white.ppm")
wall= PhotoImage(file="/home/tm/praktikum/python/brick2.ppm")
robot= PhotoImage(file="/home/tm/praktikum/python/monster.ppm")

def drawSquare(i,j):
    w1.create_line(i*W,j*W,(i+1)*W,j*W)
    w1.create_line((i+1)*W,j*W,(i+1)*W,(j+1)*W)
    w1.create_line((i+1)*W,(j+1)*W,i*W,(j+1)*W)
    w1.create_line(i*W,j*W,i*W,(j+1)*W)

def drawGrid():
    for i in range(N):
        for j in range(N):
            drawSquare (i,j)

def drawRobot(i,j):
    global playground
    #w1.create_text(i*W+0.5*W,j*W+0.5*W,text="R")
    w1.create_image(i*W,j*W,anchor=NW,image=robot)
    pg.setFigure(i,j,"R")
    drawGrid()

def drawPlayer(i,j):
    global playground
    #w1.create_bitmap ((i+0.5)*W,(j+0.5)*W, bitmap="error")
    w1.create_image(i*W,j*W,anchor=NW,image=player)
    pg.setFigure(i,j,"P") 
    drawGrid()


def drawWall(i,j):
    global playground
    w1.create_image(i*W,j*W, anchor=NW, image=wall)
    pg.setFigure(i,j,"W")
    drawGrid()

def drawBlank(i,j):
    global playground
    #w1.create_text(i*W+0.5*W,j*W+0.5*W, text="x"  )
    img = PhotoImage(file="white.ppm")
    w1.create_image(i*W,j*W, anchor=NW, image=white)
    pg.setFigure(i,j,"B")
    drawGrid()

def initalize(NRobots):
    if NRobots>N*N/4:
        raise Exception(f"error: too many robots: {NRobots}, max allowed is: {N*N/4}")
    global pg
    pg=Playground(N)
    i=randint(0,N-1)
    j=randint(0,N-1)
    drawWall(i,j)
    np=0
    while np<1:
        i=randint(0,N-1)
        j=randint(0,N-1)
        if pg.getFigure(i,j) =="B":    
            drawPlayer(i,j)
            np=np+1
    n=0
    while n<NRobots:
        i=randint(0,N-1)
        j=randint(0,N-1)
        print(i,j)
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
    print("move robots")
    ip,jp=searchPlayerPosition()
    robotsOld=[]
    robotsNew=[]
    for i in range(N):
        for j in range(N):
            if pg.getFigure(i,j)=="R":
                print(f"{i},{j}")
                robotsOld.append([i,j])
                print(robotsOld)
    for [i,j] in robotsOld:
        robotsNew.append(preMoveRobot(i,j,ip,jp))
    for [i,j] in robotsOld:drawBlank(i,j)
    for [i1,j1] in robotsNew:
        print(f"137:{i1},{j1}")
        if pg.getFigure(i1,j1)=="P":gameOver()
        if pg.getFigure(i1,j1)=="R":drawWall(i1,j1)
        if pg.getFigure(i1,j1)=="W":drawWall(i1,j1)
        if pg.getFigure(i1,j1)=="B":drawRobot(i1,j1)


def gameOver():
    print("Game Over")
    #raise Exception("_")###
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
        movePlayer(i,j,i-1,j)
    if K=="KP_8" or K=="8":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i,j-1)
    if K=="KP_6" or K=="6":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j)
    if K=="KP_2" or K=="2":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i,j+1)
    if K=="KP_7" or K=="7":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i-1,j-1)
    if K=="KP_3" or K=="3":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j+1)
    if K=="KP_9" or K=="9":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i+1,j-1)
    if K=="KP_1" or K=="1":
        i,j=searchPlayerPosition()
        movePlayer(i,j,i-1,j+1)
    if K=="KP_5" or K=="5":
        i,j=searchPlayerPosition()
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

    if K=="m":
        moveRobots()
    #print(type(eve))
w1.bind_all('<Key>', keyhandler)





    



#drawRobot(i,j)
initalize(10)
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