 
from Qt.battleViewer import BattleViewer
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)
myapp = BattleViewer()
#gen = QtSvg.QSvgGenerator()
myapp.show()
sys.exit(app.exec_())