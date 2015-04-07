from PyQt4 import QtGui,  QtSvg
#from PyQt4.QtCore import *
from PyQt4 import QtCore 
import math, os
from pilot import pilot

class miniature(QtGui.QGraphicsPixmapItem):
    def __init__(self, pilot,  playerId, battleEngine=None, height=20,width=20, miniatureId=-1,scale=2.5,rangeDistance=2.5*40):
        self.scale=scale
        self.rangeDistance=rangeDistance*scale
        self.battleEngine=battleEngine
        self.rot=0
        #QGraphicsRectItem.__init__(self, 0, 0, 100, 50)
        self.height=height
        self.width=width
        self.pilot=pilot
        self.playerId=playerId
        dirname, filename = os.path.split(os.path.abspath(__file__))
        imageFileName=os.path.join(dirname,"images",self.pilot.ship.name+".png")
        pixmap=QtGui.QPixmap(imageFileName)
        pixmap=pixmap.scaled(height*self.scale,width*self.scale);
        QtGui.QGraphicsPixmapItem.__init__(self, pixmap)#0, 0, width, height)
        
        #self.separator1=QtGui.QGraphicsLineItem( 6, 17, width-6, 17, self )
        #self.sidebar1=QtGui.QGraphicsLineItem( 6, 0, 6, height, self )
        #self.sidebar2=QtGui.QGraphicsLineItem( width-6, 0, width-6, height, self )
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.items=[]
        self.miniatureId=miniatureId
        self.textStyleSheet="QLabel { background-color : red; color : blue; }"
        #self.rotate(math.degrees(trigAngle))
        #self.moveBy(x, y)
        self.setTitle(self.pilot.name)
        self.setMiniatureIdLabel()
        #self.setPosFromBattleEngine(self.pilot.position)
        self.makePopupMenu() #creates a menu for that pilot
        
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
        
    def getSize(self):
        #this is useless. I may be ditching this soon.
        x=self.pixelsPerCentimeters*self.width
        y=self.pixelsPerCentimeters*self.height
        return self.pilot.position.rotateVector(x,y,self.pilot.position.getRotation())
        
        
    def setPosFromBattleEngine(self,position):
        self.setPos(QPointF(position.x-self.width/2,-1*position.y+self.height/2))
        rotation=math.degrees(position.getRotation())
        #print rotation
        self.setRotation(rotation)

    def setTitle(self, label):
        self.title=QtGui.QGraphicsTextItem(str(label), parent=self)
        self.title.setDefaultTextColor(QtGui.QColor(1,1,0))
        #self.items[-1].setTextInteractionFlags(Qt.TextEditorInteraction)
        self.title.moveBy(-25, -25)
        
    def addAttribute(self, label):
        self.items.append(QtGui.QGraphicsTextItem(label, self))
        self.items[-1].moveBy(6, (len(self.items))*14)
        
    def setMiniatureIdLabel(self):
        self.miniatureIdLabel=QtGui.QGraphicsTextItem(str(self.miniatureId), parent=self)
        self.miniatureIdLabel.setPos(0,0)
        
    def getPilot(self):
        return self.pilot
    
    def move(self,move):
        print self.getPos()
        move.performMove(self)
        print self.getPos()
    
    def contextMenuEvent(self,event): #QGraphicsSceneContextMenuEvent *
        self.makeMainWeaponMenu()
        action = self.menu.exec_(event.screenPos())
        if action in self.moveActions: 
            #qDebug("User clicked move")
            self.battleEngine.printMessage("Player",self.playerId,"performed" ,action.text())
            move=self.pilot.getMoveByName(action.text())
            self.move(move)
            #newPos=self.battleEngine.performMove(self,move)
            #self.setPosFromBattleEngine(newPos)
            #self.parent.moveShip(,self)
        if action in self.mainWeaponAttackActions:
            miniId=int(str(action.text()).split(":")[0])
            targetMiniature=self.battleEngine.miniatures[miniId]
            self.battleEngine.basicAttack(self,targetMiniature)
            #qDebug("User clicked attack")
        if action == self.focusAction: 
            self.battleEngine.printMessage("User clicked Perform action")
            
    def makePopupMenu(self):
        self.menu=QtGui.QMenu()
        self.menu.addAction("Player "+str(self.playerId))
        self.menu.addSeparator()
        #move=menu.addAction("Move");
        moveMenu=QtGui.QMenu(self.menu)
        moveMenu.setTitle("&Move")
        self.menu.addMenu(moveMenu)
        self.moveActions=[]
        for move in self.pilot.moves:
            cost=self.pilot.getMoveCost(move.name)
            moveAction=QtGui.QWidgetAction(moveMenu)
            moveAction.setText(move.name)
            
            #moveAction=moveMenu.addAction(move.name)
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
        self.focusAction=actionMenu.addAction("Focus");
        #performAction=menu.addAction("Perform Action");
        #attack=menu.addAction("Attack");
    def makeMainWeaponMenu(self):
        self.mainWeaponAttackActions=[]
        self.mainWeaponMenu.clear()
        
        for mini in self.battleEngine.miniatures:
            if (mini.playerId!=self.playerId):
                mainWeaponAction=self.mainWeaponMenu.addAction(str(mini.miniatureId)+": "+mini.pilot.name);
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
        cross=self.crossProdutc(vDist,self.getUnitVector())
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
        
    def crossProdutc(self,v1,v2):
        return v1.x()*v2.y()-v1.y()*v2.x()
    
    def scalarProduct(self,v1,v2):
        return v1.x()*v2.x()+v1.y()*v2.y()