from move import move

class ship:
    def __init__(self,name='',size=2):
        #size in centimeters
        self.name=name
        self.moveIds=self.initializeMoves()
        self.size=size
    def asDict(self):
        pass
    def fromDict(self):
        pass
    
    def initializeMoves(self):
        moves=range(1,17)
        return moves
    def getMoveByName(self,name):
        for move in self.moves:
            if move.name==name:
                return move
        return None