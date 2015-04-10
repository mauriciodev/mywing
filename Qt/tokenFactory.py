from PyQt4 import QtGui, QtSvg, QtCore
import os,sys

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

class TokenFactory(QtCore.QObject):
    def __init__(self,scene=None):
        self.scene=scene
        self.tokenRenderer=QtSvg.QSvgRenderer(os.path.join(os.path.split(basedir)[0],'images','tokens.svg' ))
        self.tokenCount=0
    def newToken(self,parent,type,x=-20,y=0):
        if self.tokenRenderer.elementExists(type):
            token=Token(parent,self.tokenCount)
            self.tokenCount+=1
            token.setScale(0.3)
            token.setSharedRenderer(self.tokenRenderer)
            token.setElementId(type)
            token.setZValue(100)
            token.setPos(x,y)
            return token
        else:
            print "Invalid token."
            return None

class Token(QtSvg.QGraphicsSvgItem):
    def __init__(self,parent=None,tokenId=0):
        super(Token,self).__init__(parent)
        self.tokenId=tokenId
    
    def getTokenType(self):
        return self.elementId()
    
