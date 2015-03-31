from PyQt4 import QtGui,  QtSvg
from PyQt4.QtCore import *
import math, os
from pilot import pilot

class shipItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, pilotBattleId,  parent=None ):
        self.parent=parent
        #QGraphicsRectItem.__init__(self, 0, 0, 100, 50)
        height=150
        width=150
        self.pilotBattleId=pilotBattleId
        dirname, filename = os.path.split(os.path.abspath(__file__))
        pilot=self.getPilot()
        imageFileName=os.path.join(os.path.split(dirname)[0],"images",self.getPilot().ship.name+".png")
        pixmap=QtGui.QPixmap(imageFileName)
        pixmap=pixmap.scaled(50,50);
        QtGui.QGraphicsPixmapItem.__init__(self, pixmap)#0, 0, width, height)
        #self.separator1=QtGui.QGraphicsLineItem( 6, 17, width-6, 17, self )
        #self.sidebar1=QtGui.QGraphicsLineItem( 6, 0, 6, height, self )
        #self.sidebar2=QtGui.QGraphicsLineItem( width-6, 0, width-6, height, self )
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.items=[]
        
        #self.rotate(math.degrees(trigAngle))
        #self.moveBy(x, y)
        self.setTitle(self.getPilot().name)
        self.setPosFromBattleEngine(self.getPilot().position)
        self.makePopupMenu() #creates a menu for that pilot
        
    def setPosFromBattleEngine(self,position):
        self.setPos(QPointF(position.x,-1*position.y))
        rotation=math.degrees(position.getRotation())
        print rotation
        self.setRotation(rotation)

    def setTitle(self, label):
        self.title=self.items.append(QtGui.QGraphicsTextItem(str(label), parent=self))
        self.items[-1].setTextInteractionFlags(Qt.TextEditorInteraction)
        self.items[-1].moveBy(-25, -25)
        
    def addAttribute(self, label):
        self.items.append(QtGui.QGraphicsTextItem(label, self))
        self.items[-1].setTextInteractionFlags(Qt.TextEditorInteraction)
        self.items[-1].moveBy(6, (len(self.items))*14)
        
    def getPilot(self):
        return self.parent.battleEngine.pilots[self.pilotBattleId]
    
    def contextMenuEvent(self,event): #QGraphicsSceneContextMenuEvent *
        action = self.menu.exec_(event.screenPos())
        if action in self.moveActions: 
            #qDebug("User clicked move")
            move=self.getPilot().getMoveByName(action.text())
            newPos=self.parent.battleEngine.performMove(self.getPilot().battleId,move.id)
            self.setPosFromBattleEngine(newPos)
            #self.parent.moveShip(,self)
        if action == self.mainWeaponAction: 
            qDebug("User clicked attack")
        if action == self.focusAction: 
            qDebug("User clicked Perform action")
    def makePopupMenu(self):
        self.menu=QtGui.QMenu(self.parent)
        #move=menu.addAction("Move");
        moveMenu=QtGui.QMenu(self.menu)
        moveMenu.setTitle("&Move")
        self.menu.addMenu(moveMenu)
        self.moveActions=[]
        for move in self.getPilot().moves:
            cost=self.getPilot().getMoveCost(move.name)
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
        self.mainWeaponAction=attackMenu.addAction("Main weapon");
        actionMenu=QtGui.QMenu(self.menu)
        actionMenu.setTitle("&Perform action")
        self.menu.addMenu(actionMenu)
        self.focusAction=actionMenu.addAction("Focus");
        #performAction=menu.addAction("Perform Action");
        #attack=menu.addAction("Attack");
        