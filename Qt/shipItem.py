from PyQt4 import QtGui,  QtSvg
from PyQt4.QtCore import *
import math, os
from pilot import pilot

class shipItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, pos, pilot,  parent=None ):
        self.parent=parent
        #QGraphicsRectItem.__init__(self, 0, 0, 100, 50)
        height=150
        width=150
        self.pilot=pilot
        dirname, filename = os.path.split(os.path.abspath(__file__))
        imageFileName=os.path.join(os.path.split(dirname)[0],"images",pilot.ship.name+".png")
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
        self.setTitle(self.pilot.name)
        self.setPosFromBattleEngine(pos)
        
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
        
    def contextMenuEvent(self,event): #QGraphicsSceneContextMenuEvent *
        menu=QtGui.QMenu(self.parent)
        #move=menu.addAction("Move");
        moveMenu=QtGui.QMenu(menu)
        moveMenu.setTitle("&Move")
        menu.addMenu(moveMenu)
        moveActions=[]
        for moveId in self.pilot.ship.moveIds:
            move=self.parent.battleEngine.getMoveById(moveId)
            moveAction=moveMenu.addAction(move.name)
            moveActions.append(moveAction)
        attackMenu=QtGui.QMenu(menu)
        attackMenu.setTitle("&Attack")
        menu.addMenu(attackMenu)
        mainWeaponAction=attackMenu.addAction("Main weapon");
        actionMenu=QtGui.QMenu(menu)
        actionMenu.setTitle("&Perform action")
        menu.addMenu(actionMenu)
        focusAction=actionMenu.addAction("Focus");
        #performAction=menu.addAction("Perform Action");
        #attack=menu.addAction("Attack");
        action = menu.exec_(event.screenPos())
        if action in moveActions: 
            qDebug("User clicked move")
            move=self.parent.battleEngine.getMoveByName(action.text())
            pilotId=self.parent.battleEngine.getActivePilotIdByName(self.pilot.name)
            newPos=self.parent.battleEngine.performMove(pilotId,move)
            self.setPosFromBattleEngine(newPos)
            #self.parent.moveShip(,self)
        if action == mainWeaponAction: 
            qDebug("User clicked attack")
        if action == focusAction: 
            qDebug("User clicked Perform action")