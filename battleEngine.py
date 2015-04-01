import json
import random
import os
import math
from pilot import pilot
from position import position
from move import move
from ship import ship
from PyQt4.QtCore import QObject, pyqtSignal, QString

class defaultPrinter(QObject):
    def __init__(self,battleEngine):
        super(defaultPrinter,self).__init__()
        battleEngine.messagePrinted.connect(self.printMessage)
        battleEngine.pilotDestroyed.connect(self.pilotDestroyed)
    def printMessage(self,s):
        print s
    def pilotDestroyed(self,pilotId):
        self.printMessage("Pilot %i was destroyed." % pilotId)

class BattleEngine(QObject):
    messagePrinted=pyqtSignal('QString')
    pilotDestroyed=pyqtSignal('int')
    def __init__(self,scale=50,shotRange=3):
        super(BattleEngine,self).__init__()
        self.shotRange=shotRange #number of unscaled units that remains inside range 1
        #first read the moves
        self.printMessage("Loading move data.")
        self.movesLibrary={} #this list represents every available move
        self.scale=scale
        self.readMoves(self.scale)
        #then ships, that aggregates moves
        self.printMessage("Loading ship data.")
        self.shipsLibrary={} #this list represents every available ship
        self.readShips()
        #then pilots that aggregates ships
        self.printMessage("Loading pilot data.")
        self.pilotLibrary={} #this list represents every available pilot 
        self.readPilots()
        
        #these lists represent the pilots in game and their positions
        self.pilots=[] #list of complete pilots, ready to battle
        self.players={}
        
        random.seed()
        self.attackResults=['attack','attack','attack','critical','focus','focus','nothing','nothing']
        self.defenseResults=['evade','evade','evade','focus','focus','nothing','nothing','nothing']
        random.shuffle(self.attackResults)
        self.turnStages=['Planning','Movement','Attack']
        self.currentStage=0
        self.currentTurn=0
        self.playerSequence=[]
        
        
    def getPilotShip(self,pilotId):
        return self.shipsLibrary[self.pilotLibrary[pilotId].shipId]
    
    def getPilotMoves(self,pilotId):
        moveIds=self.getPilotShip(pilotId).moveIds
        moves=[]
        for moveId in moveIds:
            moves.append(self.movesLibrary[moveId])
        return moves
    
    def addPlayer(self,name):
        playerId=len(self.players.keys())+1
        self.players[playerId]=name
        return playerId
        
    def removePlayer(self,playerId):
        self.players.pop(playerId)
        
    def rollAttackDices(self,n):
        rollResult={'attack':0,'critical':0,'focus':0,'nothing':0}
        for i in range(0,n):
            result=random.randint(0,7)
            rollResult[self.attackResults[result]]+=1
        return rollResult
        
    def rollDefenseDices(self,n):
        rollResult={'evade':0,'focus':0,'nothing':0}
        #3 evade 2 focus 3 nothing
        for i in range(0,n):
            result=random.randint(0,7)
            rollResult[self.defenseResults[result]]+=1
        return rollResult
    
    def pilotKilled(self, pilotId):
        self.pilotDestroyed.emit(pilotId)
        deadPilot=self.pilots.pop(pilotId)
        self.printMessage("Pilot %s was destroyed." % deadPilot.name)
    
    def performMove(self,pilotBattleId, moveId):
        startPos=self.getPilotPos(pilotBattleId)
        self.printMessage("From: ",startPos.toDict())
        newPos=self.movesLibrary[moveId].performMove(startPos)
        self.setPilotPos(pilotBattleId, newPos)
        self.printMessage( "To:" +str(newPos.toDict()))
        return newPos
    
    def getPilotPos(self,pilotBattleId):
        return self.pilots[pilotBattleId].position
    
    def setPilotPos(self,pilotBattleId,newPos):
        self.pilots[pilotBattleId].position=newPos
    
    def getRange(self,pilotId1,pilotId2):
        return self.positions[pilotId1].getRange(self.positions[pilotId2])
    
    def isInRange(self,pilotId1,pilotId2):
        return self.positions[pilotId1].isInRange(self.positions[pilotId2])
        
    def basicAttack(self,pilotId1,pilotId2):
        #this is a very basic attack sequence just to test how it should work
        #later on this should be replaced by a well timed sequence
        #i'm ignoring focus right now
        self.printMessage('')
        distance=self.pilots[pilotId1].position.distance(self.pilots[pilotId2].position)/self.scale
        bearing=self.pilots[pilotId1].position.bearing(self.pilots[pilotId2].position)
        self.printMessage(self.pilots[pilotId1].name, "attacked from range %i" % math.ceil(distance/self.shotRange), "and bearing %i."% math.degrees(bearing))
        attackDices=self.pilots[pilotId1].attack
        defenseDices=self.pilots[pilotId2].defense
        if (distance > 0) and (distance <=1*self.shotRange):
            attackDices+=1
        if (distance > 2*self.shotRange) and (distance <=3*self.shotRange):
            defenseDices+=1
        if distance > 3*self.shotRange:
            self.printMessage("Out of range. Distance:",distance)
            return
        if (bearing<math.radians(self.pilots[pilotId1].attackAngle[0])) or (bearing>math.radians(self.pilots[pilotId1].attackAngle[1])):
            self.printMessage("Enemy out of attack angle.")
            return 
        attackResults=self.rollAttackDices(attackDices)
        self.printMessage("Attack dices ("+str(attackDices)+"):")
        self.printMessage('  ',attackResults)
        self.printMessage(self.pilots[pilotId2].name, "tries to avoid the attacks.")
        defenseResults=self.rollDefenseDices(defenseDices)
        self.printMessage("Defense dices("+str(defenseDices)+"):")
        self.printMessage('  ',defenseResults)
        #first, lower attack using evade
        attackResults['attack']-=defenseResults['evade']
        #if attack is negative, it lowers criticals too
        if (attackResults['attack']<0): 
            attackResults['critical']+=attackResults['attack']
            attackResults['attack']=0
        if(attackResults['critical']<0): attackResults['critical']=0
        damage=attackResults['attack']+attackResults['critical']
        self.printMessage(self.pilots[pilotId2].name, "took",attackResults['attack'],"regular hits and", attackResults['critical'], "critical hits.")
        if damage>0: 
            self.pilots[pilotId2].takeDamage(damage)
        self.printMessage(self.pilots[pilotId2].name, "now has",self.pilots[pilotId2].shield,"shield and",self.pilots[pilotId2].health, "health")
        self.printMessage('') 
        self.checkPilot(pilotId2)
            
    def checkPilot(self,pilotId):
        if self.pilots[pilotId].health<1:
            self.pilotKilled(pilotId)
    
    def getPilotByName(self,name):
        for pilot in self.pilotLibrary.values():
            if pilot.name==name:
                return pilot
            
    def getMoveById(self,moveId):
        return self.movesLibrary[moveId]
    
    def getMoveByName(self,moveName):
        for move in self.movesLibrary.values():
            if move.name==moveName:
                return move
        
    def addPilotByNameAndCoords(self,name, x, y, trigAngle,playerId):
        pilot=self.getPilotByName(name)
        if pilot==None:
            return pilot
        pilotPos=position(x,y)
        pilotPos.rotate(trigAngle)
        pShip=self.getPilotShip(pilot.id)
        pMoves=self.getPilotMoves(pilot.id)
        battleId=len(self.pilots)
        pilot.setComplete(pShip, pMoves, battleId, pilotPos,playerId)
        self.addPilot(pilot)
        return pilot
    
    def getActivePilotIdByName(self,name):
        for i,p in enumerate(self.pilots):
            if p.name==name:
                return i
    
    def addPilot(self,pilot):
        self.pilots.append(pilot)
    
    def readPilots(self):
        self.pilotLibrary={}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname,'data/pilots.json')) as f:
            for line in f:
                p=pilot()
                p.fromDict(json.loads(line))
                self.pilotLibrary[p.id]=p
                #print p.asDict()
    def readMoves(self,scale=50):
        self.movesLibrary={}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname,'data/moves.json')) as f:
            for line in f:
                m=move(scale)
                m.fromDict(json.loads(line))
                self.movesLibrary[m.id]=m
    def readShips(self):
        self.shipsLibrary={}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname,'data/ships.json')) as f:
            for line in f:
                s=ship()
                s.fromDict(json.loads(line))
                self.shipsLibrary[s.id]=s
    def savePilots(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        pilotFile=open(os.path.join(dirname,'data/pilots.json'),'w')
        for pilot in self.pilotLibrary:
            pilotFile.write(json.dumps(pilot.asDict()))
        pilotFile.close() 
        
    def nextTurnStage(self):
        self.currentStage+=1
        #restarting the turn sequence
        if self.currentStage>len(self.turnStages): 
            self.currentStage=self.currentStage % len(self.turnStages)
    
    def getCurrentTurnStageName(self):
        return self.turnStages[self.currentTurn]
    
    def printMessage(self,*args):
        message=''
        for msg in args:
            message+=str(msg)+' '
        self.messagePrinted.emit(message)
    
    
if __name__=="__main__":
    test=BattleEngine()
    p=defaultPrinter(test)
    #test.readPilots()
    test.addPilotByNameAndCoords("Master Mauricio", 0, 0, 0,1)
    test.addPilotByNameAndCoords("General Leonardo", 0, 10, 0,2)
    #print test.pilots[0].isComplete()
    while len(test.pilots)>1:
        test.basicAttack(0, 1)
    #print test.pilots[1].health,test.pilots[1].shield 
    
    #for move in test.pilots[0].moves:
    #    print move.name
    #print test.rollAttackDices(10)
    #print test.rollDefenseDices(10)
    #test.savePilots()
    