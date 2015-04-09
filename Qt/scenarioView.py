 
from PyQt4 import QtGui
class ScenarioView(QtGui.QGraphicsView):
    def __init__(self,parent=None):
        super(ScenarioView,self).__init__(parent)
        
    def wheelEvent(self,event):
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        #// Scale the view / do the zoom
        scaleFactor = 1.15
        if(event.delta() > 0):
            # Zoom in
            self.scale(scaleFactor, scaleFactor)
        else:
            # Zooming out
             self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)