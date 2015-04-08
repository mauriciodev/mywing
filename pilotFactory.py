import os, json
from pilot import pilot
from ship import ship
from move import move

class PilotFactory:
    "This class should have a parent to report it's messages."
    def __init__(self,parent=None,scale=0):
        self.scale=scale
        self.parent=parent
        self.pilotLibrary = {}
        self.readPilots()

    def getPilotById(self,pilotId):
        return self.pilotLibrary[pilotId]
        
    
    def printMessage(self, message):
        if (self.parent!=None) and ('printMessage' in dir(self.parent)):
            self.parent.printMessage(message)
        else:
            print dir(self.parent)

    def getPilotByName(self,name):
        #print self.pilotLibrary
        for pilot in self.pilotLibrary.values():
            if pilot.name==name:
                return pilot
    
    def readPilots(self):
        self.printMessage("Loading ship data.")
        self.readShips()
        self.printMessage("Loading movement data.")
        self.readMoves()
        self.pilotLibrary = {}
        self.printMessage("Loading pilot data.")
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname, 'data/pilots.json')) as f:
            for line in f:
                p = pilot()
                p.fromDict(json.loads(line))
                pilotId=p.id
                p.ship=self.getPilotShip(p)
                p.moves=self.getPilotMoves(p)
                self.pilotLibrary[p.id] = p
                
        
                # print p.asDict()
    def readMoves(self):
        self.movesLibrary = {}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname, 'data/moves.json')) as f:
            for line in f:
                m = move(scale=self.scale)
                m.fromDict(json.loads(line))
                self.movesLibrary[m.id] = m
    def readShips(self):
        self.shipsLibrary = {}
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(dirname, 'data/ships.json')) as f:
            for line in f:
                s = ship()
                s.fromDict(json.loads(line))
                self.shipsLibrary[s.id] = s
    def savePilots(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        pilotFile = open(os.path.join(dirname, 'data/pilots.json'), 'w')
        for pilot in self.pilotLibrary:
            pilotFile.write(json.dumps(pilot.asDict()))
        pilotFile.close() 
    
    def getMoveById(self,moveId):
        return self.movesLibrary[moveId]
    
    def getMoveByName(self,moveName):
        for move in self.movesLibrary.values():
            if move.name==moveName:
                return move
    
    def getPilotShip(self,p):
        return self.shipsLibrary[p.shipId]
    
    def getPilotMoves(self,p):
        moves=[]
        for moveId in p.ship.moveIds:
            moves.append(self.movesLibrary[moveId])
        return moves
    
    
if __name__=="__main__":
    test=PilotFactory()
    print test.getPilotByName("Master Mauricio")
