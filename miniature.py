from PyQt4 import QtGui,  QtSvg
#from PyQt4.QtCore import *
from PyQt4 import QtCore 
import math, os
from pilot import pilot
from Qt.pilotCard import pilotCard
from copy import deepcopy
from Qt.tokenFactory import Token

import sys

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

"""This class represents both the Miniature and everything that you can do with a miniature""" 
class miniature(QtGui.QGraphicsRectItem):
    def __init__(self, pilot,  playerId, battleEngine=None, height=20,width=20, miniatureId=-1,scale=2.5,rangeDistance=2.5*40):
        self.scale=scale
        self.rangeDistance=rangeDistance
        self.battleEngine=battleEngine
        self.rot=0
        #QGraphicsRectItem.__init__(self, 0, 0, 100, 50)
        self.height=height*scale
        self.width=width*scale
        self.pilot=deepcopy(pilot)
        self.playerId=playerId
        self.stressTokens=0
        self.nextMove=None
        self.tokens=[]
        #drawing the base
        super(miniature,self).__init__(0,0,self.width,self.height)
        #QtGui.QGraphicsRectItem.__init__(self,0,0,self.width,self.height)
        brush=QtGui.QBrush(QtGui.QColor(255,255,255,150))
        self.setBrush(brush)
        
        imageFileName=os.path.join(basedir,"images",self.pilot.ship.name+".png")
        if os.path.exists(imageFileName):
            pixmap=QtGui.QPixmap(imageFileName)
            pixmap=pixmap.scaled(self.height,self.width);
            self.shipImage=QtGui.QGraphicsPixmapItem(pixmap,parent=self)#0, 0, width, height)
            self.shipImage.setZValue(1)
        
        #self.separator1=QtGui.QGraphicsLineItem( 6, 17, width-6, 17, self )
        #self.sidebar1=QtGui.QGraphicsLineItem( 6, 0, 6, height, self )
        #self.sidebar2=QtGui.QGraphicsLineItem( width-6, 0, width-6, height, self )
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.items=[]
        self.miniatureId=miniatureId
        self.textStyleSheet="QLabel { background-color : red; color : blue; }"
        #self.rotate(math.degrees(trigAngle))
        #self.moveBy(x, y)
        self.setTitle(self.getMiniatureName())
        
        #self.setPosFromBattleEngine(self.pilot.position)
        self.makePopupMenu() #creates a menu for that pilot
        self.addPilotData()
        
    def doRotate(self,rotation):
        self.rot+=rotation
        transform = QtGui.QTransform()
        center=self.getCenter()
        transform.translate( center.x(),center.y())
        transform.rotate( -self.rot )
        transform.translate( -1*center.x(), -1*center.y() )
        self.setTransform( transform )
        

    def getPos(self):
        return self.pos()
        
    def getCenter(self):
        return QtCore.QPointF(self.boundingRect().width()/2, self.boundingRect().height()/2)
        
    def addPilotData(self):
        textYpos=self.height/2
        textXstep=12
        textXpos=-2
        self.pilotData=[]
        #attack
        attributes=[self.pilot.attack,self.pilot.defense,self.pilot.shield,self.pilot.health]
        colors=[QtGui.QColor(255,0,0),QtGui.QColor(0,255,0),QtGui.QColor(100,100,255), QtGui.QColor(255,255,0)]
        font=QtGui.QFont()
        font.setBold(True)
        for color,at in zip(colors,attributes):
            self.pilotData.append(QtGui.QGraphicsTextItem(str(at), parent=self))
            self.pilotData[-1].setFont(font)
            self.pilotData[-1].setDefaultTextColor(color)
            self.pilotData[-1].setPos(textXpos,textYpos)
            textXpos+=textXstep
            self.pilotData[-1].setZValue(2)
        #skill
        self.pilotData.append(QtGui.QGraphicsTextItem(str(self.pilot.skillLevel), parent=self))
        self.pilotData[-1].setPos(-2,-4)
        font.setPointSize(font.pointSize()+2)
        self.pilotData[-1].setFont(font)
        self.pilotData[-1].setZValue(2)
        #self.pilotData.append(QtGui.QGraphicsTextItem(str(self.pilot.skillLevel), parent=self))
        #self.pilotData[-1].setDefaultTextColor(QtGui.QColor(1,1,0))
        #self.pilotData[-1].moveBy(self.width-5*self.scale, self.height-5*self.scale)
    
    def setMiniatureShield(self,value):
        self.pilotData[2].setPlainText(str(value))
    def setMiniatureHealth(self,value):
        self.pilotData[3].setPlainText(str(value))
    
    def getSize(self):
        #this is useless. I may be ditching this soon.
        x=self.pixelsPerCentimeters*self.width
        y=self.pixelsPerCentimeters*self.height
        return self.pilot.position.rotateVector(x,y,self.pilot.position.getRotation())
        
        

    def setTitle(self, label):
        self.title=QtGui.QGraphicsTextItem(str(label), parent=self)
        xPos=-self.title.boundingRect().width()/2+self.width/2
        self.title.setDefaultTextColor(QtGui.QColor(1,1,0))
        #self.items[-1].setTextInteractionFlags(Qt.TextEditorInteraction)
        self.title.moveBy(xPos, -self.height/2-1)
        
    def addAttribute(self, label):
        self.items.append(QtGui.QGraphicsTextItem(label, self))
        self.items[-1].moveBy(6, (len(self.items))*14)
        
      
        
    def getPilot(self):
        return self.pilot
    
    def chooseMove(self,move):
        self.nextMove=move
    
    def move(self,move):
        #print self.getPos()
        move.performMove(self)
        cost=self.getMoveCost(move)
        if cost==2:
            self.addStressToken()
        if cost==0:
            self.remStressToken()
        self.nextMove=None
        #print self.getPos()
    
    def getMoveCost(self,move):
        return self.pilot.getMoveCost(move.name)
    
    def contextMenuEvent(self,event): #QGraphicsSceneContextMenuEvent *
        self.makeMainWeaponMenu()
        action = self.menu.exec_(event.screenPos())
        if action in self.moveActions: 
            #qDebug("User clicked move")
            self.battleEngine.printMessage(self.battleEngine.getPlayerName(self.playerId),"chose",self.pilot.name+'\'s next move.')
            move=self.pilot.getMoveByName(action.text())
            self.chooseMove(move)
            #newPos=self.battleEngine.performMove(self,move)
            #self.setPosFromBattleEngine(newPos)
            #self.parent.moveShip(,self)
        if action ==self.actionPerformMove:
            if self.nextMove==None:
                self.battleEngine.printMessage(self.battleEngine.getPlayerName(self.playerId), " didn't choose a move for this unit.")
            else:
                self.battleEngine.printMessage(self.battleEngine.getPlayerName(self.playerId),"performed" ,self.nextMove.name)
                self.move(self.nextMove)
        if action in self.mainWeaponAttackActions:
            miniId=int(str(action.text()).split(":")[0])
            targetMiniature=self.battleEngine.getMiniatureById(miniId)
            self.battleEngine.basicAttack(self,targetMiniature)
            #qDebug("User clicked attack")
        if action == self.actionFocus: 
            self.battleEngine.printMessage("User clicked Perform action")
        if action == self.actionPilotCard:
            self.battleEngine.pilotClicked.emit(self.pilot.id)

    
    def getMiniatureName(self):
        return str(self.miniatureId)+': '+self.pilot.name
    
    def makePopupMenu(self):
        self.menu=QtGui.QMenu()
        self.menu.addAction(self.battleEngine.getPlayerName(self.playerId))
        self.menu.addSeparator()
        self.actionPilotCard=self.menu.addAction(self.getMiniatureName())
        self.menu.addSeparator()
        #move=menu.addAction("Move");
        moveMenu=QtGui.QMenu(self.menu)
        moveMenu.setTitle("&Move")
        self.menu.addMenu(moveMenu)
        self.moveActions=[]
        for move in self.pilot.moves:
            cost=self.getMoveCost(move)
            moveAction=QtGui.QWidgetAction(moveMenu)
            moveAction.setText(move.name)
            
            if cost==0:
                font=moveAction.font()
                font.setItalic(True)
                moveAction.setFont(font)
            if cost==2:
                font=moveAction.font()
                font.setBold(True)
                moveAction.setFont(font)
            moveMenu.addAction(moveAction)
            self.moveActions.append(moveAction)
        self.actionPerformMove=self.menu.addAction("Perform move")
        
        attackMenu=QtGui.QMenu(self.menu)
        attackMenu.setTitle("&Attack")
        self.menu.addMenu(attackMenu)
        self.mainWeaponMenu=QtGui.QMenu(attackMenu)
        self.mainWeaponMenu.setTitle("&Main weapon")
        attackMenu.addMenu(self.mainWeaponMenu)
        #self.actionsActions=[]
        actionMenu=QtGui.QMenu(self.menu)
        actionMenu.setTitle("&Perform action")
        self.menu.addMenu(actionMenu)
        self.actionFocus=actionMenu.addAction("Focus");
        #performAction=menu.addAction("Perform Action");
        #attack=menu.addAction("Attack");
    def makeMainWeaponMenu(self):
        self.mainWeaponAttackActions=[]
        self.mainWeaponMenu.clear()
        
        for mini in self.battleEngine.miniatures:
            if (mini.playerId!=self.playerId):
                mainWeaponAction=self.mainWeaponMenu.addAction(mini.getMiniatureName());
                self.mainWeaponAttackActions.append(mainWeaponAction)
        
    def distance(self,mini):
        vDist=QtGui.QVector2D(self.pos()-mini.pos())
        return vDist.length()
    
    def bearing(self,mini):
        d=self.distance(mini)
        vDist=QtGui.QVector2D(mini.pos()-self.pos())
        dot=self.scalarProduct(vDist,self.getUnitVector())
        if vDist.length()==0: return 0
        cosTheta=dot/vDist.length()
        bearing=math.acos(cosTheta)
        cross=self.crossProduct(vDist,self.getUnitVector())
        if abs(cross)!=0.:
            sign=cross/abs(cross)
        else: sign=1.
        return math.degrees(bearing*sign)
    
    def range(self,mini):
        d=self.distance(mini)
        range=math.ceil(d/self.rangeDistance)
        return range
    
    def isInRange(self,mini):
        range=self.range(mini)
        bearing=self.getBearing(mini)
        if (range<3) and (True):
            return True
        else:
            return False
    def getUnitVector(self):
        angle=math.radians(self.rot+90)
        return QtGui.QVector2D(math.cos(angle),-1*math.sin(angle))
        
    def crossProduct(self,v1,v2):
        return v1.x()*v2.y()-v1.y()*v2.x()
    
    def scalarProduct(self,v1,v2):
        return v1.x()*v2.x()+v1.y()*v2.y()
    
    def takeDamage(self,n):
        self.pilot.takeDamage(n)
        self.setMiniatureHealth(self.pilot.health)
        self.setMiniatureShield(self.pilot.shield)
    
    def getNextTokenPos(self):
        tokenCount=len(self.tokens)
        x=y=0
        if tokenCount<=3:
            x=-20
            y=tokenCount*15
        if tokenCount >3 and tokenCount<= 7:
            y= 56
            x=-20+tokenCount*15
        if tokenCount > 7 :
            x= 50
            y=60-tokenCount*15
        return (x,y)
    
    def addStressToken(self):
        tokenPos=self.getNextTokenPos()
        self.tokens.append(self.battleEngine.tokenFactory.newToken(self, "Stress",tokenPos[0],tokenPos[1]))
        for move,moveAction in zip(self.pilot.moves,self.moveActions):
            cost=self.getMoveCost(move)
            if cost==2:
                moveAction.setEnabled(False)
    
    def hasStressToken(self):
        for token in self.tokens:
            if token.getTokenType()=='Stress':
                return token
        return None
    
    
    def remStressToken(self):
        token=self.hasStressToken()
        if token!=None:
            self.removeToken(token.tokenId)
            self.tokens.pop(self.tokens.index(token))
        if self.hasStressToken()==None:
            #activates the cost 2 moves
            for move,moveAction in zip(self.pilot.moves,self.moveActions):
                cost=self.getMoveCost(move)
                if cost==2:
                    moveAction.setEnabled(True)
            
    def removeToken(self,tokenId):
        for item in self.childItems():
            if type(item) is Token:
                if item.tokenId==tokenId:
                    self.battleEngine.scene.removeItem(item)
                    return        