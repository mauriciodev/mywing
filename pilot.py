from ship import ship


"""Pilots store pilot data. If it's a complete pilot, it also stores the ship and moves necessary for battle calculations."""
class pilot:
    def __init__(self,id=0,name='',skillLevel=0,attack=0,defense=0,health=0,shield=0, shipId=0,cost=0):
        self.id=0
        self.name=name
        self.skillLevel=skillLevel
        self.attack=attack
        self.defense=defense
        self.health=health
        self.shield=shield
        self.attackAngle=(-40,40) #bearing
        self.shipId=shipId
        self.maneuvers=[]
        self.improvements=[]
        self.cost=cost
        self.resetHealth()
        self.setIncomplete()
        
    def resetHealth(self):
        self.currentHealth=self.health
        self.currentShield=self.shield
    def takeDamage(self,n):
        if (self.shield>0):
            self.shield-=n
            if self.shield<0: #shield broke
                self.health+=self.shield #takes whatever went through shield
                self.shield=0
        else: #no shield
            self.health-=n
    def getCost(self):
        return self.skillLevel+self.attack+self.defense+self.health+self.shield
    def asDict(self):
        """output={}
        output['id']=self.id
        output['name']=self.name
        output['skillLevel']=self.skillLevel
        output['attack']=self.attack
        output['defense']=self.defense
        output['health']=self.health
        output['shield']=self.shield
        output['attackAngle']=self.attackAngle
        output['ship']=self.ship
        #output['actions']=self.
        #output['improvements']=self.
        output['cost']=self.cost
        return output"""
    def fromDict(self,dict):
        self.id=dict['id']
        self.name=dict['name']
        self.skillLevel=dict['skillLevel']
        self.attack=dict['attack']
        self.defense=dict['defense']
        self.health=dict['health']
        self.shield=dict['shield']
        self.attackAngle=dict['attackAngle']
        #self.=dict['actions']
        #self.=dict['improvements']
        self.shipId=dict['shipId']
        self.cost=dict['cost']
        self.setIncomplete()

    def setComplete(self,ship, moves,battleId,pos):
        self.moves=moves
        self.ship=ship
        self.battleId=battleId
        self.position=pos
    def setIncomplete(self):
        self.ship=None
        self.moves=[]
        self.battleId=-1
        self.position=None
    def isComplete(self):
        t1=(len(self.moves)>0)
        t2=(self.ship!=None)
        t3=(self.battleId!=-1)
        t4=(self.position!=None)
        return (t1 and t2 and t3 and t4) 
    
    def getMoveByName(self,name):
        if self.isComplete():
            for move in self.moves:
                if move.name==name:
                    return move
        return None
    def getMoveCost(self,moveName):
        move=self.getMoveByName(moveName)
        return self.ship.getMoveCost(move.id)
        
        

