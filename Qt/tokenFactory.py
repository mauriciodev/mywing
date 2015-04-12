from PyQt4 import QtGui, QtSvg, QtCore
import os,sys

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.join(os.path.split(os.path.dirname(__file__))[0],'images')

class TokenFactory(QtCore.QObject):
    def __init__(self,scene=None, scale=1):
        self.scene=scene
        self.tokenRenderer=QtSvg.QSvgRenderer(os.path.join(basedir,'tokens.svg' ))
        self.tokenCount=0
        self.tokenTypes=["Evade", "Target_Locker","Target_Locked", "Stress", "Focus"]
        self.scale=scale
    def newToken(self,parent,type,x,y):
        if self.tokenRenderer.elementExists(type):
            token=Token(parent,self.tokenCount)
            self.tokenCount+=1
            token.setScale(self.scale*0.25)
            token.setSharedRenderer(self.tokenRenderer)
            token.setElementId(type)
            token.setZValue(100)
            token.setPos(x,y)
            return token
        else:
            print "Invalid token."
            return None
    def newTargetLockerToken(self,parent, x,y,TargetMiniatureId):
        tokenType="Target_Locker"
        TLToken=self.newToken(parent, tokenType, x, y)
        TLToken.TargetPlayerId=TargetMiniatureId
    def newTargetLockedToken(self,parent, x,y,TargeteerMiniatureId):
        tokenType="Target_Locked"
        TLToken=self.newToken(parent, tokenType, x, y)
        TLToken.TargetPlayerId=TargeteerMiniatureId
        

class Token(QtSvg.QGraphicsSvgItem):
    def __init__(self,parent=None,tokenId=0,TargetMiniatureId=-1):
        super(Token,self).__init__(parent)
        self.tokenId=tokenId
        self.TargetMiniatureId=TargetMiniatureId
    
    def getTokenType(self):
        return self.elementId()
    
