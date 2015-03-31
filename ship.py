from move import move

class ship:
    def __init__(self,id=0,name='NewShip',moveIds=[],moveCosts=[],sizeX=50,sizeY=50):
        self.id=id
        self.name=name
        self.moveIds=moveIds
        self.moveCosts=moveCosts
        self.sizeX=sizeX
        self.sizeY=sizeY
        self.moves=[]
    
    def readMoves(self,movesLibrary):
        self.moves=[]
        for moveId in self.moveIds:
            self.moves.append(movesLibrary[moveId])
    
    def asDict(self):
        pass
    def fromDict(self,dict):
        self.id=dict["id"]
        self.name=dict["name"]
        self.moveIds=dict["moveIds"]
        self.moveCosts=dict["moveCosts"]
        self.sizeX=dict["sizeX"]
        self.sizeY=dict["sizeY"]

    def getMoveCost(self,moveId):
        shipMoveId=self.moveIds.index(moveId)
        if shipMoveId>=0:
            return self.moveCosts[shipMoveId]
        else:
            return -1
        
"""    def getMoveByName(self,name):
        for move in self.moves:
            if move.name==name:
                return move
        return None"""
    
