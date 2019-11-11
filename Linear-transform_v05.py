from tkinter import *

import math
from tkinter import Canvas
import time

panx = 0
pany = 0
panStartx = 0
panStarty = 0
tempPanx = 0
tempPany = 0



#draws the coordinate system
def drawGrid(canvas,scale):
    mainLine = 0.5
    secondaryLine = 0.5
    global panx,pany
    y1 = 400-pany
    y2 = 400-pany
    if(scale>=3):
        mainLine = 1.5
    while y1 <= 800 :
        canvas.create_line(0,y1,canvas.winfo_width(),y1, fill = "gray90", width = mainLine)
        y1 = y1 + 50 * scale
    while y2 >=0:
        canvas.create_line(0,y2, canvas.winfo_width(),y2, fill = "gray90", width = mainLine)
        y2 = y2-50*scale

    x1 = 400-panx
    x2 = 400-panx
    while x1 <= 800:
       canvas.create_line(x1, 0, x1, canvas.winfo_width(), fill="gray90", width=mainLine)
       x1 = x1 + 50 * scale

    while x2 >= 0:

       canvas.create_line(x2, 0, x2, canvas.winfo_width(), fill="gray90", width=mainLine)
       x2 = x2 - 50 * scale

    if scale >= 3:
        y1 = 400-pany
        y2 = 400-pany
        while y1 <= 800:
            canvas.create_line(0, y1, canvas.winfo_width(), y1, fill="gray90", width=secondaryLine)
            y1 = y1 + 5 * scale
        while y2 >= 0:
            canvas.create_line(0, y2, canvas.winfo_width(), y2, fill="gray90", width=secondaryLine)
            y2 = y2 - 5 * scale

        x1 = 400-panx
        x2 = 400-panx
        while x1 <= 800:
            canvas.create_line(x1, 0, x1, canvas.winfo_width(), fill="gray90", width=secondaryLine)
            x1 = x1 + 5 * scale

        while x2 >= 0:
            canvas.create_line(x2, 0, x2, canvas.winfo_width(), fill="gray90", width=secondaryLine)
            x2 = x2 - 5 * scale

    canvas.create_line(400-panx, 0, 400-panx, 800, fill="gray80", width=1.5)
    canvas.create_line(0, 400-pany, 800, 400-pany, fill="gray80", width=1.5)

#rounds up to the nearest 10
def roundup(x, base):
    #print("base = ", base)
    r = x%base
    if(r<base/2):
        x = x-r

    if(r>=base/2):
        x= x-r+base
    #print("x = ", x)
    return x



#COVERT SCREEN COORDS TO REAL COORDS
def ScreenToRealX(pointx,scale,snap, screenWidth=800):
    global panx
    if(snap):
        if (scale >= 3):
            x = ((pointx) - (screenWidth/2-panx))/(50*scale)
            x = roundup(x,0.1)
        else:
            x = ((pointx) - (screenWidth/2-panx)) / (50 * scale)
            x = roundup(x, 1)
    else:
        x = ((pointx) - (screenWidth / 2 - panx)) / (50 * scale)


    return x

def ScreenToRealY(pointy,scale,snap,screenHeight=800):
    global pany
    if (snap):
        if(scale >= 3):
            y = ((screenHeight/2-pany) - (pointy)) / (50 * scale)
            y = roundup(y, 0.1)
        else:
            y = ((screenHeight/2-pany)-(pointy))/(50*scale)
            y = roundup(y, 1)
    else:
        y = ((screenHeight / 2 - pany) - (pointy)) / (50 * scale)
    #y = int(y)
    #print("y = ", y)

    return y

#CONVERT REAL COORDS TO SCREEN COORDS
def RealToScreenX(pointx,scale, screenWidth=800):
    global panx
    x = ((pointx)*(50*scale))+(screenWidth/2-panx)

    return x


def RealToScreenY(pointy, scale, screenHeight=800):
    global pany
    y = -((pointy) * (50 * scale)) + (screenHeight/ 2-pany)

    return y

def panStart(event):
    global panx
    global pany
    global panStartx
    panStartx = event.x
    global panStarty
    panStarty = event.y
    global tempPanx
    global tempPany
    tempPanx = panx
    tempPany = pany

