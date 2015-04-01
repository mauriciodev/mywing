import math

class position:
    def __init__(self,x=0,y=0, vx=0,vy=1):
        #position x, y and a direction unit vector 
        self.x=x
        self.y=y
        self.setUnitVector(vx,vy)
    
    def rotate(self,angle):
        #print self.vx,self.vy
        rotated=self.rotateVector(self.vx, self.vy, angle)
        self.setUnitVector(rotated[0], rotated[1])
    def getRotation(self):
        theta=math.acos(self.vy)
        if (self.vx<0):
            theta*=-1
        return theta
    def moveBy(self,dx,dy):
        #movement along the tangent
        self.x+=self.vx*dx 
        self.y+=self.vy*dx
        angle=math.pi/2
        perpendicularVector=self.rotateVector(self.vx, self.vy, angle)
        self.x+=perpendicularVector[0]*dy
        self.y+=perpendicularVector[1]*dy
        
    def rotateVector(self,vx,vy,angle):
        vx1=vx*math.cos(angle)-vy*math.sin(angle) 
        vy1=vx*math.sin(angle)+vy*math.cos(angle)
        return (vx1,vy1)
    
    def setUnitVector(self,vx,vy):
        m=math.sqrt(vx*vx+vy*vy)
        self.vx=vx/m
        self.vy=vy/m
        
    def revertTrigAngle(self): 
        #self.trigAngle=math.fmod((azimuth+math.pi),math.pi*2)
        pass
        
    def bearing(self,pos2):
        dx=pos2.x-self.x
        dy=pos2.y-self.y
        cosTheta=(self.vx*dx+self.vy*dy)/math.sqrt(dx**2+dy**2)
        bearing=math.acos(cosTheta)
        cross=self.unitVectorCrossProduct(pos2)
        if abs(cross)!=0.:
            sign=cross/abs(cross)
        else: sign=1
        return bearing*sign
        
    def distance(self,pos2):
        return math.sqrt((self.x-pos2.x)**2 + (self.y-pos2.y)**2)
    
    def unitVectorCrossProduct(self,pos2):
        return self.vx*pos2.vy-self.vy*pos2.vx
    
    def unitVectorScalarProduct(self,pos2):
        return self.vx*pos2.vx+self.vy*pos2.vy
    def unitVectorModule(self):
        return math.sqrt(self.vx**2+self.vy**2)
    
    def reduceAngle(self,angle):
        return math.fmod(angle,math.pi*2)
    def getRange(self,pos2):
        dx=self.x-pos2.x
        dy=self.x-pos2.x
        return (math.sqrt(dx*dx+dy*dy))
    
    def isInRange(self,pos2):
        range=self.getRange(pos2)
        bearing=self.getBearing(pos2)
        if (range<3) and (True):
            return True
        else:
            return False
    def toDict(self):
        d={}
        d['x']=self.x
        d['y']=self.y
        d['vx']=self.vx
        d['vy']=self.vy
        return d
        
if __name__=="__main__":
    a=position(10,10,math.pi)
    b=position(10,15,10)
    