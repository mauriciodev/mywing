from ship import ship

class pilot:
    def __init__(self,id=0,name='',skillLevel=0,attack=0,defense=0,health=0,shield=0, pilotShip='',cost=0):
        self.id=0
        self.name=name
        self.skillLevel=skillLevel
        self.attack=attack
        self.defense=defense
        self.health=health
        self.shield=shield
        self.attackAngle=(-40,40) #bearing
        self.ship=ship(pilotShip)
        self.moveIds=ship(self.ship).moveIds
        self.maneuvers=[]
        self.improvements=[]
        self.cost=cost
        self.resetHealth()
        
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
        output={}
        output['id']=self.id
        output['name']=self.name
        output['skillLevel']=self.skillLevel
        output['attack']=self.attack
        output['defense']=self.defense
        output['health']=self.health
        output['shield']=self.shield
        output['attackAngle']=self.attackAngle
        output['ship']=self.ship
        #output['maneuvers']=self.
        #output['improvements']=self.
        output['cost']=self.cost
        return output
    def fromDict(self,dict):
        self.id=dict['id']
        self.name=dict['name']
        self.skillLevel=dict['skillLevel']
        self.attack=dict['attack']
        self.defense=dict['defense']
        self.health=dict['health']
        self.shield=dict['shield']
        self.attackAngle=dict['attackAngle']
        #self.=dict['maneuvers']
        #self.=dict['improvements']
        self.ship=ship(dict['ship'])
        self.moveIds=ship(self.ship).moveIds
        self.cost=dict['cost']


