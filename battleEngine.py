import json
import random,math
import os,sys

from position import position
from PyQt4.QtCore import QObject, pyqtSignal, QString
from pilotFactory import PilotFactory
from miniature import miniature
from PyQt4 import QtGui,  QtSvg, QtCore
from PyQt4.QtCore import *

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
    def __init__(self,scale=2.5,shotRange=10,bounds=[-450,-450,450,450]):
        super(BattleEngine,self).__init__()
        self.shotRange=shotRange #number of unscaled units that remains inside range 1
        self.scale=scale
        #these lists represent the pilots in game and their positions
        self.miniatures=[] #list of complete pilots, ready to battle
        self.players={}
        
        random.seed()
        self.attackResults=['attack','attack','attack','critical','focus','focus','nothing','nothing']
        self.defenseResults=['evade','evade','evade','focus','focus','nothing','nothing','nothing']
        random.shuffle(self.attackResults)
        self.turnStages=['Planning','Movement','Attack']
        self.currentStage=0
        self.currentTurn=0
        self.playerSequence=[]
        self.bounds=bounds
        self.pilotFactory=PilotFactory(self)
        self.scene=QtGui.QGraphicsScene()
    
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
    
    def pilotKilled(self, mini):
        self.pilotDestroyed.emit(mini.miniatureId)
        self.miniatures.pop(mini.miniatureId)
        self.printMessage("Pilot %s was destroyed." % mini.pilot.name)
    
        
    def basicAttack(self,m1,m2):
        #this is a very basic attack sequence just to test how it should work
        #later on this should be replaced by a well timed sequence
        #i'm ignoring focus right now
        #self.printMessage('')
        distance=m1.range(m2)
        #distance=self.pilots[pilotId1].position.distance(m2.pilot.position)#/self.scale
        #bearing=self.pilots[pilotId1].position.bearing(m2.pilot.position)
        bearing=m1.bearing(m2)
        self.printMessage(m1.pilot.name, "attacked from range %i" % distance, "and bearing %i."% bearing)
        attackDices=m1.pilot.attack
        defenseDices=m2.pilot.defense
        if (distance > 0) and (distance <=1*self.shotRange):
            attackDices+=1
        if (distance > 2*self.shotRange) and (distance <=3*self.shotRange):
            defenseDices+=1
        if distance > 3*self.shotRange:
            self.printMessage("Out of range. Distance:",distance)
            return
        if (bearing<m1.pilot.attackAngle[0]) or (bearing>m1.pilot.attackAngle[1]):
            self.printMessage("Enemy out of attack angle.")
            return 
        attackResults=self.rollAttackDices(attackDices)
        self.printMessage("Attack dices ("+str(attackDices)+"):")
        self.printMessage('  ',attackResults)
        self.printMessage(m2.pilot.name, "tries to avoid the attacks.")
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
        self.printMessage(m2.pilot.name, "took",attackResults['attack'],"regular hits and", attackResults['critical'], "critical hits.")
        if damage>0: 
            m2.pilot.takeDamage(damage)
        self.printMessage(m2.pilot.name, "now has",m2.pilot.shield,"shield and",m2.pilot.health, "health")
        self.printMessage('') 
        self.checkPilot(m2)
            
    def checkPilot(self,mini):
        if mini.pilot.health<1:
            self.pilotKilled(mini)
    

    def addBorders(self,scenarioName):
        #rect=QtCore.QRect(-1*x/2,-1*y/2,x/2,y/2)
        b=self.bounds
        b=map(lambda x:x*self.scale,b)
        self.borders=self.scene.addRect(b[0],b[1],b[2]-b[0],b[3]-b[1])
        dirname, filename = os.path.split(os.path.abspath(__file__))
        imageFileName=os.path.join(dirname,"images/scenarios",scenarioName+".jpg")
        pixmap=QtGui.QPixmap(imageFileName)
        pixmap=pixmap.scaled(b[2]-b[0],b[3]-b[1]);
        self.backgroundPixmap=self.scene.addPixmap(pixmap)
        self.backgroundPixmap.setPos(b[0],b[1])
        self.backgroundPixmap.setZValue(-1)

        
    def addPilotByNameAndCoords(self,name, x, y, trigAngle,playerId):
        p=self.pilotFactory.getPilotByName(name)
        if p==None:
            return p
        #pilotPos=position(x,y)
        #pilotPos.rotate(trigAngle)
        miniId=len(self.miniatures)
        m=miniature(p,playerId,battleEngine=self, miniatureId=miniId)
        self.miniatures.append(m)
        self.scene.addItem(m)
        m.setPos(x,y)
        m.doRotate(trigAngle)
        return m
    
    def getMiniatureByName(self,name):
        for i,m in enumerate(self.miniatures):
            if m.pilot.name==name:
                return m
       
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
        print message
    
    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    test=BattleEngine()
    p=defaultPrinter(test)
    #test.readPilots()
    m1=test.addPilotByNameAndCoords("Master Mauricio", 0, 0, 0,1)
    m2=test.addPilotByNameAndCoords("General Leonardo", 0, 10, 0,2)
    #print test.pilots[0].isComplete()
    while len(test.miniatures)>1:
        test.basicAttack(m1,m2)
    #print test.pilots[1].health,test.pilots[1].shield 
    m1.move(m1.pilot.moves[1])
    #for move in test.pilots[0].moves:
    #    print move.name
    #print test.rollAttackDices(10)
    #print test.rollDefenseDices(10)
    #test.savePilots()
    
    #gen = QtSvg.QSvgGenerator()
    sys.exit(app.exec_())
    