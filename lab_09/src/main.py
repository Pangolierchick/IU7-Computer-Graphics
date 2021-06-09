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

        self.shift_pressed = False

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
            pen.setWidthF(1.8)

        self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)

    def addCutterBtnHandler(self):
        self.adding_cutter = not self.adding_cutter

    def repaint(self):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def previewData(self) -> (QPoint, QColor, bool):
        '''
        Line preview routine. Returns start point, color, shift pressed
        '''

        start_p = None

        if self.adding_cutter:
            color   = self.CUTTER_COLOR
        else:
            color = self.LINE_COLOR

        if len(self.curr_line) != 0:
            start_p = self.curr_line[0]

        return (start_p, color, self.shift_pressed)

    def lineAddHandler(self, p:QPoint, type):
        self.curr_line.append(p)

        if len(self.curr_line) == 2:
            if self.adding_cutter:
                curr_buf = self.cutter
                color = self.CUTTER_COLOR
            else:
                curr_buf = self.lines
                color = self.LINE_COLOR

            if len(curr_buf) == 0:
                curr_buf.append(self.curr_line[0])

            if type == scene.RELEASE:
                curr_buf.append(p)
                self.drawLine(self.curr_line[0], self.curr_line[1], color)
                del self.curr_line[0]
            else:
                del self.curr_line[1]

    def cleanScreen(self):
        self.image.fill(QColorConstants.White)
        self.repaint()

        self.curr_line.clear()
        self.lines.clear()
        self.cutter.clear()

        self.scene.reset()

    def closeCutterHandler(self):
        if self.adding_cutter:
            curr_fig = self.cutter
            color    = self.CUTTER_COLOR
        else:
            curr_fig = self.lines
            color    = self.LINE_COLOR

        if len(curr_fig) > 2:
            self.drawLine(curr_fig[0], curr_fig[-1], color)
            self.curr_line.clear()

            self.adding_cutter = False
        else:
            self.throwWarn('Введенно недостаточное кол-во ребер.')

    def throwWarn(self, text:str):
        warn = QMessageBox()

        warn.setText(text)
        warn.exec_()

    def cutBtnHandler(self):
        fig = cut.cut(self.lines, self.cutter)

        for i, v in enumerate(fig):
            self.drawLine(fig[i], fig[(i + 1) % len(fig)], self.CUTTED_LINE_COLOR)


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Shift:
            self.shift_pressed = not self.shift_pressed

        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())
