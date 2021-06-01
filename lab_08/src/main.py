from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem, QColorDialog, QWidget, QMessageBox
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter, QTextImageFormat
from PyQt5.QtCore import QLine, QRectF, Qt, QTime, QCoreApplication, QEventLoop, QPoint, QLine, QEvent
import sys

from scene import graphicsScene
import scene

import cut

class mainWindow(QtWidgets.QMainWindow):
    SCENE_WIDTH  = 1070
    SCENE_HEIGHT = 751

    LINE_COLOR        = QColorConstants.Black
    CUTTED_LINE_COLOR = QColorConstants.Magenta
    CUTTER_COLOR      = QColorConstants.Red

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)

        self.scene = graphicsScene(self, 0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT)

        self.main_scene.setScene(self.scene)

        self.image = QImage(self.SCENE_WIDTH, self.SCENE_HEIGHT, QImage.Format_RGB32)

        self.image.fill(QColorConstants.White)

        self.repaint()

        self.lines          = []
        self.ctrl_pressed   = False
        self.adding_cutter  = False # If False then adding line on screen, otherwise adding cutter rectangle

        self.curr_line      = []
        self.cutter         = []

        self.current_cutter = []

        # self.add_line_btn.clicked.connect(self.addLineBtnHandler)
        self.clean_btn.clicked.connect(self.cleanScreen)
        self.add_cutter_btn.clicked.connect(self.addCutterBtnHandler)
        self.cut_btn.clicked.connect(self.cutBtnHandler)
        self.closeCutter.clicked.connect(self.closeCutterHandler)

    def drawLine(self, p1:QPoint, p2:QPoint, color:QColor):
        pen = QPen(color)

        if color == self.CUTTED_LINE_COLOR:
            pen.setWidthF(1.3)

        self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)

    def addCutterBtnHandler(self):
        self.adding_cutter = not self.adding_cutter

    def repaint(self):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def previewData(self) -> (QPoint, QColor):
        '''
        Line preview routine. Returns start point and color
        '''

        start_p = None

        if self.adding_cutter:
            color   = self.CUTTER_COLOR
        else:
            color = self.LINE_COLOR

        if len(self.curr_line) != 0:
            start_p = self.curr_line[0]

        return (start_p, color)

    def lineAddHandler(self, p:QPoint, type):
        self.curr_line.append(p)

        if len(self.curr_line) == 2:
            if self.adding_cutter:
                if len(self.cutter) == 0:
                    self.cutter.append(self.curr_line[0])

                if type == scene.RELEASE:
                    self.cutter.append(p)
                    self.drawLine(self.curr_line[0], self.curr_line[1], self.CUTTER_COLOR)
                    del self.curr_line[0]
                else:
                    del self.curr_line[1]
            else:
                self.lines.append(QLine(self.curr_line[0], self.curr_line[1]))

                self.drawLine(self.curr_line[0], self.curr_line[1], self.LINE_COLOR)

                self.curr_line.clear()

    def cleanScreen(self):
        self.image.fill(QColorConstants.White)
        self.repaint()

        self.curr_line.clear()
        self.lines.clear()
        self.cutter.clear()

        self.scene.reset()

    def closeCutterHandler(self):
        if len(self.cutter) > 2:
            self.drawLine(self.cutter[0], self.cutter[-1], self.CUTTER_COLOR)
            self.curr_line.clear()

            self.cutter.append(self.cutter[0])

            self.adding_cutter = False
        else:
            self.throwWarn('Введенно недостаточное кол-во ребер отсекателя.')

    def throwWarn(self, text:str):
        warn = QMessageBox()

        warn.setText(text)
        warn.exec_()

    def cutBtnHandler(self):
        convexity = cut.checkConvexity(self.cutter)

        if convexity != 1:
            self.throwWarn('Заданный отсекатель не является выпуклым многоугольником')
            return

        poly3d = cut.twoD2ThreeDPoly(self.cutter)

        direction = cut.direction(poly3d)

        if direction == 0:
            print('direction is zero. Exitting...')
            return

        normVect = cut.normalizePoly(poly3d, direction)

        for i in self.lines:
            visible, p1, p2 = cut.cutLine(poly3d, normVect, i.p1(), i.p2())

            print('visible?:', visible)

            if visible:
                self.drawLine(p1, p2, self.CUTTED_LINE_COLOR)

        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())
