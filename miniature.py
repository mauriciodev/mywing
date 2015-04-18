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
    basedir = os.path.join(os.path.dirname(__file__),'images')

"""This class represents both the Miniature and everything that you can do with a miniature""" 
class miniature(QtGui.QGraphicsRectItem):
    def __init__(self, pilot,  playerId, battleEngine=None, miniatureId=-1,scale=2.5,rangeDistance=2.5*40):
        self.scale=scale
        self.rangeDistance=rangeDistance
        self.battleEngine=battleEngine
        self.rot=0
        #QGraphicsRectItem.__init__(self, 0, 0, 100, 50)
        self.pilot=deepcopy(pilot)
        self.height=self.pilot.ship.sizeY*scale
        self.width=self.pilot.ship.sizeX*scale
        self.playerId=playerId
        self.stressTokens=0
        self.nextMove=None
        self.tokens=[None]*9 #the token list has at most 9 tokens. 
        #drawing the base
        super(miniature,self).__init__(0,0,self.width,self.height)
        #QtGui.QGraphicsRectItem.__init__(self,0,0,self.width,self.height)
        brush=QtGui.QBrush(QtGui.QColor(255,255,255,150))
        self.setBrush(brush)
        
        imageFileName=os.path.join(basedir,self.pilot.ship.name+".png")
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
        self.actionEvade=None
        self.actionEvade=None
        self.actionBarrelRoll=None
        self.endOfTurn()

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
        textYpos=self.height-10*self.scale
        textXstep=10*self.scale
        textXpos=3*self.scale
        self.pilotData=[]
        #attack
        attributes=[self.pilot.attack,self.pilot.defense,self.pilot.shield,self.pilot.health]
        colors=[QtGui.QColor(255,0,0),QtGui.QColor(0,255,0),QtGui.QColor(100,100,255), QtGui.QColor(255,255,0)]
        font=QtGui.QFont()
        font.setBold(True)
        font.setPointSize(22)
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
        
    def barrelRoll(self):
        self.battleEngine.printMessage("Barrel roll")
    
    def getMoveCost(self,move):
        return self.pilot.getMoveCost(move.name)
    
    def contextMenuEvent(self,event): #QGraphicsSceneContextMenuEvent *
        self.makeMainWeaponMenu()
        self.makeTargetLockMenu()
        action = self.menu.exec_(event.screenPos())
        if action != None:
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
                #targetMiniature=self.battleEngine.getMiniatureById(miniId)
                #self.battleEngine.basicAttack(self,targetMiniature)
                self.battleEngine.miniatureAttacked.emit(self.miniatureId, miniId)
                #qDebug("User clicked attack")
               
            if action in self.targetLockActions:
                miniId=int(str(action.text()).split(":")[0])
                targetMiniature=self.battleEngine.getMiniatureById(miniId)
                self.addTargetLockerToken(targetMiniature)
            if action == self.actionPilotCard:
                self.showPilotCard()

    
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
        
        self.mainWeaponMenu=QtGui.QMenu(self.menu)
        self.mainWeaponMenu.setTitle("&Attack: Main weapon")
        self.menu.addMenu(self.mainWeaponMenu)
        #self.actionsActions=[]
        actionMenu=QtGui.QMenu(self.menu)
        
        #Adding actions
        self.availableActions={}
        actionMenu.setTitle("&Perform action")
        self.menu.addMenu(actionMenu)
        focusAction=actionMenu.addAction("Focus")
        focusAction.triggered.connect(self.addFocusToken)
        if self.pilot.hasAction("Evade"):
            evadeAction=actionMenu.addAction("Evade")
            evadeAction.triggered.connect(self.addEvadeToken)
        if self.pilot.hasAction("Barrel roll"):
            barrelRollAction=actionMenu.addAction("Barrel roll")
            barrelRollAction.triggered.connect(self.performBarrelRoll)
        if self.pilot.hasAction("Target Lock"):
            self.menuTargetLock=QtGui.QMenu(actionMenu)
            self.menuTargetLock.setTitle("Target Lock")
            actionMenu.addMenu(self.menuTargetLock)
        #performAction=menu.addAction("Perform Action");
        #attack=menu.addAction("Attack");
    def makeMainWeaponMenu(self):
        self.mainWeaponAttackActions=[]
        self.mainWeaponMenu.clear()
        
        for mini in self.battleEngine.miniatures:
            if (mini.playerId!=self.playerId):
                mainWeaponAction=self.mainWeaponMenu.addAction(mini.getMiniatureName());
                self.mainWeaponAttackActions.append(mainWeaponAction)
    
        
    
    def makeTargetLockMenu(self):
        #TO DO:Should check if player can target lock
        self.targetLockActions=[]
        if self.pilot.hasAction("Target Lock"):
            self.menuTargetLock.clear()
            
            for mini in self.battleEngine.miniatures:
                if (mini.playerId!=self.playerId):
                    targetLockAction=self.menuTargetLock.addAction(mini.getMiniatureName())
                    self.targetLockActions.append(targetLockAction)
        
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
        #TO DO: Modify this with ship's geometry
        d=self.distance(mini)
        #Computing the circle (NOT THE SQUARE) radius. This should be changed later.
        #r=math.sqrt((self.height/2)**2+(self.width/2)**2)
        r=(self.height+self.width)/4
        #reducing the distance because the borders should be he real value
        d-=2*r 
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
        x=y=0
        nextTokenId=0
        #looking for empty spaces
        i=self._findIndexOfFirstEmptyTokenSlot()
        #found an empty space
        if i>=0:
            nextTokenId=i
        else: 
            return
        if nextTokenId<3:
            x=-15*self.battleEngine.scale
            y=nextTokenId*15*self.battleEngine.scale
        if nextTokenId >=3 and nextTokenId< 6:
            y= 40*self.battleEngine.scale
            x=(-2(nextTokenId-3)*15)*self.battleEngine.scale
        if nextTokenId >= 6 :
            x= 40*self.battleEngine.scale
            y=(30-(nextTokenId-6)*15)*self.battleEngine.scale
        return (x,y)
    
    
    def _addTokenByType(self, tokenType):
        tokenPos=self.getNextTokenPos()
        token=self.battleEngine.tokenFactory.newToken(self, tokenType,tokenPos[0],tokenPos[1])
        self._addToken(token)
    
    def _findIndexOfFirstEmptyTokenSlot(self):
        for i in range(0,len(self.tokens)):
            if self.tokens[i]==None:
                return i 
        return -1
    
    def _findTokenIndexByType(self, tokenType):
        #you can use this to find the first empty slot too
        for i in range(0,len(self.tokens)):
            if self.tokens[i]!=None:
                if self.tokens[i].getTokenType()==tokenType:
                    return i
        return -1
    
    def _addToken(self,token):
        i=self._findIndexOfFirstEmptyTokenSlot()
        if i>len(self.tokens):
            print "More than 9 tokens were added."
        else: 
            self.tokens[i]=token

    
    def addStressToken(self):
        self._addTokenByType("Stress")
        for move,moveAction in zip(self.pilot.moves,self.moveActions):
            cost=self.getMoveCost(move)
            if cost==2:
                moveAction.setEnabled(False)
    def addFocusToken(self):
        self._addTokenByType("Focus")
        
    def addEvadeToken(self):
        self._addTokenByType("Evade")
        
    def addTargetLockerToken(self,targetMiniature):
        tokenPos=self.getNextTokenPos()
        token=self.battleEngine.tokenFactory.newTargetLockerToken(self, tokenPos[0],tokenPos[1],targetMiniature.miniatureId)
        self._addToken(token)
        targetMiniature.addTargetLockedToken(self)
        
    def addTargetLockedToken(self,targeteerMiniature):
        tokenPos=self.getNextTokenPos()
        token=self.battleEngine.tokenFactory.newTargetLockedToken(self, tokenPos[0],tokenPos[1],targeteerMiniature.miniatureId)
        self._addToken(token)
    
    def _hasToken(self,tokenName):
        for token in self.tokens:
            if token!=None:
                if token.getTokenType()==tokenName:
                    return token
        return None
    
    def hasStressToken(self):
        return self._hasToken("Stress")
    
    def hasFocusToken(self):
        return self._hasToken("Focus")
    
    #def hasTargetLockerToken(self):
    #    return self._hasToken("Target_Locker")
    
    #def hasTargetLockedToken(self):
    #    return self._hasToken("Target_Locked")
        
    def hasEvadeToken(self):
        return self._hasToken("Evade")
    
    def _remToken(self,tokenType):
        tokenIndex=self._findTokenIndexByType(tokenType)
        if tokenIndex>=0:
            self._remTokenById(self.tokens[tokenIndex].tokenId)
            self.tokens[tokenIndex]=None
        
    def checkAvailableActions(self):
        self.actionsToPerform-=1
        if self.actionsToPerform==0:
            #deactivates actions until next turn
            pass
            
        
    
    def remStressToken(self):
        self._remToken("Stress")
        if self.hasStressToken()==None:
            #activates the cost 2 moves
            for move,moveAction in zip(self.pilot.moves,self.moveActions):
                cost=self.getMoveCost(move)
                if cost==2:
                    moveAction.setEnabled(True)
       
    def remEvadeToken(self):
        self._remToken("Evade")
       
    def remFocusToken(self):
        self._remToken("Focus")
       
    def remTargetLockToken(self,targetMiniId):
        self._remTargetLockerToken(targetMiniId)
        self.battleEngine.getMiniatureById(targetMiniId)._remTargetLockedToken(self.miniatureId)
        
    def hasTargetLockerToken(self, targetMiniId):
        #Target Locks have target Miniatures so I can't remove any TL token. It must be that one.
        for token in self.tokens:
            if token != None:
                if token.getTokenType()=="Target_Locker":
                    if token.TargetMiniatureId==targetMiniId:
                        return token
        return None
    
    def _remTargetLockerToken(self,miniId):
        #Target Locks have target Miniatures so I can't remove any TL token. It must be that one.
        TLToken=self.hasTargetLockerToken(miniId)
        if TLToken!=None:
            self._remTokenById(TLToken.tokenId)
            self.tokens[self.tokens.index(TLToken)]
    
    def hasTargetLockedToken(self,targeteerMiniId=-1):
        #use -1 to check for any miniature
        for token in self.tokens:
            if token != None:
                if token.getTokenType()=="Target_Locked":
                    if (token.TargetMiniatureId==targeteerMiniId) or (targeteerMiniId==-1): 
                        return token
        return None        
    
    def _remTargetLockedToken(self,miniId):
        #Target Locks have target Miniatures so I can't remove any TL token. It must be that one.
        TLToken=self.hasTargetLockedToken(miniId)
        if TLToken!=None:
            self._remTokenById(TLToken.tokenId)
            self.tokens[self.tokens.index(TLToken)]=None
            
    def _remTokenById(self,tokenId):
        for item in self.childItems():
            if type(item) is Token:
                if item.tokenId==tokenId:
                    self.battleEngine.scene.removeItem(item)
                    return        
    
    def performBarrelRoll(self):
        print "Not Implemented"
    
    def showPilotCard(self):
        self.battleEngine.pilotClicked.emit(self.pilot.id)
    
    def endOfTurn(self):
        self.actionsToPerform=1
        while self.hasFocusToken()!=None:
            self.remFocusToken()
        while self.hasEvadeToken()!=None:
            self.remEvadeToken()
            
    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.showPilotCard()
        return QtGui.QGraphicsRectItem.mouseDoubleClickEvent(self, *args, **kwargs)