def panMove(event,geometry_object,canvas_object):
    global panStartx
    global panStarty
    global panx
    global pany
    global tempPanx
    global tempPany


    panx = tempPanx + (panStartx-event.x)
    pany = tempPany + (panStarty-event.y)

    geometry_object.update(canvas_object)

def distance(pointA,pointB):
    return math.sqrt( ((pointA[0]-pointB[0])**2)+((pointA[1]-pointB[1])**2))

#VARIABLES--------------------------------------------------------------------------------------------------------------------------


class GeometryContainer:
    def __init__(self):

        self.points = [[]]
        self.origin = [[0, 0]]
        self.transformed = [[]]
        self.transformedHistory = [[[]]]
        self.undoCounter = 0
        self.globalScale = 1.0
        self.snap = True
        self.pan = [[0,0]]
        self.stackTransforms = True
        self.selectedPoint = -1
        self.lineWidth = 1
        self.transformedLineWidth = 1.5
        self.lineColour = "black"
        self.transformedLineColour = "plum1"
        self.pointRadius = 3
        self.pointOutline = 0
        self.pointFill = "white"
        self.transformedFill = "plum1"
        self.originFill = "orchid1"
        self.mode = "Draw and Transform"

    #ADD POINTS-------------------------------------------------------------------------------------------------------------------
    def addPoint(self,event,canvas):
        x = event.x
        y = event.y

        self.points.append([ScreenToRealX(x,self.globalScale,self.snap), ScreenToRealY(y,self.globalScale,self.snap)]) #TRANSLATING FROM SCREEN COORDS TO REAL COORDS

        # print(pointsTable)
        self.update(canvas) #REFRESHING SCREEN

    def update(self,canvas_instance):

        canvas_instance.delete('all')  # clears the canvas
        # canvas_instance.update()

        drawGrid(canvas_instance,self.globalScale)  # draws the grid
        modeTextBox = canvas_instance.create_text(400, 12, text=self.mode, font=("Roboto", 10), fill="orange")
        canvas_instance.create_rectangle(canvas_instance.bbox(modeTextBox), fill="black")
        canvas_instance.create_text(400,12, text = self.mode, font = ("Roboto", 10), fill = "orange")

        # DRAW LINES-----------------------------------------------------------------------------------
        i = 1
        for i in range(1, len(self.points)):
            if i != 1:
                x = RealToScreenX(self.points[i][0],self.globalScale)
                y = RealToScreenY(self.points[i][1],self.globalScale)
                x1 = RealToScreenX(self.points[i-1][0], self.globalScale)
                y1 = RealToScreenY(self.points[i-1][1], self.globalScale)

                canvas_instance.create_line(x,y,x1,y1,width = self.lineWidth, fill = self.lineColour)
        if i > 1:
            x = RealToScreenX(self.points[i][0], self.globalScale)
            y = RealToScreenY(self.points[i][1], self.globalScale)
            x0 = RealToScreenX(self.points[1][0], self.globalScale)
            y0 = RealToScreenY(self.points[1][1], self.globalScale)
            canvas_instance.create_line(x,y,x0,y0,width = self.lineWidth, fill = self.lineColour)
                                          # draws line from last point to first point
        i = 1
        for i in range(1, len(self.transformed)):
            if i != 1:
                x = RealToScreenX(self.transformed[i][0], self.globalScale)
                y = RealToScreenY(self.transformed[i][1], self.globalScale)
                x1 = RealToScreenX(self.transformed[i - 1][0], self.globalScale)
                y1 = RealToScreenY(self.transformed[i - 1][1], self.globalScale)

                canvas_instance.create_line(x, y, x1, y1, width=self.transformedLineWidth , fill=self.transformedLineColour)
        if i > 1:
            x = RealToScreenX(self.transformed[i][0], self.globalScale)
            y = RealToScreenY(self.transformed[i][1], self.globalScale)
            x0 = RealToScreenX(self.transformed[1][0], self.globalScale)
            y0 = RealToScreenY(self.transformed[1][1], self.globalScale)
            canvas_instance.create_line(x, y, x0, y0, width=self.transformedLineWidth , fill=self.transformedLineColour)
                                         # draws line from last point to first point

        # DRAW CIRCLES AND LABELS-----------------------------------------------------------------------------------
        for i in range(1, len(self.points)):
            x = RealToScreenX(self.points[i][0], self.globalScale)
            y = RealToScreenY(self.points[i][1], self.globalScale)

            canvas_instance.create_oval(x - self.pointRadius, y - self.pointRadius, x + self.pointRadius, y + self.pointRadius, fill=self.pointFill)

            label = "(" + str(round(self.points[i][0],2)) + "," + str(round(self.points[i][1],2)) + ")"
            canvas_instance.create_text(x, y - (30*self.globalScale), text=label,font = ("Roboto", int(6*self.globalScale)))

        for i in range(1, len(self.transformed)):
            x = RealToScreenX(self.transformed[i][0], self.globalScale)
            y = RealToScreenY(self.transformed[i][1], self.globalScale)

            canvas_instance.create_oval(x - self.pointRadius, y - self.pointRadius, x + self.pointRadius,
                                        y + self.pointRadius, fill=self.transformedFill)

            xLabel = round(self.transformed[i][0], 2)
            xLabel = str(xLabel)
            yLabel = round(self.transformed[i][0], 2)
            yLabel = str(yLabel)
            label = "(" + xLabel + "," + yLabel + ")"
            fontsize= 24*self.globalScale
            canvas_instance.create_text(x, y - (30*self.globalScale), text=label, font = ("Roboto", int(6*self.globalScale)))

        # DRAW ORIGIN------------------------------------------------------------------------------------
        #print("origin = ", self.origin[0][0], " ", self.origin[0][1])
        x = RealToScreenX(self.origin[0][0], self.globalScale)
        y = RealToScreenY(self.origin[0][1], self.globalScale)
        canvas_instance.create_oval(x - self.pointRadius, y - self.pointRadius, x + self.pointRadius, y + self.pointRadius, fill=self.originFill)

    def addOriginMode(self, canvas, button):
        self.mode = "Double click to position origin"
        button.configure(relief = SUNKEN, bg="orange")
        self.update(canvas)
        canvas.bind("<Double-Button-1>",
                    lambda event: self.placeOrigin(event,canvas,button))

    def placeOrigin(self, event, canvas, button):
        #print("Placing origin")
        #print(self.origin)
        x = event.x
        y = event.y
        #print(x)
        #print(y)
        x = ScreenToRealX(x, self.globalScale,self.snap)
        y = ScreenToRealY(y, self.globalScale,self.snap)
        self.origin.append([x, y])
        self.origin.pop(0)
        #print(self.origin[0][0], self.origin[0][1])
        self.mode = "Draw and Transform"
        self.update(canvas)
        button.configure(relief=RAISED, bg="chartreuse2")
        canvas.bind("<Double-Button-1>",
                    lambda event: self.addPoint(event,canvas))

    def clear(self, canvas_instance):
        global panx
        global pany
        panx = 0
        pany = 0
        #print("button pressed")
        canvas_instance.delete('all')

        pointsSize = len(self.points)

        for i in range(pointsSize - 1, 0, -1):
            del self.points[i]

        for i in range(len(self.transformed) - 1, 0, -1):
            del self.transformed[i]

        for i in range(len(self.transformedHistory) - 1, 0, -1):
            del self.transformedHistory[i]

        self.undoCounter=0

        print("undoCounter = ", self.undoCounter)
        print(self.transformedHistory)
        mode = "Draw and Transform"
        self.update(canvas_instance)

    def deletePoint(self, event, canvas_instance):  # delete a point
        #print("Middle ", event.x, " ", event.y)
        x = event.x
        y = event.y

        pointToDelete = 0
        for i in range(1, len(self.points)):
            xp = RealToScreenX(self.points[i][0], self.globalScale)
            yp = RealToScreenY(self.points[i][1], self.globalScale)
            if ((x >= xp - 10*self.globalScale) and (x <= xp + 10*self.globalScale) and (y >= yp - 10*self.globalScale) and (y <= yp + 10*self.globalScale)):
                #print("yes ", i)
                pointToDelete = i
                break

        if (pointToDelete != 0):
            self.points.pop(pointToDelete)

        self.update(canvas_instance)

    def addUndo(self):
        print("--------------------------------------------")
        print("addUndo| undoCounter = ", self.undoCounter)
        print(self.transformed)
        if(len(self.transformed)>1):
            if(self.undoCounter<=20):
                self.undoCounter += 1
                self.transformedHistory.append(self.transformed)
            else:
                self.transformedHistory.pop(1)
                self.transformedHistory.append(self.transformed)
        print("undoCounter = ", self.undoCounter)
        print(self.transformedHistory)
        print("--------------------------------------------")


    def enlarge(self, canvas, scale):
        #print("Enlarging")
        #print(self.stackTransforms)
        #print(originCoords)
        #print("enlarge command: scale = ", scale.get())
        scaleFactor = float(scale.get())  # gets scale from the box
        if scaleFactor != 1:
            tempPoints = [[]]

            if self.stackTransforms is True and len(self.transformed)>1:

                for i in range(1, len(self.points)):  # converts screen coords to friendly coords

                    tempPoints.append([self.transformed[i][0],
                                       self.transformed[i][1]])
                #print(tempPoints)
            else:
                for i in range(1, len(self.points)):  # converts screen coords to friendly coords

                    tempPoints.append([self.points[i][0],
                                       self.points[i][1]])
                #print(tempPoints)


            if (len(tempPoints) > 1):

                for i in range(1,
                               len(tempPoints)):  # moves all points as if the origin was at 0,0 - shifts the coord system
                    tempPoints[i][0] = tempPoints[i][0] - self.origin[0][0]
                    tempPoints[i][1] = tempPoints[i][1] - self.origin[0][1]
                for i in range(1, len(tempPoints)):  # enlargment here
                    tempPoints[i][0] = tempPoints[i][0] * scaleFactor
                    tempPoints[i][1] = tempPoints[i][1] * scaleFactor
                for i in range(1, len(tempPoints)):  # moves all points back to previous origin position - shifts it back
                    tempPoints[i][0] = tempPoints[i][0] + self.origin[0][0]
                    tempPoints[i][1] = tempPoints[i][1] + self.origin[0][1]

            # pointsTable = tempPoints
            self.transformed = tempPoints
            if self.stackTransforms is True:
                self.addUndo()
            #print(transformedPoints)
            self.update(canvas)

    def setScale(self,scale):
        if(scale):
            self.globalScale = scale/100
            #print("Scale change = ", self.globalScale,)
            self.update(canvas)

    def rotate(self, canvas, rotation):
        if(rotation !=0):
            rotationRadians = math.radians(float(rotation.get()))  # gets scale from the box
            tempPoints = [[]]

            if self.stackTransforms is True and len(self.transformed) > 1:

                for i in range(1, len(self.transformed)):  # converts screen coords to friendly coords
                    tempPoints.append([self.transformed[i][0], self.transformed[i][1]])
                #print(tempPoints)
                if (len(self.points) > 1):

                    for i in range(1,
                                   len(
                                       tempPoints)):  # moves all points as if the origin was at 0,0 - shifts the coord system
                        tempPoints[i][0] = tempPoints[i][0] - self.origin[0][0]
                        tempPoints[i][1] = tempPoints[i][1] - self.origin[0][1]
                    for i in range(1, len(tempPoints)):  # enlargment here
                        x = tempPoints[i][0]
                        y = tempPoints[i][1]
                        sinAlpha = math.sin(rotationRadians)
                        cosAlpha = math.cos(rotationRadians)

                        tempPoints[i][0] = round(x * cosAlpha + y * sinAlpha,1)
                        tempPoints[i][1] = round(x * -sinAlpha + y * cosAlpha,1)
                    for i in range(1, len(
                            tempPoints)):  # moves all points back to previous origin position - shifts it back
                        tempPoints[i][0] = tempPoints[i][0] + self.origin[0][0]
                        tempPoints[i][1] = tempPoints[i][1] + self.origin[0][1]
            else:
                for i in range(1, len(self.points)):  # converts screen coords to friendly coords
                    tempPoints.append([self.points[i][0],self.points[i][1]])
                #print(tempPoints)
                if (len(self.points) > 1):

                    for i in range(1,
                                   len(tempPoints)):  # moves all points as if the origin was at 0,0 - shifts the coord system
                        tempPoints[i][0] = tempPoints[i][0] - self.origin[0][0]
                        tempPoints[i][1] = tempPoints[i][1] - self.origin[0][1]
                    for i in range(1, len(tempPoints)):  # enlargment here
                        x = tempPoints[i][0]
                        y = tempPoints[i][1]
                        sinAlpha = round(math.sin(rotationRadians),1)
                        cosAlpha = round(math.cos(rotationRadians),1)

                        tempPoints[i][0] = x * cosAlpha + y * sinAlpha
                        tempPoints[i][1] = x * -sinAlpha + y * cosAlpha
                    for i in range(1, len(tempPoints)):  # moves all points back to previous origin position - shifts it back
                        tempPoints[i][0] = tempPoints[i][0] + self.origin[0][0]
                        tempPoints[i][1] = tempPoints[i][1] + self.origin[0][1]

                # pointsTable = tempPoints
            self.transformed = tempPoints
            if self.stackTransforms is True:
                self.addUndo()
            self.update(canvas)

    def translate(self, canvas, vectorx,vectory):

        if(vectorx!=0 or vectory!=0):
            tempPoints = [[]]

            if self.stackTransforms is True and len(self.transformed) > 1:
                for i in range(1,len(self.transformed)):
                    tempPoints.append([self.transformed[i][0],self.transformed[i][1]])

            else:
                for i in range(1,len(self.points)):
                    tempPoints.append([self.points[i][0],self.points[i][1]])

            for i in range(1, len(tempPoints)):
                tempPoints[i][0] = tempPoints[i][0] + vectorx
                tempPoints[i][1] = tempPoints[i][1] + vectory

            self.transformed = tempPoints
            if self.stackTransforms is True:
                self.addUndo()

            self.update(canvas)

    def changeStacked(self):
        self.stackTransforms = not self.stackTransforms
    def movePoint(self,event,canvas):
        tempPoint = [[0,0]]
        tempPoint[0][0] = ScreenToRealX(event.x, self.globalScale,self.snap)
        tempPoint[0][1] = ScreenToRealY(event.y, self.globalScale,self.snap)

        self.points[self.selectedPoint][0] = tempPoint[0][0]
        self.points[self.selectedPoint][1] = tempPoint[0][1]
        self.update(canvas)


    def selectPoint(self,event,canvas):

        x = event.x
        y = event.y


        if(self.selectedPoint == -1):
            for i in range(1, len(self.points)):
                xp = RealToScreenX(self.points[i][0], self.globalScale)
                yp = RealToScreenY(self.points[i][1], self.globalScale)
                print(xp," ",yp)
                if ((x >= xp - 10 * self.globalScale) and (x <= xp + 10 * self.globalScale) and (
                        y >= yp - 10 * self.globalScale) and (y <= yp + 10 * self.globalScale)):
                    print("yes ", i)
                    self.selectedPoint = i
                    break

    def clearSelected(self):
        self.selectedPoint = -1

    def undo(self, canvas):
        print("----------------------------------------------")
        print("Undoing| Undo Counter = ", self.undoCounter)
        print("tranformed = ",self.transformed)
        print("transformedHistory = ", self.transformedHistory[self.undoCounter])
        self.undoCounter -= 1
        self.transformed = self.transformedHistory[self.undoCounter]


        print("tranformed = ",self.transformed)
        print("transformedHistory = ",self.transformedHistory)
        print("Undo Counter = ", self.undoCounter)

        self.update(canvas)

    def redo(self,canvas):
        if(len(self.transformedHistory) > self.undoCounter+1):
            print("--------------------------------------------")
            print("redo| undoCounter = ", self.undoCounter)
            print("Transformed = ", self.transformed)
            print("History = ",self.transformedHistory)

            self.transformed = self.transformedHistory[self.undoCounter+1]
            self.update(canvas)
            self.undoCounter += 1

            print("Transformed = ", self.transformed)
            print("History = ", self.transformedHistory)

        else:
            print("unable to redo")

    def insertPointStart(self,canvas,button):
        if(len(self.points)>=3):
            self.mode = "Insert point"
            self.update(canvas)
            canvas.bind("<Double-Button-1>",
                        lambda event: self.insertPoint(event,canvas,button))
            button.configure(relief=SUNKEN, bg="orange")
        

    def insertPoint(self,event,canvas,button):
        pointC = [ScreenToRealX(event.x,self.globalScale,self.snap),ScreenToRealY(event.y,self.globalScale,self.snap)]
        insertionPoint=-1
        for i in range(1,len(self.points)-1):
            A = distance(self.points[i],pointC)
            B = distance(self.points[i+1],pointC)
            C = distance(self.points[i],self.points[i+1])
            if(A+B<C+0.1 and A+B>C-0.1):
                print("Hurray the point was ", i)
                insertionPoint = i+1
                break
        if(insertionPoint!=-1):
            self.points.insert(insertionPoint,pointC)
            print("inserted in place ", insertionPoint, " the point coords were ", pointC, "the event was ", event.x, ",", event.y)
            self.update(canvas)
        if(insertionPoint == -1): # check between last point and first
            A = distance(self.points[1], pointC)
            B = distance(self.points[len(self.points)-1], pointC)
            C = distance(self.points[1], self.points[len(self.points)-1])
            if (A + B < C + 0.1 and A + B > C - 0.1):
                print("Hurray the point was ", i)
                insertionPoint = -2

        if(insertionPoint == -2):
            print("point was between the last and first")
            self.points.append(pointC)
            self.update(canvas)

        canvas.bind("<Double-Button-1>",
                    lambda event: self.addPoint(event,canvas))
        self.mode = "Draw and Transform"
        button.configure(relief=RAISED, bg="DeepSkyBlue2")
        self.update(canvas)

        '''
    def drawCircle(self,canvas,radius):
        angle = 0
        increment = 0.001
        print("drawingcircle")
        i = radius
        while(i > -radius):
            print(i)
            print(radius-(i*i))
            self.points.append([math.sqrt((radius * radius) - (i * i)), i])
            #self.update(canvas)
            #time.sleep(0.1)
            angle+=1/(radius*radius)
            i = i - math.sin(math.radians(angle))
        angle = 0
        i = radius
        while(i > -radius):
            print(i)
            self.points.append([math.sqrt((radius*radius)-(i*i))*-1, i])
            #self.update(canvas)
            #time.sleep(0.1)

            angle += 1/(radius*radius)
            i = i - math.sin(math.radians(angle))

        self.update(canvas)
        '''

    def changeSnap(self):

        self.snap = not self.snap

