import PyQt5

from PyQt5.QtGui import QPen
from PyQt5.QtCore import QPoint

PRESS   = 1
RELEASE = 2

class graphicsScene(PyQt5.QtWidgets.QGraphicsScene):
    def __init__(self, parent, *args, **kwargs):
        '''
        Wrapper around qt QGraphicsScene. Needed to preview lines
        '''

        super().__init__(*args, **kwargs)

        self.parent = parent

        self.preview = None

    def mouseMoveEvent(self, event):
        pos = event.scenePos()

        left_p, color = self.parent.previewData()

        if self.preview is not None:
            self.removeItem(self.preview)
            self.preview = None

        if left_p is not None:
            self.preview = self.addLine(left_p.x(), left_p.y(), pos.x(), pos.y(), QPen(color))

        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        pos = QPoint(event.scenePos().x(), event.scenePos().y())

        self.parent.lineAddHandler(pos, PRESS)

    def mouseReleaseEvent(self, event):
        pos = QPoint(event.scenePos().x(), event.scenePos().y())

        self.parent.lineAddHandler(pos, RELEASE)

        if self.preview is not None:
            self.removeItem(self.preview)
            self.preview = None

    def reset(self):
        self.preview = None
