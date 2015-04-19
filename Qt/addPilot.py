from PyQt4 import QtGui,  QtSvg, QtCore, uic

import sys, os
import math

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

Ui_addPilotDialog, addPilotClass = uic.loadUiType(os.path.join(basedir, "addPilotDialog.ui"))

class addPilot(QtGui.QDialog, Ui_addPilotDialog):
    def __init__(self, pilotFactory, players, parent=None):
        super(addPilot,self).__init__(parent)
        self.setupUi(self)
        self.pilotFactory=pilotFactory
        self.addPilotsToList()
        self.parent=parent
        self.players=players #dict
        self.playersIds=[]
        self.listPlayers()
        
        
    def addPilotsToList(self):
        self.pilotIds=[]
        self.pilotListWidget.clear()
        self.teamPilotListWidget.clear()
        for p in self.pilotFactory.pilotLibrary.values():
            self.addPilotToList(p)
    def addPilotToList(self,pilot):
        self.pilotIds.append(pilot.id)
        self.pilotListWidget.addItem(pilot.name)
    def selectedPilots(self):
        result=[]
        for i in range(self.teamPilotListWidget.count()):
            item=self.teamPilotListWidget.item(i)
            result.append(self.pilotFactory.getPilotByName(item.text()))
        return result
    
    
    def listPlayers(self):
        self.playerComboBox.clear()
        
        for id,player in self.parent.battleEngine.players.iteritems():
            self.playerComboBox.addItem(player)
            self.playersIds.append(id)
    
    def accept(self, *args, **kwargs):
        QtGui.QDialog.accept(self, *args, **kwargs)
        pilots=self.selectedPilots()
        playerId=self.playersIds[self.playerComboBox.currentIndex()]
        for pilot in pilots:
            self.parent.addShip(pilot.name,playerId)
        return
    def newTeam(self):
        pass
    def eraseTeam(self):
        pass
    def saveTeam(self):
        pass
    def viewPilotCard(self):
        pName=self.pilotListWidget.currentItem().text()
        p=self.pilotFactory.getPilotByName(pName)
        self.parent.showPilotCard(p.id)
    def removeFromTeam(self):
        pass
        #self.teamPilotListWidget.
    def addToTeam(self):
        for item in self.pilotListWidget.selectedItems():
            self.teamPilotListWidget.addItem(item.text())
            
    
    


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = addPilot()
    #gen = QtSvg.QSvgGenerator()
    myapp.show()
    sys.exit(app.exec_())
        

