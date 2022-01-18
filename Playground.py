#!/usr/bin/python3
class Playground:
    def __init__(self,N) -> None:
        self.N=N
        self.playground=[["B" for j in range (N)]for i in range (N)]
    """
    put the character c into line i column 
    """
    def setFigure(self,i,j,c):
        self.playground[j][i]=c
    
    def getFigure(self,i,j):
        return self.playground[j][i] 

    def printPlayground(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.playground [j][i]+", ",end="")
            print("") #linebreak

