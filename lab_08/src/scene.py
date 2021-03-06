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

        left_p, color, shift = self.parent.previewData()

        if self.preview is not None:
            self.removeItem(self.preview)
            self.preview = None

        if left_p is not None:
            if shift:
                dx = pos.x() - left_p.x()
                dy = pos.y() - left_p.y()

                if abs(dy) > abs(dx):
                    self.preview = self.addLine(left_p.x(), left_p.y(), left_p.x(), pos.y(), QPen(color))
                    self.release = QPoint(left_p.x(), pos.y())
                else:
                    self.preview = self.addLine(left_p.x(), left_p.y(), pos.x(), left_p.y(), QPen(color))
                    self.release = QPoint(pos.x(), left_p.y())
            else:
                self.preview = self.addLine(left_p.x(), left_p.y(), pos.x(), pos.y(), QPen(color))
                self.release = QPoint(pos.x(), pos.y())

        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        pos = QPoint(event.scenePos().x(), event.scenePos().y())

        self.parent.lineAddHandler(pos, PRESS)

    def mouseReleaseEvent(self, event):
        pos = self.release

        self.parent.lineAddHandler(pos, RELEASE)

        if self.preview is not None:
            self.removeItem(self.preview)
            self.preview = None

    def reset(self):
        self.preview = None
