from ship import ship


"""Pilots store pilot data."""
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
        self.shipId=-1
        self.ship=None
        self.improvements=[]
        self.cost=cost
        self.availableActionsNames=[]
        self.availableActions=[]
        self.resetHealth()
        
    def resetHealth(self):
        self.currentHealth=self.health
        self.currentShield=self.shield
    def takeDamage(self,n):
        if n<=0: return
        if (self.shield>0):
            self.shield-=n
            if self.shield<0: #shield broke
                self.health+=self.shield #takes whatever went through shield
                self.shield=0
        else: #no shield
            self.health-=n
    def getCost(self):
        return self.cost
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
        self.availableActionsNames=dict["actions"]

    def hasAction(self,actionName):
        result=False
        for actionObj in self.availableActions:
            if actionObj.name==actionName:
                result=actionObj
        return result
        #return actionName in self.availableActionsNames
            
  
    def getMoveByName(self,name):
        for move in self.moves:
            if move.name==name:
                return move
        return None
    
    def getMoveById(self,moveId):
        for move in self.moves:
            if move.id==moveId:
                return move
        return None
    
    def getMoveCost(self,moveName):
        move=self.getMoveByName(moveName)
        return self.ship.getMoveCost(move.id)
        
        

