#!/usr/bin/python3

i=5.0
print (type(i))
print (i*2)
Thies="Thies Munaf"
i=Thies
print (type(i))
print (i*7)
i=[ 1,[0],2,Thies ]
print (type(i))
print(i*5)
def f(x,y):
    print(x+y) 
    print(y)
f(3*3/2,5)
def f(x):
    print(x*x)
f(2+3)
for i in range(10):
    print(i+1,end=": ")
    f(i)