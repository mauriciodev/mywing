from PyQt4 import QtGui, QtSvg, QtCore
import os


class TokenFactory(QtCore.QObject):
    def __init__(self,scene=None):
        self.scene=scene
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.tokenRenderer=QtSvg.QSvgRenderer(os.path.join(os.path.split(dirname)[0],'images','tokens.svg' ))
    def newToken(self,parent,type,x=-20,y=0):
        if self.tokenRenderer.elementExists(type):
            token=QtSvg.QGraphicsSvgItem(parent)
            print token.boundingRect()
            #token.boundingRect().setWidth(20)
            #token.boundingRect().setHeight(20)
            token.setScale(0.3)
            token.setSharedRenderer(self.tokenRenderer)
            token.setElementId(type)
            token.setZValue(100)
            token.setPos(-20,0)
            return token
        else:
            print "Invalid token."
            return None