#LAYOUT SECTION--------------------------------------------------------------------------------------------------------------------
root = Tk()
root.geometry("+500+50")
topFrame = Frame(root,width = 800, height = 800)
topFrame.pack()
canvas = Canvas(topFrame,width = 800, height = 800, background="white")
canvas.pack()
midFrame = Frame(root)
midFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack()

#GEOMETRY OBJECT INTIALISE----------------------------------------------------------------------------------------------------------
geometry = GeometryContainer()
geometry.update(canvas)
#geometry.drawCircle(canvas,5)
#BUTTON SECTION----------------------------------------------------------------------------------------------------------------
clearButton = Button(bottomFrame,text="Clear", command = lambda:geometry.clear(canvas),bg="red",fg="white",height = 3, width = 10)
originButton = Button(bottomFrame,text="Set Origin",height = 3, width = 10, bg="chartreuse2", fg="black", command = lambda:geometry.addOriginMode(canvas,originButton))
enlargeButton = Button(bottomFrame,text="Enlarge",height = 3, width = 10,command = lambda:geometry.enlarge(canvas,scaleEntry) )
rotateButton = Button(bottomFrame,text="Rotate",height = 3, width = 10,command = lambda:geometry.rotate(canvas,rotateEntry) )
translateButton = Button(bottomFrame,text="Translate",height = 3, width = 10, command = lambda:geometry.translate(canvas,float(translateEntryx.get()),float(translateEntryy.get())))
insertPointButton = Button(bottomFrame,text="Insert",height = 3, width = 10, bg="DeepSkyBlue2", command = lambda:geometry.insertPointStart(canvas,insertPointButton))
scaleSlider = Scale(midFrame, from_=0, to=400, orient=HORIZONTAL, resolution = 10, length=800, digits =1, label="Zoom", showvalue=1, command = lambda event: geometry.setScale( scaleSlider.get() ))
scaleSlider.set(100)
stackTransformsCheck = Checkbutton(bottomFrame,text= "Stack transformations", onvalue = True, offvalue = False, command = lambda: geometry.changeStacked())
stackTransformsCheck.select()
snapButton = Checkbutton(bottomFrame,text= "Snapping", onvalue = True, offvalue = False, command = lambda: geometry.changeSnap())
snapButton.select()
undoButton = Button(bottomFrame,text = "Undo",height = 3, width = 10, command = lambda:geometry.undo(canvas))
redoButton = Button(bottomFrame,text = "Redo",height = 3, width = 10, command = lambda:geometry.redo(canvas))


