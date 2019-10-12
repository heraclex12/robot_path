from graphics import *
ratio=30
win=GraphWin("robot_path",23*ratio,19*ratio)
#poly=Polygon(Point(4*10,18*10-4*10),Point(5*30,18*30-9*30),Point(8*30,18*30-10*30),Point(9*30,18*30-5*30))
#poly.setFill(color_rgb(255,0,255))
#line=Line(Point(14*30,18*30-1*30),Point(11*30,18*30-1*30))
#line.setFill(color_rgb(0,255,255))
#poly2=Polygon(Point(8*30,18*30-12*30),Point(8*30,18*30-17*30),Point(13*30,18*30-12*30))
list1=[8,12,8,17,13,12]
list2=[11,1,11,6,14,6,14,1]
list3=[4,4,5,9,8,10,9,5]
path=[2,2,3,3,4,3,5,3,6,3,7,3,8,3,9,4,10,5,10,6,10,7,11,8,12,9,13,10,14,11,15,12,16,13,17,14,18,15,19,16]
path2=[4,4,4,5,4,6,4,7,4,8,5,9,6,9,7,10,8,10,9,9,9,8,9,7,9,6,9,5,8,5,8,5,7,4,6,4,5,4,8,4]
path3=[11,1,11,2,11,3,11,4,11,5,11,6,11,6,12,6,13,6,14,6,14,5,14,4,14,3,14,2,14,1,13,1,12,1]
path4=[8,12,8,13,8,14,8,15,8,16,8,17,9,16,10,15,11,14,12,13,13,12,12,12,11,12,10,12,9,12,8,12]
hang=[1,1,2,1,3,1,4,1]

def drawPath(list):
    k = 0
    for i in range(len(path) // 2):
        txt = Text(Point(path[k] * ratio, 18 * ratio - path[k + 1] * ratio), "x")
        txt.draw(win)
        k += 2
def drawPath2(list,color):
    k = 0
    for i in range(len(list) // 2):
        x=(list[k]+1-0.5)*ratio
        y=19*ratio-(list[k+1]+1-0.5)*ratio
        xLBottom=(list[k]+1-1)*ratio
        yLBottom=19*ratio-(list[k+1]+1-1)*ratio
        xRTop=(list[k]+1)*ratio
        yRTop=19*ratio-(list[k+1]+1)*ratio
        xq=Rectangle(Point(xLBottom,yLBottom),Point(xRTop,yRTop))
        xq.setFill(color)
        xq.draw(win)
        k += 2
def drawPolygan(list):
    k = 0
    for i in range(len(list) // 2 - 1):
        line = Line(Point(ratio * list[k], 18 * ratio - list[k + 1] * 20),Point(ratio * list[k + 2], 18 * ratio - list[k + 3] * ratio))

        line.draw(win)
        k += 2
    line = Line(Point(list[len(list) - 2] * ratio, 18 * ratio - list[len(list) - 1] * ratio),Point(list[0] * ratio, 18 * ratio - list[1] * ratio))
    line.setWidth(ratio)

#x=1-0.5
#y=1-0.5

#x2=2-0.5
#y2=1-0.5
#txt=Text(Point(ratio*x,18*ratio-y*ratio),"x")

#txt=Text(Point(ratio*x2,18*ratio-y2*ratio),"x")

a=[]
for i in range(23):
    for j in range(19):
        a.append(i)
        a.append(j)
drawPath2(a,color_rgb(236,236,236))
a=[]
for i in range(23):
    a.append(i)
    a.append(0)
    a.append(i)
    a.append(18)
for i in range(19):
    a.append(22)
    a.append(i)
    a.append(0)
    a.append(i)
drawPath2(a,color_rgb(160,160,160))
drawPath2(path2,color_rgb(255,0,0))
drawPath2(path,color_rgb(0,0,255))
drawPath2(path3,color_rgb(0,255,0))
drawPath2(path4,color_rgb(220,116,0))

x=(2+1-0.5)*ratio
y=19*ratio-(2+1-0.5)*ratio



txt=Text(Point(x,y),"S")
txt.setSize(20)
txt.setFill(color_rgb(255,255,255))
txt.draw(win)

x=(19+1-0.5)*ratio
y=19*ratio-(16+1-0.5)*ratio



txt=Text(Point(x,y),"G")
txt.setSize(20)
txt.setFill(color_rgb(255,255,255))
txt.draw(win)




#squ=Rectangle(Point(ratio*(x-0.5),18*ratio-(y-0.5)*ratio),Point(ratio*(x+0.5),18*ratio-(y+0.5)*ratio))


#squ=Rectangle(Point(ratio*(x2-0.5),18*ratio-(y2-0.5)*ratio),Point(ratio*(x2+0.5),18*ratio-(y2+0.5)*ratio))



#img=Image(Point(ratio*10,ratio*11),"\Hpzdi9q.gif")

#img=Image(Point(ratio*15,ratio*11),"\Hpzdi9q.gif")




win.getMouse()


win.close()