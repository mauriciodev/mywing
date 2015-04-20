from PyQt4 import QtCore,QtGui

class turnSequencer(QtCore.QObject):
    playersChoseTheirMoves=QtCore.pyqtSignal()
    stageDone=QtCore.pyqtSignal()
    def __init__(self,battleViewer):
        self.battleViewer=battleViewer
        
        self.miniatures=self.battleViewer.battleEngine.miniatures[:] #sorted (by pilot skillLevel) list of miniatures
        self.currMini=0
        super(QtCore.QObject,self).__init__()
        self.machine=QtCore.QStateMachine()
        
        #Choose team
        stageChooseTeam=QtCore.QState()
        stageChooseTeam.entered.connect(self.battleViewer.addPilot)
        
        #Set Pieces
        stageSetPieces=QtCore.QState()
        stageChooseTeam.addTransition(self.stageDone, stageSetPieces)
        stageSetPieces.entered.connect(self.setPieces)
        
        #This is the first stage in the main game
        stageChooseMove=QtCore.QState()
        stageSetPieces.addTransition(self.stageDone, stageChooseMove)
        stageChooseMove.entered.connect(self.chooseMoves)
        
        stageChooseAction=QtCore.QState()
        stageChooseMove.addTransition(self.playersChoseTheirMoves, stageChooseAction)
        stageChooseAction.entered.connect(self.beginActionStage)
        stageAttack=QtCore.QState()
        stageGameOver=QtCore.QFinalState()
        
        self.machine.addState(stageChooseTeam)
        self.machine.addState(stageSetPieces)
        self.machine.addState(stageChooseMove)
        self.machine.addState(stageChooseAction)
        self.machine.addState(stageAttack)
        self.machine.addState(stageGameOver)
        
        #Begin choosing moves
        #self.machine.setInitialState(stageChooseTeam)
        self.machine.setInitialState(stageChooseTeam)


    def updateMiniatures(self):
        self.miniatures=self.battleViewer.battleEngine.miniatures[:]
        self.sortMiniatures()
        self.miniatures.reverse()
    
    def updatePlayers(self):
        self.players=self.battleViewer.battleEngine.players

    def beginGame(self):
        self.updatePlayers()
        self.updateMiniatures()
        #self.addAttackSequence()
        self.turn=0
        self.machine.start()
    
    def addAttackSequence(self):
        self.attackSequence=[]
        for mini in self.miniatures:
            self.machine

    def sortMiniatures(self):
        self.miniatures.sort(key=lambda x: x.pilot.skillLevel)
        

    def currentMiniature(self):
        """Returns -1 if it's a stage that everyone can attack. Return an self.miniatures id otherwise."""
        pass
    def getNumberOfPlayers(self):
        return len(self.players)
    
    def checkIfEveryPlayerChoseTheirMoves(self):
        miniNotOk=[]
        for mini in self.miniatures:
            if mini.nextMove==None:
                miniNotOk.append(mini)
        if len(miniNotOk)==0:
            self.stageDone.disconnect(self.checkIfEveryPlayerChoseTheirMoves)
            self.playersChoseTheirMoves.emit()
        else:
            miniNames=map(lambda x: x.name, miniNotOk)
            self.showMessage( "Turn not finished.", "Miniatures left to move: " + str(miniNames))
    
    def beginActionStage(self):
        self.updateStage("Move and perform actions")
        self.showMessage("Action stage", "Players should now perform their moves and choose their actions.")
    
    def beginAttackStage(self):
        pass
    
    def done(self):
        #Generic method to tell the sequencer that the user ended a stage
        self.stageDone.emit()
    
    def chooseMoves(self):
        self.updateStage("Choose each move")
        self.showMessage("Choose your moves", "Use the right button on each miniature to assign their moves.")
        self.stageDone.connect(self.checkIfEveryPlayerChoseTheirMoves)
        
    def setPieces(self):
        self.updateStage("Positioning")
        self.showMessage("Miniature positioning stage", "Players can now position their miniatures wherever they want.")
        self.updateMiniatures()
    def endTurn(self):
        self.turn+=1
        
    def showMessage(self,title,message):
        QtGui.QMessageBox.information(self.battleViewer,title,message)
    
    def updateStage(self,stage):
        s="Turn: "+str(self.turn)+" Stage: "+stage
        self.updateStatus(s)
    
    def updateStatus(self, s):
        self.battleViewer.statusbar.showMessage(s)
if __name__=="__main__":
    test=turnSequencer()    