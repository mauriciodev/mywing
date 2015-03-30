from PyQt4 import QtGui,  QtSvg, QtCore
from PyQt4.QtCore import *
import sys, os
import math

dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.split(dirname)[0])

from addPilotDialog import Ui_addPilotDialog

class addPilot(QtGui.QDialog, Ui_addPilotDialog):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        Ui_addPilotDialog.__init__(self, parent)
        self.setupUi(self)
    def addPilotsToList(self, pilots):
        for p in pilots:
            self.addPilotToList(p)
    def addPilotToList(self,pilot):
        self.pilotListWidget


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = addPilot()
    #gen = QtSvg.QSvgGenerator()
    myapp.show()
    sys.exit(app.exec_())
        

