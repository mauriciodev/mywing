from PyQt4 import QtCore

class turnSequencer(QtCore.QObject):
    def __init__(self,players={}, miniatures=[]):
        self.players=players #dictionary of players
        self.miniatures=miniatures[:] #sorted (by pilot skillLevel) list of miniatures
        self.currMini=0
        super(QtCore.QObject,self).__init__()
        self.machine=QtCore.QStateMachine()
        
        stageSetPieces=QtCore.QState()
        stageChooseMove=QtCore.QState()
        stageChooseAction=QtCore.QState()
        stageAttack=QtCore.QState()
        stageGameOver=QtCore.QFinalState()
        
        self.machine.addState(stageSetPieces)
        self.machine.addState(stageChooseMove)
        self.machine.addState(stageChooseAction)
        self.machine.addState(stageAttack)
        self.machine.addState(stageGameOver)
        
        #Begin choosing moves
        self.machine.setInitialState(stageSetPieces)


    def updateMiniatures(self,miniatures):
        self.miniatures=miniatures[:]
        self.sortMiniatures()
        self.miniatures.reverse()
    
    def updatePlayers(self,players):
        self.players=players

    def beginGame(self,miniatures,players):
        self.updatePlayers(players)
        self.updateMiniatures(miniatures)
        self.addAttackSequence()
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


if __name__=="__main__":
    test=turnSequencer()    