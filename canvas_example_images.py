#!/usr/bin/python3
from tkinter import *
W= 30
N= 20

m1= Tk()
w1= Canvas(m1,width=500,height=500)
w1.pack()

def drawSquare(i,j):
    w1.create_line(i*W,j*W,(i+1)*W,j*W)
    w1.create_line((i+1)*W,j*W,(i+1)*W,(j+1)*W)
    w1.create_line((i+1)*W,(j+1)*W,i*W,(j+1)*W)
    w1.create_line(i*W,j*W,i*W,(j+1)*W)

def drawRobot(i,j):
    w1.create_text(i*W+0.5*W,j*W+0.5*W,text="R")

def drawPlayer(i,j):
    #w1.create_bitmap ((i+0.5)*W,(j+0.5)*W, bitmap="error")
    img = PhotoImage(file="bot_andro.ppm.")
    w1.create_image(i*W,j*W, anchor=NW, image=img)
def drawWall(i,j):
    img = PhotoImage(file="cube1.ppm")
    w1.create_image(i*W,j*W, anchor=NW, image=img)
    w1.create_image(0,0, anchor=NW, image=img)
def drawBlank(i,j):
    #w1.create_text(i*W+0.5*W,j*W+0.5*W, text="x"  )
    img = PhotoImage(file="white.ppm")
    w1.create_image(i*W,j*W, anchor=NW, image=img)
    w1.create_image(0,0, anchor=NW, image=img)


for i in range(N):
    for j in range(N):
        drawSquare (i,j)
drawRobot(5,5)
drawBlank(5,5)
drawRobot(0,0)
drawPlayer(5,5)
"""drawWall(4,4)
"""#drawSquare (14,15)

drawBlank(1,1)

mainloop()

