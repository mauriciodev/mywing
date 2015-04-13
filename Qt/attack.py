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

formClass, baseClass = uic.loadUiType(os.path.join(basedir, "attack.ui"))


class Attack(QtGui.QDialog, formClass):
    def __init__(self, parent=None):
        super(Attack,self).__init__(parent)
        self.parent=parent
        self.setupUi(self)


    def showAttack(self,attackingMiniature,defendingMiniature):
        self.attackingMiniature=attackingMiniature
        self.defendingMiniature=defendingMiniature
        self.attackUnitLineEdit.setText(attackingMiniature.getMiniatureName())
        self.attackShipLineEdit.setText(attackingMiniature.pilot.ship.name)
        self.attackSpinBox.setValue(attackingMiniature.pilot.attack)
        self.evadeSpinBox.setValue(defendingMiniature.pilot.defense)
        self.defenseUnitLineEdit.setText(defendingMiniature.getMiniatureName())
        self.defenseShipLineEdit.setText(defendingMiniature.pilot.ship.name)
        self.attackResults=None
        self.defenseResults=None
        return self.exec_()
        
    def rollAttackDices(self):
        self.attackResults=self.parent.battleEngine.getAttackResults(self.attackingMiniature,self.defendingMiniature)
        self.hitSpinBox.setValue(self.attackResults['attack'])
        self.criticalSpinBox.setValue(self.attackResults['critical'])
        self.focusAttackSpinBox.setValue(self.attackResults['focus'])
        self.blankAttackSpinBox.setValue(self.attackResults['nothing'])
    
    def rollDefenseDices(self):
        self.defenseResults=self.parent.battleEngine.getDefenseResults(self.attackingMiniature,self.defendingMiniature)
        self.evadeDefenseSpinBox.setValue(self.defenseResults['evade'])
        self.blankDefenseSpinBox.setValue(self.defenseResults['nothing'])
        self.focusDefenseSpinBox.setValue(self.defenseResults['focus'])
        
    
    def useAttackFocus(self):
        focusDices=self.focusAttackSpinBox.value()
        attackDices=self.hitSpinBox.value()
        self.focusAttackSpinBox.setValue(0)
        self.hitSpinBox.setValue(focusDices+attackDices)
    
    def useEvade(self):
        pass
    
    def useAttackModifier(self):
        pass
    
    def useDefenseModifier(self):
        pass
