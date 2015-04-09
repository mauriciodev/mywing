
import sys, os
import math

from PyQt4 import QtGui,  QtSvg, QtCore, uic

from pilot import pilot

class pilotCard(QtGui.QDialog):
    def __init__(self, parent = None):
        super(pilotCard, self).__init__(parent)
        dirname, filename = os.path.split(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname,'pilotCard.ui'), self)
        self.scene=QtGui.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        #self.miniature=mini
    def showPilotData(self,pilot):
        #self.groupBox_2.setTitle(str(pilot.name))
        self.scene.clear()
        self.skillLabel.setText(str(pilot.skillLevel))
        self.attackLabel.setText(str(pilot.attack))
        self.evadeLabel.setText(str(pilot.defense))
        self.shieldLabel.setText(str(pilot.shield))
        self.healthLabel.setText(str(pilot.health))
        #loading ship image
        dirname, filename = os.path.split(os.path.abspath(__file__))
        imageFileName=os.path.join(os.path.split(dirname)[0],"images",pilot.ship.name+".png")
        #pixmap=QtGui.QPixmap(imageFileName)
        if os.path.exists(imageFileName):
            pixmap=QtGui.QPixmap(imageFileName)
            pixmap=pixmap.scaled(100,100)
            self.shipImage=QtGui.QGraphicsPixmapItem(pixmap,parent=None,scene=self.scene)#0, 0, width, height)
            self.shipImage.setZValue(1)
        self.setWindowTitle(pilot.name)
        #pixmap=pixmap.scaled(120,120);
        #shipLabel=QtGui.QLabel(self.groupBox)
        #shipLabel.setPixmap(pixmap)
        
        #self.shipImage=QtGui.QGraphicsPixmapItem(pixmap,self.groupBox)
        self.groupBox.setTitle(str(pilot.ship.name))
        self.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    card = pilotCard()
    
    p=pilot()
    card.showPilotData(p)
    #gen = QtSvg.QSvgGenerator()
    #myapp.show()
    sys.exit(app.exec_())
        

