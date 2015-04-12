import math
from PyQt4 import QtCore, QtGui
moveTypesDescription={0:"linear", 1:"curve",2:"strong curve",3:"U turn"}

class move:
    def __init__(self,id=0,name='NewMove', dx=0,dy=0,rotation=0,scale=0):
        self.id=id
        self.dx=dx*scale #move along the tangent
        self.dy=dy*scale #move along the perpendicular
        self.rotation=rotation
        self.name=name
        self.scale=scale
            
    def performMove(self,mini):
        newPos=self.standardMove(mini)
        
        return newPos
    
    def fromDict(self,dict):
        self.id=dict['id']
        self.dx=dict['dx']*self.scale #move along the tangent
        self.dy=dict['dy']*self.scale #move along the perpendicular
        self.rotation=dict['rotation']
        self.name=dict['name']
        
    def standardMove(self,mini):
        v0=QtGui.QVector2D(mini.getPos())
        #computing support vectors
        uVec=mini.getUnitVector()
        normalVec=self.rotateVector(uVec, -90)
        #First, we move the center of mass to the border of the unit's base. 
        v1=v0+uVec*mini.height/2.
        #then we perform the move
        v2=v1+uVec*self.dx+normalVec*self.dy
        #now we rotate the ship
        mini.doRotate(self.rotation)
        #and we get the new direction to move the center of mass back to it's place
        uVec=mini.getUnitVector()
        v3=v2+uVec*mini.height/2.
        mini.setPos(v3.toPointF())
        
        return mini.getPos()


        
    def rotateVector(self,vec,angle):
        angle=math.radians(angle)
        vx1=vec.x()*math.cos(angle)-vec.y()*math.sin(angle) 
        vy1=vec.x()*math.sin(angle)+vec.y()*math.cos(angle)
        return QtGui.QVector2D(vx1,vy1)
        
    """def performMove(self,startPosition):
        if moveType=='line':
            return self._performLine(startPosition)
        if modeType=='curve':
            return self._performCurve(startPosition)
        if modeType=='strongcurve':
            return self._performStrongCurve(startPosition)
        if modeType=='uturn':
            return self._performUTurn(startPosition)
        
            
    def _performCurve(self,startPosition):
        self.circularMove(pos, self.distance, self.angle)
    
    def _performStrongCurve(self,startPosition):
        #i'm not sure if these are equal, so they are here for now
        self._performCurve(startPosition)
    
    def _performLine(self,startPosition):
        x=startPosition.x+self.distance*self.scale*math.acos(startPosition.trigAngle)
        y=startPosition.y+self.distance*self.scale*math.asin(startPosition.trigAngle)
        newPos=position(x,y,startPosition.trigAngle)
        return newPos #returns the same direction
    
    def _performUTurn(self,startPosition):
        performLine=self._performLine(startPosition)
        performLine.revertTrigAngle()
        return performLine
    
    def circularMove(self,pos,radius, angle):
        #center
        cx=pos.x+radius*math.sin(pos.trigAngle)
        cy=pos.y-radius*math.cos(pos.trigAngle)
        #find the starting angle on the circle
        circStartAngle=pos.reduceAngle(math.pi/2+pos.trigAngle)
        circFinalAngle=circStartAngle-angle
        #find the tangent by the end of the move
        finalTrigAngle=pos.reduceAngle(circFinalAngle+math.pi/2)
        newPos=(cx+math.cos(circFinalAngle)*radius,cy+math.sin(circFinalAngle)*radius,finalTrigAngle)
        return newPos"""
        

if __name__=="__main__":
    test=move()
    #print math.degrees(test.revertTrigAngle(math.pi/3))
    #print math.degrees(test.revertTrigAngle(math.pi*4/3))
    print test.performMove2(position(0,0,math.radians(90)), 10,10, 90)
    print test.circularMove(position(0,0,math.radians(90)), 10, 90)