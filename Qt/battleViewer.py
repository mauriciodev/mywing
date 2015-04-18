
import sys, os
import math
import sys

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

from battleEngine import BattleEngine
#from shipItem import shipItem

from Qt.addPilot import addPilot
from PyQt4 import QtGui,  QtSvg, QtCore, uic
from Qt.attackAreaItem import attackAreaItem 
from Qt.pilotCard import pilotCard
import Qt.scenarioView
from Qt.attack import Attack

formClass, baseClass = uic.loadUiType(os.path.join(basedir, "battleViewerDialog.ui"))


class BattleViewer(QtGui.QMainWindow, formClass):
    def __init__(self, parent=None,scale=2.5,range=40*2.5):
        super(BattleViewer,self).__init__(parent)
        #QtGui.QMainWindow.__init__(self, parent)
        #Ui_battleViewerDialog.__init__(self, parent)
        self.setupUi(self)
        self.pilotCardWindow=pilotCard(self)
        self.attackWindow=Attack(self)
        self.scale=scale
        self.range=range*scale
        #self.connect(self.ui.actionExport, QtCore.SIGNAL('triggered()'), QtCore.SLOT('saveToSvg()'))

        self.newGame()
        self.addBasicSet()
        self.battleEngine.pilotClicked.connect(self.showPilotCard)
        self.battleEngine.miniatureAttacked.connect(self.showAttack)
        #self.graphicsView.scale(5,5)
        #scale of centimeters to pixels
        
        #self.addShip(100,100)-1.*x/2.,-1.*y/2.
        #self.addShip(300,100)
        
    def toggleShowRange(self):
        if self.attackArea.isVisible():
            self.attackArea.hide()
            self.actionRange_ruler.setChecked(False)
        else:
            self.attackArea.show()
            self.actionRange_ruler.setChecked(True)
    
    def showPilotCard(self,pilotId):
        p=self.battleEngine.pilotFactory.getPilotById(pilotId)
        self.pilotCardWindow.showPilotData(p)
        
        
    def newGame(self,players=["My Player 1","My Player 2"]):
        self.battleEngine=BattleEngine(self.scale,self.range)
        for player in players:
            self.battleEngine.addPlayer(player)
        self.graphicsView.setScene(self.battleEngine.scene)
        self.graphicsView.show()
        self.battleEngine.messagePrinted.connect(self.logTextEdit.append)
        self.battleEngine.addBorders('maxresdefault')
        #for i in range(0, 100):
        #    self.newDataSourceItem(0, i*10)
        self.statusBar().showMessage('Ready')
        self.attackArea=attackAreaItem(self,QtCore.QPointF(0,0), self.range)
        self.attackArea.hide()
        self.battleEngine.scene.addItem(self.attackArea)
        
    def newBasicSetGame(self):
        self.newGame()
        self.addBasicSet()
    
    #def pilotDestroyed(self,pilotId):
    #    item=self.getPilotShipItem(pilotId)
    #    self.scene.removeItem(item)
        
        
    def addShip(self, name="novo", playerId=0,x=0,y=0,angle=0):
        mini=self.battleEngine.addPilotByNameAndCoords(name,playerId,x,y,angle)
        
                
    def fileSave(self):
        print("save")
    
    def fileOpen(self):
        print("open")
        
    def export(self):
        fileName,filter = QtGui.QFileDialog.getSaveFileNameAndFilter(self, self.tr("Export diagram"),os.getcwd(), self.tr("Scalable Vector Graphics (*.svg);;Portable Document Files (*.pdf);;all files (*)"))
        if (os.path.exists(os.path.split(str(fileName))[0])):
            if (filter=="Scalable Vector Graphics (*.svg)"):
                self.exportToSvg(str(fileName))
            elif (filter=="Portable Document Files (*.pdf)"):
                self.exportToPdf(str(fileName))
        else:
            print "Folder does not exist"
    def addBasicSet(self):
        self.addShip("Master Mauricio",1,x=-400,y=0,angle=-90)
        #self.addShip(self.toPixels(-45),self.toPixels(10), -1*math.pi/2, "Master Mauricio",1)
        self.addShip("Extra",2,x=400,y=-50,angle=90)
        self.addShip("Extra",2,x=400,y=50,angle=90)
    
    def toPixels(self,cm):
        return self.scale*cm
    def exportToPdf(self,filename):
        printer = QtGui.QPrinter()
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        pdfPainter = QtGui.QPainter(printer)
        self.scene.render(pdfPainter)
        pdfPainter.end()

    def exportToSvg(self, fileName):
        #Dump to SVG
        gen = QtSvg.QSvgGenerator()
        gen.setFileName(fileName)
        gen.setSize(QSize(200, 200))
        svgPainter = QtGui.QPainter(gen)
        self.scene.render(svgPainter)
        svgPainter.end()

    def moveShip(self,move,shipItem):
        self.battleEngine.printMessage("Move to where?")
    def attack(self):
        pass
    def performAction(self):
        pass
    def addPilot(self):
        window=addPilot(pilotFactory=self.battleEngine.pilotFactory,players=self.battleEngine.players,parent=self)
        window.show()
    def printMessage(self,message):
        self.logTextEdit.append(message)
    
    def endOfTurn(self):
        self.battleEngine.endTurn()
    def movementStage(self):
        pass
    
    def attackStage(self):
        pass
    
    def preparationStage(self):
        pass
    def showAttack(self,mini1Id, mini2Id):
        m1=self.battleEngine.getMiniatureById(mini1Id)
        m2=self.battleEngine.getMiniatureById(mini2Id)
        attackResult=self.attackWindow.showAttack(m1,m2)
        if attackResult:
            if (self.attackWindow.attackResults and self.attackWindow.defenseResults):
                self.battleEngine.computeDamage(self.attackWindow.attackResults, self.attackWindow.defenseResults, m1, m2)
                self.battleEngine.printMessage(m2.pilot.name, "now has",m2.pilot.shield,"shield and",m2.pilot.health, "health")
                self.printMessage('') 
                self.battleEngine.checkPilot(m2)
            


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = BattleViewer()
    #gen = QtSvg.QSvgGenerator()
    myapp.show()
    sys.exit(app.exec_())
        

