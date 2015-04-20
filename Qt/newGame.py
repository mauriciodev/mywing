import sys, os
import math
import sys

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

from PyQt4 import QtGui, QtCore, uic

formClass, baseClass = uic.loadUiType(os.path.join(basedir, "newGame.ui"))
from player import Player

class NewGame(QtGui.QDialog, formClass):
    def __init__(self, parent=None):
        super(NewGame,self).__init__(parent) 
        self.setupUi(self)
        self.setupComboBoxes()
    def setupComboBoxes(self):
        aux=Player("aux")
        for item in aux.getAvailablePlayerTypes():
            self.p1TypeComboBox.addItem(item)
            self.p2TypeComboBox.addItem(item)
        for item in aux.getAvailableFactions():
            self.p1FactionComboBox.addItem(item)
            self.p2FactionComboBox.addItem(item)
    
    #def accept(self):
    #    return True
        #formClass.accept(self)
        
    def getPlayers(self):
        p1=Player(str(self.p1NameLineEdit.text()))
        p1.setFaction(p1.getAvailableFactions()[self.p1FactionComboBox.currentIndex()])
        p1.setPlayerType(p1.getAvailablePlayerTypes()[self.p1TypeComboBox.currentIndex()])
        p2=Player(str(self.p2NameLineEdit.text()))
        p2.setFaction(p2.getAvailableFactions()[self.p2FactionComboBox.currentIndex()])
        p2.setPlayerType(p2.getAvailablePlayerTypes()[self.p2TypeComboBox.currentIndex()])
        return [p1,p2]
        