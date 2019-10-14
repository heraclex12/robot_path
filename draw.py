from graphics import *
import random

def drawPath(list,color,win,height):
    scale=30
    k = 0
    for i in range(len(list) // 2):
        x=(list[k]+1-0.5)*scale
        y=(height+1)*scale-(list[k+1]+1-0.5)*scale
        xLBottom=(list[k]+1-1)*scale
        yLBottom=(height+1)*scale-(list[k+1]+1-1)*scale
        xRTop=(list[k]+1)*scale
        yRTop=(height+1)*scale-(list[k+1]+1)*scale
        xq=Rectangle(Point(xLBottom,yLBottom),Point(xRTop,yRTop))
        xq.setFill(color)
        xq.draw(win)
        k += 2

def drawText(x,y,height,win,text,size):
    scale=30
    x=(x+1-0.5)*scale
    y=(height+1)*scale-(y+1-0.5)*scale
    txt=Text(Point(x,y),text)
    txt.setSize(size)
    txt.setFill(color_rgb(0,0,0))
    txt.draw(win)

def drawGrid(width,height,win):
    a = []
    for i in range(width+1):
        for j in range(height+1):
            a.append(i)
            a.append(j)
    drawPath(a, color_rgb(255, 255, 255), win,height)
    a = []
    for i in range(width + 1):
        a.append(i)
        a.append(0)
        a.append(i)
        a.append(height)
    for i in range(height + 1):
        a.append(width)
        a.append(i)
        a.append(0)
        a.append(i)
    drawPath(a, color_rgb(160, 160, 160), win,height)
    for i in range(width+1):
        drawText(i,0,height,win,str(i),10)
    for i in range(height+1):
        drawText(0,i,height,win,str(i),10)
def reverseArray(_2d):
    list=[]
    index=0
    for i in _2d:

        list.append(_2d[index][0])
        list.append(_2d[index][1])
        index += 1
    return list
def processMaxtrix(_2d):
    list=reverseArray(_2d)
    leng=len(list)
    for i in range(0,leng,2):
        list[i],list[i+1]=list[i+1],list[i]
    return list
def random_color():
    return color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))


