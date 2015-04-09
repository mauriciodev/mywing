
import sys, os
import math

dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.split(dirname)[0])
from battleEngine import BattleEngine
#from shipItem import shipItem

from addPilot import addPilot
from PyQt4 import QtGui,  QtSvg, QtCore, uic
from attackAreaItem import attackAreaItem 
from pilotCard import pilotCard


formClass, baseClass = uic.loadUiType(os.path.join(dirname, "battleViewerDialog.ui"))


class BattleViewer(QtGui.QMainWindow, formClass):
    def __init__(self, parent=None,scale=2.5,range=40*2.5):
        super(BattleViewer,self).__init__(parent)
        #QtGui.QMainWindow.__init__(self, parent)
        #Ui_battleViewerDialog.__init__(self, parent)
        self.setupUi(self)
        self.pilotCardWindow=pilotCard(self)
        self.scale=scale
        self.range=range*scale
        #self.connect(self.ui.actionExport, QtCore.SIGNAL('triggered()'), QtCore.SLOT('saveToSvg()'))
        self.newGame()
        self.addBasicSet()
        self.battleEngine.pilotClicked.connect(self.showPilotCard)
        self.graphicsView.installEventFilter(self)
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
        
    def newGame(self):
        self.battleEngine=BattleEngine(self.scale,self.range)
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
        
        
    def addShip(self, x, y, trigAngle, name="novo", playerId=0):
        mini=self.battleEngine.addPilotByNameAndCoords(name,x,y,trigAngle,playerId)
        
                
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
        self.addShip(self.toPixels(-100),self.toPixels(0), -90, "General Leonardo",1)
        #self.addShip(self.toPixels(-45),self.toPixels(10), -1*math.pi/2, "Master Mauricio",1)
        self.addShip(self.toPixels(100), self.toPixels(20), 90, "Darth Philipe",2)
        self.addShip(self.toPixels(100), self.toPixels(-20),90, "Emperor Luiz Claudius",2)
    
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
        window=addPilot()
        window.show()
    def printMessage(self,message):
        self.logTextEdit.append(tr(message))
        


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = BattleViewer()
    #gen = QtSvg.QSvgGenerator()
    myapp.show()
    sys.exit(app.exec_())
        

