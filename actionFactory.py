
class ActionFactory():
    def __init__(self):
        self.actionsLibrary=[Evade(), Focus(), TargetLock(), BarrelRoll()]
    
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
    def __init__(self):
        AbstractAction.__init__(self,u"Barrel Roll")
        

        

        