import json
import random
import os
from pilot import pilot
from position import position
from move import move
from ship import ship

class BattleEngine:
    def __init__(self):
        #first read the moves
        self.movesLibrary={} #this list represents every available move
        self.readMoves()
        #then ships, that aggregates moves
        self.shipsLibrary={} #this list represents every available ship
        self.readShips()
        #then pilots that aggregates ships
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
    
    def performMove(self,pilotBattleId, moveId):
        startPos=self.getPilotPos(pilotBattleId)
        print "From: ",startPos.toDict()
        newPos=self.movesLibrary[moveId].performMove(startPos)
        self.setPilotPos(pilotBattleId, newPos)
        print "To:",newPos.toDict()
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
        print self.pilots[pilotId1].name, "attacked."
        attackResults=self.rollAttackDices(self.pilots[pilotId1].attack)
        print attackResults
        print self.pilots[pilotId2].name, "tries to avoid the attacks."
        defenseResults=self.rollDefenseDices(self.pilots[pilotId2].defense)
        print defenseResults
        #first, lower attack using evade
        attackResults['attack']-=defenseResults['evade']
        #if attack is negative, it lowers criticals too
        if (attackResults['attack']<0): 
            attackResults['critical']+=attackResults['attack']
            attackResults['attack']=0
        damage=attackResults['attack']+attackResults['critical']
        print self.pilots[pilotId2].name, "took",attackResults['attack'],"regular hits and", attackResults['critical'], "critical hits."
        self.pilots[pilotId2].takeDamage(damage)
        print self.pilots[pilotId2].name, "now has",self.pilots[pilotId2].shield,"shield and",self.pilots[pilotId2].health, "health" 
            
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
    def readMoves(self):
        self.movesLibrary={}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname,'data/moves.json')) as f:
            for line in f:
                m=move()
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
    

    
if __name__=="__main__":
    test=BattleEngine()
    #test.readPilots()
    test.addPilotByNameAndCoords("Mauricio", 0, 0, 0,1)
    test.addPilotByNameAndCoords("Leonardo", 0, 0, 0,2)
    #print test.pilots[0].isComplete()
    test.basicAttack(0, 1)
    #print test.pilots[1].health,test.pilots[1].shield 
    
    #for move in test.pilots[0].moves:
    #    print move.name
    #print test.rollAttackDices(10)
    #print test.rollDefenseDices(10)
    #test.savePilots()
    