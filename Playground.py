#!/usr/bin/python3
class Playground:
    def __init__(self,N) -> None:
        self.N=N
        self.playground=[[f"({i},{j})" for j in range (N)]for i in range (N)]
    """
    put the character c into line i column 
    """
    def setFigure(self,i,j,c):
        self.playground[i][j]=c
    
    def getFigure(self,i,j):
        return self.playground[i][j] 

    def printPlayground(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.playground [i][j]+", ",end="")
            print("") #linebreak



