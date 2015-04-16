import json
import random,math
import os,sys

from position import position
from PyQt4.QtCore import QObject, pyqtSignal, QString
from pilotFactory import PilotFactory
from miniature import miniature
from PyQt4 import QtGui,  QtSvg, QtCore
from turnSequencer import turnSequencer
from Qt.tokenFactory import TokenFactory
from Qt.tokenFactory import Token

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.join(os.path.dirname(__file__),'images','scenarios')

class defaultPrinter(QtCore.QObject):
    def __init__(self,battleEngine):
        super(defaultPrinter,self).__init__()
        battleEngine.messagePrinted.connect(self.printMessage)
        battleEngine.pilotDestroyed.connect(self.pilotDestroyed)
    def printMessage(self,s):
        print s
    def pilotDestroyed(self,pilotId):
        self.printMessage("Pilot %i was destroyed." % pilotId)

class BattleEngine(QObject):
    pilotClicked=QtCore.pyqtSignal('int')
    miniatureAttacked=QtCore.pyqtSignal('int','int')
    messagePrinted=pyqtSignal('QString')
    pilotDestroyed=pyqtSignal('int')
    def __init__(self,scale=2.5,shotRange=40*2.5,bounds=[-450,-450,450,450]):
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
        self.bounds=map(lambda x: x*self.scale,bounds)
        self.pilotFactory=PilotFactory(self,self.scale)
        self.scene=QtGui.QGraphicsScene()
        self.tokenFactory=TokenFactory(self.scene,self.scale)
    
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
    
    def getMiniatureById(self,miniId):
        for mini in self.miniatures:
            if mini.miniatureId==miniId:
                return mini
    
    def rollDefenseDices(self,n):
        rollResult={'evade':0,'focus':0,'nothing':0}
        #3 evade 2 focus 3 nothing
        for i in range(0,n):
            result=random.randint(0,7)
            rollResult[self.defenseResults[result]]+=1
        return rollResult
    
    def pilotKilled(self, mini):
        self.pilotDestroyed.emit(mini.miniatureId)
        self.miniatures.pop(self.miniatures.index(mini))
        self.printMessage("Pilot %s was destroyed." % mini.pilot.name)
        self.scene.removeItem(mini)
        self.pilotDestroyed.emit(mini.miniatureId)
    
    def getModifiedAttackDices(self,m1,m2):
        attackRange=m1.range(m2)
        bearing=m1.bearing(m2)
        self.printMessage(m1.pilot.name, "attacked from range %i" % attackRange, "and bearing %i."% bearing)
        attackDices=m1.pilot.attack
        if (attackRange > 0) and (attackRange <=1):
            attackDices+=1
        if attackRange > 3:
            self.printMessage("Out of range. Distance:",attackRange)
            return None
        if (bearing<m1.pilot.attackAngle[0]) or (bearing>m1.pilot.attackAngle[1]):
            self.printMessage("Enemy out of attack angle.")
            return None
        self.printMessage("Attack dices ("+str(attackDices)+"):")
        return attackDices        
    
    def getModifiedDefenseDices(self,m1,m2):
        defenseDices=m2.pilot.defense
        attackRange=m1.range(m2)
        if (attackRange > 2) and (attackRange <=3):
            defenseDices+=1
        self.printMessage("Defense dices("+str(defenseDices)+"):")
        return defenseDices

    def getAttackResults(self,m1,m2):
        attackDices=self.getModifiedAttackDices(m1,m2)
        attackResults=self.rollAttackDices(attackDices)
        self.printMessage(attackResults)
        return attackResults
    
    def getDefenseResults(self,m1,m2):
        defenseDices=self.getModifiedDefenseDices(m1,m2)
        self.printMessage(m2.pilot.name, "tries to avoid the attacks.")
        defenseResults=self.rollDefenseDices(defenseDices)
        self.printMessage(defenseResults)
        return defenseResults

    def computeDamage(self,attackResults, defenseResults,m1,m2):
        attackResults['attack']-=defenseResults['evade']
        #if attack is negative, it lowers criticals too
        if (attackResults['attack']<0): 
            attackResults['critical']+=attackResults['attack']
            attackResults['attack']=0
        if(attackResults['critical']<0): attackResults['critical']=0
        damage=attackResults['attack']+attackResults['critical']
        self.printMessage(m2.pilot.name, "took",attackResults['attack'],"regular hits and", attackResults['critical'], "critical hits.")
        if damage>0: 
            m2.takeDamage(damage)
    
    def basicAttack(self,m1,m2):
        #this is a very basic attack sequence just to test how it should work
        #later on this should be replaced by a well timed sequence
        #i'm ignoring focus right now
        #self.printMessage('')
        attackResults=self.getAttackResults(m1, m2)
        if attackResults!=None: #not out of range or bearing
            defenseResults=self.getDefenseResults(m1, m2)
            #first, lower attack using evade
            self.computeDamage(attackResults, defenseResults, m1, m2)
            self.printMessage(m2.pilot.name, "now has",m2.pilot.shield,"shield and",m2.pilot.health, "health")
            self.printMessage('') 
            self.checkPilot(m2)
    
    def getPlayerName(self,playerId):
        return self.players[playerId]
    
    def getPlayerList(self):
        res=[]
        for player in self.players.values():
            res.append(player)
        return res
    
    def getPlayerStartAngle(self,playerId):
        startAngles=[-90,90,0,180]
        startPos=[(-450,0),(450,0),(0,-450),(0,450)]
        index=self.players.keys().index(playerId)
        return (startAngles[index],startPos[index])
    
    def checkPilot(self,mini):
        if mini.pilot.health<1:
            self.pilotKilled(mini)
    

    def addBorders(self,scenarioName):
        #rect=QtCore.QRect(-1*x/2,-1*y/2,x/2,y/2)
        b=self.bounds
        self.borders=self.scene.addRect(b[0],b[1],b[2]-b[0],b[3]-b[1])
        dirname, filename = os.path.split(os.path.abspath(__file__))
        imageFileName=os.path.join(basedir,scenarioName+".jpg")
        pixmap=QtGui.QPixmap(imageFileName)
        pixmap=pixmap.scaled(b[2]-b[0],b[3]-b[1]);
        self.backgroundPixmap=self.scene.addPixmap(pixmap)
        self.backgroundPixmap.setPos(b[0],b[1])
        self.backgroundPixmap.setZValue(-1)

        
    def addPilotByNameAndCoords(self,name, playerId,x=0,y=0,angle=0):
        if (x==0 and y==0 and angle ==0):
            angle,pos=self.getPlayerStartAngle(playerId)
            x=pos[0]
            y=pos[1]
        p=self.pilotFactory.getPilotByName(name)
        if p==None:
            return p
        x*=self.scale
        y*=self.scale
        #pilotPos=position(x,y)
        #pilotPos.rotate(trigAngle)
        miniId=len(self.miniatures)
        m=miniature(p,playerId,battleEngine=self, miniatureId=miniId, scale=self.scale,rangeDistance=self.shotRange)
        self.miniatures.append(m)
        self.scene.addItem(m)
        m.setPos(x,y)
        m.doRotate(angle)
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
    
    def endTurn(self):
        for mini in self.miniatures:
            mini.endOfTurn()
    
    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    test=BattleEngine()
    p=defaultPrinter(test)
    test.addPlayer("Mauricio")
    test.addPlayer("Leonardo")
    #test.readPilots()
    m1=test.addPilotByNameAndCoords("Master Mauricio", 1)
    
    m2=test.addPilotByNameAndCoords("General Leonardo", 2)
    #print test.pilots[0].isComplete()
    while len(test.miniatures)>1:
        m1.move(m1.pilot.moves[0])
        test.basicAttack(m1,m2)
    #print test.pilots[1].health,test.pilots[1].shield 
    #m1.move(m1.moves[1])
    #for move in test.pilots[0].moves:
    #    print move.name
    #print test.rollAttackDices(10)
    #print test.rollDefenseDices(10)
    #test.savePilots()
    
    #gen = QtSvg.QSvgGenerator()
    sys.exit(app.exec_())
    