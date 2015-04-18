import move

class ActionFactory():
    def __init__(self, pilotFactory):
        self.actionsLibrary=[Evade(), Focus(), TargetLock(), BarrelRoll(pilotFactory), Boost(pilotFactory)]
        self.pilotFactory=pilotFactory
    
    def getActionByName(self,name):
        for item in self.actionsLibrary:
            if item.name==name:
                return item
        return None

    

class AbstractAction():
    def __init__(self,name=''):
        self.name=name
    def perform(self, miniature):
        pass
    
class Evade(AbstractAction):
    def __init__(self):
        AbstractAction.__init__(self,u"Evade")
    def perform(self,miniature):
        miniature.addEvadeToken()

class Focus(AbstractAction):
    def __init__(self):
        AbstractAction.__init__(self,u"Focus")
    def perform(self,miniature):
        miniature.addFocusToken()

class TargetLock(AbstractAction):
    def __init__(self):
        AbstractAction.__init__(self,u"Target Lock")
    def perform(self, targeteerMiniature,targetedMiniature):
        targeteerMiniature.addTargetLockerToken(targetedMiniature)
        
class BarrelRoll(AbstractAction):
    def __init__(self,pilotFactory):
        self.pilotFactory=pilotFactory
        AbstractAction.__init__(self,u"Barrel Roll")
    def perform(self, mini, size="right", position=0.5):
        #side = left or right
        #position is a float that represents the position of the 1 bar
        brMove=self.pilotFactory.movesLibrary[20]
        brMove.dx=-mini.height
        brMove.performMove(mini)
        print "Not implemented"
class Boost(AbstractAction):
    def __init__(self,pilotFactory):
        self.pilotFactory=pilotFactory
        AbstractAction.__init__(self,u"Boost")
    def perform(self, mini, direction=0):
        
        #direction can be -1, 0 or 1 meaning bank left, straight or bank right
        boostMove=None
        if direction==0:
            boostMove=self.pilotFactory.movesLibrary[0]
        if direction==-1:
            boostMove=self.pilotFactory.movesLibrary[8]
        if direction==1:
            boostMove=self.pilotFactory.movesLibrary[5]
        if boostMove==None:
            print "Invalid boost move."
        else: 
            boostMove.performMove(mini)
        
        

        