clearButton.grid(row = 1, column = 0, rowspan = 2)
originButton.grid(row = 1, column = 1, rowspan = 2)
enlargeButton.grid(row = 1, column = 3, rowspan = 2)
rotateButton.grid(row = 1, column = 4, rowspan = 2)
translateButton.grid(row = 1, column = 5, rowspan = 2, columnspan=2)
stackTransformsCheck.grid(row = 0, column = 0, columnspan = 2)
snapButton.grid(row = 0, column = 8, columnspan = 2)
undoButton.grid(row = 1,column = 7)
redoButton.grid(row = 1,column = 9)
insertPointButton.grid(row=1,column=2)
#matrixButton.grid(row = 1, column = 6, rowspan = 2)

scaleSlider.pack()
#clearButton.pack()
#originButton.pack()
#enlargeButton.pack()
#rotateButton.pack()
#translateButton.pack()
#matrixButton.pack()





#INPUT BOXES-----------------------------------------------------------------------------------------------------------------------
#scaleLable = Label(bottomFrame,text = "Scale",height = 3)
scaleEntry = Entry(bottomFrame, width=10)
scaleEntry.insert(END, 1)

#scaleLable.pack(side=LEFT)
#scaleEntry.pack(side=LEFT)
#rotateLable = Label(bottomFrame,text = "Rotate",height = 3)
rotateEntry = Entry(bottomFrame, width=10)
rotateEntry.insert(END, 0)
#rotateLable.pack(side=LEFT)
#rotateEntry.pack(side=LEFT)
#translateLable = Label(bottomFrame,text = "Translate",height = 3)
#translateEntry = Entry(bottomFrame, width=4)
#translateLable.pack(side=LEFT)
#translateEntry.pack(side=LEFT)
#translateLable = Label(bottomFrame,text = "Translate",height = 3)
translateEntryx = Entry(bottomFrame, width=5)
translateEntryx.insert(END, 0)
translateEntryy = Entry(bottomFrame, width=5)
translateEntryy.insert(END, 0)
#matrixLable = Label(bottomFrame,text = "Translate",height = 3)
#matrixEntry = Entry(bottomFrame, width=4)
#matrixLable.pack(side=LEFT)
#matrixEntry.pack(side=LEFT)

#scaleLable.grid(row = 2,column = 3, sticky=N)
scaleEntry.grid(row = 0,column = 3, sticky=N)
rotateEntry.grid(row = 0,column = 4, sticky=N)
translateEntryx.grid(row = 0,column = 5, sticky=N)
translateEntryy.grid(row = 0,column = 6, sticky=N)

#MOUSE BINDINGS---------------------------------------------------------------------------------------------------------------------
#drawAll(canvas,points,origin,transformed)
#place point with double click
canvas.bind("<Double-Button-1>", lambda event: geometry.addPoint(event,canvas))

#delete point with middle button
canvas.bind("<Button-2>", lambda event: geometry.deletePoint(event,canvas))

#move point with right button
canvas.bind("<Button-3>", lambda event: geometry.selectPoint(event,canvas))
canvas.bind("<B3-Motion>", lambda event: geometry.movePoint(event,canvas))
canvas.bind("<ButtonRelease-3>", lambda event: geometry.clearSelected())

#pan
canvas.bind("<Button-1>", panStart)
canvas.bind("<B1-Motion>", lambda event: panMove(event,geometry,canvas))
#canvas.bind("<ButtonRelease-1>", panStop)





root.mainloop()









