from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem, QColorDialog, QWidget
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter, QTextImageFormat
from PyQt5.QtCore import QLine, QRectF, Qt, QTime, QCoreApplication, QEventLoop, QPoint, QLine, QEvent
import sys
from dataclasses import dataclass
from cut import simple_cut

from line import Line
from cutter import Cutter

class mainWindow(QtWidgets.QMainWindow):
    SCENE_WIDTH  = 1070
    SCENE_HEIGHT = 751

    LINE_COLOR        = QColorConstants.Black
    CUTTED_LINE_COLOR = QColorConstants.Magenta
    CUTTER_COLOR      = QColorConstants.Red

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.scene = QGraphicsScene(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT)
        self.main_scene.setScene(self.scene)

        self.lines         = []
        self.ctrl_pressed  = False
        self.adding_cutter = False # If False then adding line on screen, otherwise adding cutter rectangle
        
        self.curr_line     = []
        self.line_preview  = None
        
        self.current_cutter = []
        self.cutter_preview = None

        self.cutter:Cutter = None

        self.add_line_btn.clicked.connect(self.addLineBtnHandler)
        self.clean_btn.clicked.connect(self.cleanScreen)
        self.add_cutter_btn.clicked.connect(self.addCutterBtnHandler)
        self.cut_btn.clicked.connect(self.cutBtnHandler)
    
        self.main_scene.setMouseTracking(True)
        self.main_scene.viewport().installEventFilter(self)
    
    def addLineBtnHandler(self):
        p1 = QPoint(self.x0_spin.value(), self.y0_spin.value())
        p2 = QPoint(self.x1_spin.value(), self.y1_spin.value())

        self.addLine(p1, p2)
    
    def addCutterBtnHandler(self):
        self.__delCutter()
        self.adding_cutter = True

    def cutBtnHandler(self):
        if self.cutter:
            xl = self.cutter.topLeft().x()
            yu = self.cutter.topLeft().y()
            xr = self.cutter.bottomRight().x()
            yd = self.cutter.bottomRight().y()

            for i in self.lines:
                p1 = [i.p1().x(), i.p1().y()]
                p2 = [i.p2().x(), i.p2().y()]

                visible, p1, p2 = simple_cut(xl, xr, yd, yu, p1, p2)

                if visible:
                    self.scene.addLine(p1[0], p1[1], p2[0], p2[1], self.CUTTED_LINE_COLOR)
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove and source is self.main_scene.viewport():
            self.__previewCutter(event.pos())
            self.__previewLine(event.pos())

        return QWidget.eventFilter(self, source, event)
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        but = a0.button()
        x = a0.x()
        y = a0.y()
        borders = self.main_scene.geometry().getCoords()
        if borders[0] <= x < borders[2] and borders[1] <= y < borders[3]:
            x -= borders[0]
            y -= borders[1]
        else:
            return

        if a0.buttons() == Qt.LeftButton:
            pos = QPoint(x, y)
            self.__drawLineHandler(pos)
            self.__drawCutterHandler(pos)
    
    def addLine(self, p1:QPoint, p2:QPoint):
        l = Line(p1, p2)
        self.lines.append(l)
        self.__drawLine(l)
    
    def addCutter(self, p1:QPoint, p2:QPoint):
        c = Cutter(p1, p2)
        self.cutter = c
        self.__drawCutter(c)
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Control:
            self.ctrl_pressed = False
    
    def __drawLine(self, l:Line):
        lp = l.p1()
        rp = l.p2()

        l.setSceneItem(self.scene.addLine(lp.x(), lp.y(), rp.x(), rp.y(), self.LINE_COLOR))
    
    def __drawCutter(self, c:Cutter):
        tl = c.topLeft()
        br = c.bottomRight()
    
        c.setSceneItem(self.scene.addRect(tl.x(), tl.y(), br.x() - tl.x(), br.y() - tl.y(), self.CUTTER_COLOR))
    
    def __drawLineHandler(self, p:QPoint):
        if self.adding_cutter == False:
            if len(self.curr_line) == 0 or not self.ctrl_pressed:
                self.curr_line.append(p)
            elif self.ctrl_pressed:
                line_start = self.curr_line[0]

                dx = p.x() - line_start.x()
                dy = p.y() - line_start.y()

                if abs(dy) > abs(dx):
                    self.curr_line.append(QPoint(line_start.x(), p.y()))
                else:
                    self.curr_line.append(QPoint(p.x(), line_start.y()))
            
            if len(self.curr_line) == 2:
                p1, p2 = self.curr_line

                self.addLine(p1, p2)
                self.curr_line.clear()
                self.scene.removeItem(self.line_preview)
    
    def __drawCutterHandler(self, p:QPoint):
        if self.adding_cutter:
            self.current_cutter.append(p)

            if len(self.current_cutter) == 2:
                v1, v2 = self.current_cutter
                self.addCutter(v1, v2)
                self.current_cutter.clear()
                self.scene.removeItem(self.cutter_preview)
                
                self.adding_cutter = False


    def __previewLine(self, p:QPoint):
        if len(self.curr_line) == 1:
            line_start = self.curr_line[0]

            if self.line_preview:
                self.scene.removeItem(self.line_preview)
            
            if self.ctrl_pressed:
                dx = p.x() - line_start.x()
                dy = p.y() - line_start.y()

                if abs(dy) >= abs(dx):
                    right_p = QPoint(line_start.x(), p.y())
                else:
                    right_p = QPoint(p.x(), line_start.y())

                self.line_preview = self.scene.addLine(line_start.x(), line_start.y(), right_p.x(), right_p.y(),  self.LINE_COLOR)
            else:
                self.line_preview = self.scene.addLine(line_start.x(), line_start.y(), p.x(), p.y(), self.LINE_COLOR)
    
    def __previewCutter(self, p:QPoint):
        if len(self.current_cutter) == 1:
            lu_p = self.current_cutter[0]
            rd_p = p

            x_l = lu_p.x()
            x_r = rd_p.x()

            y_u = lu_p.y()
            y_d = rd_p.y()

            if self.cutter_preview:
                self.scene.removeItem(self.cutter_preview)

            if x_l > x_r:
                x_l, x_r = x_r, x_l
            if y_u > y_d:
                y_u, y_d = y_d, y_u

            self.cutter_preview = self.scene.addRect(x_l, y_u, x_r - x_l, y_d - y_u, self.CUTTER_COLOR)
    
    def __delCutter(self):
        if self.cutter is not None:
            self.scene.removeItem(self.cutter.sceneItem())
            self.current_cutter.clear()
    
    def cleanScreen(self):
        self.lines.clear()
        self.curr_line.clear()
        self.current_cutter.clear()

        self.line_preview = None
        self.cutter_preview = None
        self.cutter = None

        self.adding_cutter = False

        self.scene.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())
