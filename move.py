import math
from position import position
moveTypesDescription={0:"linear", 1:"curve",2:"strong curve",3:"U turn"}

class move:
    def __init__(self,id=0,name='NewMove', dx=0,dy=0,rotation=0,scale=50):
        self.id=id
        self.dx=dx #move along the tangent
        self.dy=dy #move along the perpendicular
        self.rotation=rotation
        self.name=name
        self.scale=scale
            
    def performMove(self,pos):
        pos.moveBy(self.dx*self.scale,self.dy*self.scale)
        pos.rotate(self.rotation)
        return pos
    
    def fromDict(self,dict):
        self.id=dict['id']
        self.dx=dict['dx'] #move along the tangent
        self.dy=dict['dy'] #move along the perpendicular
        self.rotation=math.radians(dict['rotation'])
        self.name=dict['name']

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
    print test.performMove2(position(0,0,math.radians(90)), 10,10, math.radians(90))
    print test.circularMove(position(0,0,math.radians(90)), 10, math.radians(90))