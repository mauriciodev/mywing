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
        self.clearDiceResults()  
        self.attackingMiniature=attackingMiniature
        self.defendingMiniature=defendingMiniature
        self.attackUnitLineEdit.setText(attackingMiniature.getMiniatureName())
        self.attackShipLineEdit.setText(attackingMiniature.pilot.ship.name)
        attackDices=self.parent.battleEngine.getModifiedAttackDices(attackingMiniature,defendingMiniature)
        if attackDices==None:
            QtGui.QMessageBox.warning(self, "Attack not possible.", "Enemy out of attack range or angle.")
            return None
        else:
            self.attackSpinBox.setValue(attackDices)
            self.evadeSpinBox.setValue(self.parent.battleEngine.getModifiedDefenseDices(attackingMiniature,defendingMiniature))
            self.defenseUnitLineEdit.setText(defendingMiniature.getMiniatureName())
            self.defenseShipLineEdit.setText(defendingMiniature.pilot.ship.name)
            self.attackResults=None
            self.defenseResults=None
            self.listAttackModifiers(attackingMiniature,defendingMiniature)
            self.listDefenseModifiers(defendingMiniature)
            self.hideReroll()
            self.rollAttackPushButton.setEnabled(True)
            self.rollDefensePushButton.setEnabled(True)
            self.setAttackResultsVisibile(False)
            self.setDefenseResultsVisibile(False)
            return self.exec_()
    
    def setDefenseResultsVisibile(self, visible=True):
        self.groupBox_6.setVisible(visible)
        self.groupBox_4.setVisible(visible)
        
    def setAttackResultsVisibile(self, visible=True):
        self.groupBox_2.setVisible(visible)
        self.groupBox_5.setVisible(visible)
    
    def setAttackRerollsEnabled(self, enabled=True):
        self.pushButton_5.enabled=enabled
        self.pushButton_6.enabled=enabled
        self.pushButton_7.enabled=enabled
        self.pushButton_8.enabled=enabled
    def setDefenseRerollsEnabled(self, enabled=True):
        self.pushButton_9.enabled=enabled
        self.pushButton_11.enabled=enabled
        self.pushButton_12.enabled=enabled
        
        
    def clearDiceResults(self):
        self.hitSpinBox.setValue(0)
        self.criticalSpinBox.setValue(0)
        self.focusAttackSpinBox.setValue(0)
        self.blankAttackSpinBox.setValue(0)
        self.evadeDefenseSpinBox.setValue(0)
        self.blankDefenseSpinBox.setValue(0)
        self.focusDefenseSpinBox.setValue(0)
        self.hideReroll()
        self.setAttackRerollsEnabled(True)
        self.setDefenseRerollsEnabled(True)

        
    def addAttackDicesToSpinBoxes(self,attackResults):
        self.hitSpinBox.setValue(self.hitSpinBox.value()+attackResults['attack'])
        self.criticalSpinBox.setValue(self.criticalSpinBox.value()+attackResults['critical'])
        self.focusAttackSpinBox.setValue(self.focusAttackSpinBox.value()+attackResults['focus'])
        self.blankAttackSpinBox.setValue(self.blankAttackSpinBox.value()+attackResults['nothing'])

    def addDefenseDicesToSpinBoxes(self,defenseResults):
        self.evadeDefenseSpinBox.setValue(self.evadeDefenseSpinBox.value()+self.defenseResults['evade'])
        self.blankDefenseSpinBox.setValue(self.blankDefenseSpinBox.value()+self.defenseResults['nothing'])
        self.focusDefenseSpinBox.setValue(self.focusDefenseSpinBox.value()+self.defenseResults['focus'])
    
    def rollAttackDices(self):
        self.attackResults=self.parent.battleEngine.getAttackResults(self.attackingMiniature,self.defendingMiniature)
        self.addAttackDicesToSpinBoxes(self.attackResults)
        self.setAttackResultsVisibile(True)
        self.rollAttackPushButton.setEnabled(False)
    
    def rollDefenseDices(self):
        self.defenseResults=self.parent.battleEngine.getDefenseResults(self.attackingMiniature,self.defendingMiniature)
        self.addDefenseDicesToSpinBoxes(self.defenseResults)
        self.setDefenseResultsVisibile(True)
        self.rollDefensePushButton.setEnabled(False)
    
    def useAttackFocus(self):
        focusDices=self.focusAttackSpinBox.value()
        attackDices=self.hitSpinBox.value()
        self.focusAttackSpinBox.setValue(0)
        self.hitSpinBox.setValue(focusDices+attackDices)
        self.attackingMiniature.remFocusToken()
        
    def useDefenseFocus(self):
        focusDices=self.focusDefenseSpinBox.value()
        attackDices=self.evadeDefenseSpinBox.value()
        self.focusDefenseSpinBox.setValue(0)
        self.evadeDefenseSpinBox.setValue(focusDices+attackDices)
        self.defendingMiniature.remFocusToken()
    
    def useEvade(self):
        self.evadeDefenseSpinBox.setValue(self.evadeDefenseSpinBox.value()+1)
        self.defendingMiniature.remEvadeToken()
    
    def useAttackModifier(self):
        if len(self.attackModListWidget.selectedItems())>0:
            modText=self.attackModListWidget.selectedItems()[0].text()
            if modText=="Focus":
                self.useAttackFocus()
            if modText=="Target Lock":
                self.useTargetLock()
            self.attackModListWidget.takeItem(self.attackModListWidget.currentRow())
        else:
            QtGui.QMessageBox.warning(self, "Invalid attack modifier", "Please select one attack modifier.")
    
    def useDefenseModifier(self):
        if len(self.defenseModListWidget.selectedItems())>0:
            modText=self.defenseModListWidget.selectedItems()[0].text()
            if modText=="Focus":
                self.useDefenseFocus()
            if modText=="Evade":
                self.useEvade()
            self.defenseModListWidget.takeItem(self.defenseModListWidget.currentRow())
        else:
            QtGui.QMessageBox.warning(self, "Invalid attack modifier", "Please select one defense modifier.")
    
    def listAttackModifiers(self,attackingMiniature, defendingMiniature):
        if attackingMiniature.hasFocusToken():
            self.attackModListWidget.addItem("Focus")
        if attackingMiniature.hasTargetLockerToken(defendingMiniature.miniatureId):
            self.attackModListWidget.addItem("Target Lock")
            
    def listDefenseModifiers(self,defendingMiniature):
        if defendingMiniature.hasFocusToken():
            self.defenseModListWidget.addItem("Focus")
        if defendingMiniature.hasEvadeToken():
            self.defenseModListWidget.addItem("Evade")

    def setAttackRerollsVisible(self, visible=True):
        self.pushButton_5.setVisible(visible)
        self.pushButton_6.setVisible(visible)
        self.pushButton_7.setVisible(visible)
        self.pushButton_8.setVisible(visible)

    def useTargetLock(self):
        self.setAttackRerollsVisible(True)
        self.attackingMiniature.remTargetLockToken(self.defendingMiniature.miniatureId)

    def rerollAttackDice(self, spinBox, pushButton):
        dices=spinBox.value()
        spinBox.setValue(0)
        results=self.parent.battleEngine.rollAttackDices(dices)
        self.addAttackDicesToSpinBoxes(results)
        pushButton.setEnabled(False)
            
    def hideReroll(self, hide=True):
        self.setAttackRerollsVisible(not hide)
        self.setAttackRerollsVisible(not hide)
        self.setAttackRerollsEnabled(not hide)
        self.setDefenseRerollsEnabled(not hide)

    def hitReroll(self):
        self.rerollAttackDice(self.hitSpinBox, self.pushButton_5)
    def criticalHitReroll(self):
        self.rerollAttackDice(self.criticalSpinBox, self.pushButton_6)
    def attackFocusReroll(self):
        self.rerollAttackDice(self.focusAttackSpinBox, self.pushButton_7)
    def attackBlankReroll(self):
        self.rerollAttackDice(self.blankAttackSpinBox, self.pushButton_8)
    def evadeReroll(self):
        pass
        #self.rerollAttackDice(self.hitSpinBox, self.pushButton_9)
    def evadeFocusReroll(self):
        pass
        #self.rerollAttackDice(self.hitSpinBox, self.pushButton_11)
    def evadeBlankReroll(self):
        pass
        #self.rerollAttackDice(self.hitSpinBox, self.pushButton_12)