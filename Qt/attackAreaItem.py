from PyQt4 import QtGui,  QtSvg
from PyQt4.QtCore import *
import math, os

class attackAreaItem(QtGui.QGraphicsEllipseItem):
    def __init__(self, parent=None, center=QPointF(0,0),  range=40*2.5):
        self.center=center
        self.parent=parent
        #this class is the external circle
        r3=self.getRectangle(3*range)
        QtGui.QGraphicsEllipseItem.__init__(self,r3,parent=None)#0, 0, width, height)
        pen=QtGui.QPen()
        pen.setWidth(2)
        self.setPen(pen)
        #this is the range 2 circle
        r2=self.getRectangle(2*range)
        self.range2=QtGui.QGraphicsEllipseItem(r2,parent=self)
        self.range2.setPen(pen)
        #this is the range 1 circle
        r1=self.getRectangle(range)
        self.range1=QtGui.QGraphicsEllipseItem(r1,parent=self)
        self.range1.setPen(pen)
        #this is the center
        center=self.getRectangle(2)
        self.center=QtGui.QGraphicsEllipseItem(center,parent=self)
        fillBrush=QtGui.QBrush( QtGui.QColor(0,0,0), Qt.SolidPattern )
        self.center.setBrush(fillBrush)
        self.center.setPen(pen)

        
        #setting up for user interaction
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(100)
    def getSize(self):
        self.setStartAngle
        
    def getRectangle(self,radius):
        return QRectF(self.center-QPointF(radius,radius),self.center+QPointF(radius,radius))
    def setPosFromBattleEngine(self,position):
        self.setPos(QPointF(position.x-self.width/2,-1*position.y+self.height/2))
        rotation=math.degrees(position.getRotation())
        #print rotation
        self.setRotation(rotation)
