from PyQt4 import QtGui,  QtSvg, QtCore
from PyQt4.QtCore import *
import sys, os
import math

dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.split(dirname)[0])
from battleEngine import BattleEngine
from battleViewerDialog import Ui_battleViewerDialog
from shipItem import shipItem
from addPilot import addPilot

class BattleViewer(QtGui.QMainWindow, Ui_battleViewerDialog):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        Ui_battleViewerDialog.__init__(self, parent)
        self.setupUi(self)
        self.scene=QtGui.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
        
        #scale of centimeters to pixels
        self.pixelsPerCentimeter=10./2.
        
        self.battleEngine=BattleEngine()
        self.battleEngine.readPilots()
        #for i in range(0, 100):
        #    self.newDataSourceItem(0, i*10)
        self.statusBar().showMessage('Ready')
        #self.connect(self.ui.actionExport, QtCore.SIGNAL('triggered()'), QtCore.SLOT('saveToSvg()'))
        
        self.addBasicSet()
        #self.addShip(100,100)-1.*x/2.,-1.*y/2.
        #self.addShip(300,100)
 
    def addBorders(self,x,y):
        #rect=QtCore.QRect(-1*x/2,-1*y/2,x/2,y/2)
        self.borders=self.scene.addRect(0,0,x,y)
        self.borders.moveBy(-1.*x/2.,-1.*y/2.)
    def addShip(self, x, y, trigAngle, name="novo", shipName="NewShip"):
        (pilot,pos)=self.battleEngine.addPilotByNameAndCoords(name,x,y,trigAngle)
        self.scene.addItem(shipItem(pos,pilot,parent=self))
        
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
        self.addBorders(self.toPixels(120), self.toPixels(120))
        self.addShip(self.toPixels(-50),self.toPixels(0), -1*math.pi/2, "Luke Skywalker")
        self.addShip(self.toPixels(50), self.toPixels(-10), math.pi/2, "Obsidian squadron pilot")
        self.addShip(self.toPixels(50), self.toPixels(10), math.pi/2, "Night Beast")
    
    def toPixels(self,cm):
        return self.pixelsPerCentimeter*cm
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
        qDebug("Move to where?")
    def attack(self):
        pass
    def performAction(self):
        pass
    def addPilot(self):
        window=addPilot()
        window.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = BattleViewer()
    #gen = QtSvg.QSvgGenerator()
    myapp.show()
    sys.exit(app.exec_())
        

