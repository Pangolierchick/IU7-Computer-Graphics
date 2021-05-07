from os import X_OK
from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter, QTextImageFormat
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import sys
from dataclasses import dataclass
from time import perf_counter, sleep
import math


@dataclass
class Edge:
    l: QPoint
    r: QPoint

    def __init__(self, l:QPoint, r:QPoint):
        self.l = l
        self.r = r


class Window(QtWidgets.QMainWindow):
    SCENE_WIDTH  = 1191
    SCENE_HEIGHT = 725
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.scene = MyScene(self, 0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT)
        self.main_scene.setScene(self.scene)
        self.image = QImage(self.SCENE_WIDTH, self.SCENE_HEIGHT, QImage.Format_RGB32)
        self.image.fill(QColorConstants.White)

        self.add_dot_btn.clicked.connect(self.addPoint)
        self.clean_screen_btn.clicked.connect(self.clean)
        self.color_chooser.clicked.connect(self.__chooseColor)
        self.close_figure_btn.clicked.connect(self.__closePoly)
        self.paint_figure_btn.clicked.connect(self.__paintOverFigure)
        
        self.color = QColor(0, 0, 0)
        self.pen = QPen(self.color)


        self.last_point = None
        self.edges = []
        self.points = []
        self.seed_point = QPoint(0, 0)

        self.backGroundColor = QColorConstants.DarkMagenta
        self.lineColor = QColorConstants.Black

        scene = QtWidgets.QGraphicsScene(0, 0, 68, 20)
    
        image = QPixmap(68, 20)
        image.fill(self.backGroundColor)

        scene.addPixmap(image)
        self.color_viewer.setScene(scene)
    
    def __getPoint(self):
        return QPoint(self.x_spinbox.value(), self.y_spinbox.value())
    
    def addPoint(self, x_coord=None, y_coord=None):
        if x_coord is not None and y_coord is not None:
            x = QTableWidgetItem(str(x_coord))
            y = QTableWidgetItem(str(y_coord))
    
            self.drawPolyHandler(QPoint(x_coord, y_coord))

        else:
            dot = self.__getPoint()
            x = QTableWidgetItem(str(dot.x()))
            y = QTableWidgetItem(str(dot.y()))

            self.drawPolyHandler(dot)

        curr_rows = self.coord_table.rowCount()

        self.coord_table.insertRow(curr_rows)
        self.coord_table.setItem(curr_rows, 0, x)
        self.coord_table.setItem(curr_rows, 1, y)

    def __chooseColor(self):
        self.backGroundColor = QColorDialog.getColor()

        if self.color.isValid():
            scene = QtWidgets.QGraphicsScene(0, 0, 68, 20)
    
            image = QPixmap(68, 20)
            image.fill(self.backGroundColor)

            scene.addPixmap(image)
            self.color_viewer.setScene(scene)

    
    def clean(self):
        self.scene.clear()
    
        self.coord_table.clear()
        self.coord_table.setRowCount(0)
    
        self.last_point = None
        self.edges = []
        self.points = []
        self.image.fill(QColorConstants.White)
    
    def drawPolyHandler(self, p:QPoint):
        if self.last_point is not None:
            self.scene.addLine(self.last_point.x(), self.last_point.y(), p.x(), p.y(), self.pen)

            self.edges.append(Edge(self.last_point, p))
        else:
            self.first_point = p

        self.last_point = p

        self.points.append(p)

    
    def drawEdges(self):
        pix = QPixmap()
        painter = QPainter()

        painter.begin(self.image)

        pen = QPen(QColorConstants.Black)
        pen.setWidth(1)
        painter.setPen(pen)

        for edge in self.edges:
            painter.drawLine(edge.l.x(), edge.l.y(), edge.r.x(), edge.r.y())
        
        painter.end()

        pix.convertFromImage(self.image)
        self.scene.clear()
        self.scene.addPixmap(pix)

    
    def __closePoly(self):
        if len(self.edges) > 1:
            last = self.edges[-1].r
            self.scene.addLine(self.first_point.x(), self.first_point.y(), last.x(), last.y(), self.pen)

            self.last_point = None

            self.edges.append(Edge(self.first_point, last))
    
    def __delay(self):
        QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)
    
    def trace_edge(self, edge:Edge):
        '''
        Traces edge with bresenhem algo
        '''

        x1 = edge.l.x()
        x2 = edge.r.x()
        y1 = edge.l.y()
        y2 = edge.r.y()

        dx = int(x2 - x1)
        dy = int(y2 - y1)
        sx = math.copysign(1, dx)
        sy = math.copysign(1, dy)
        dx = abs(dx)
        dy = abs(dy)

        swap = False
        if (dy <= dx):
            swap = False
        else:
            swap = True
            dx, dy = dy, dx

        e = int(2 * dy - dx)
        x = int(x1)
        y = int(y1)

        for i in range(dx + 1):
            self.image.setPixel(x, y, self.backGroundColor.rgb())
            if (e >= 0):
                if (swap):
                    x += sx
                else:
                    y += sy
                e = e - 2 * dx
            if (e < 0):
                if (swap):
                    y += sy
                else:
                    x += sx
                e = e + 2 * dy
        self.redraw()

    def trace_figure(self):
        for edge in self.edges:
            self.trace_edge(edge)
    

    def __paintOverFigure(self):
        self.scene.clear()
        self.trace_figure()

        stack = [self.seed_point]
        color = self.backGroundColor.rgb()

        start = perf_counter()

        while len(stack):
            if self.do_slow_drawing.isChecked():
                QtWidgets.QApplication.processEvents()

            point = stack.pop()
            self.image.setPixel(point.x(), point.y(), color)

            x, y = point.x() + 1, point.y()

            while self.image.pixelColor(x, y).rgb() not in [self.backGroundColor.rgb(), self.lineColor.rgb()]:
                self.image.setPixel(x, y, color)
                x += 1

            rborder = x - 1

            x = point.x() - 1
    
            while self.image.pixelColor(x, y).rgb() not in [self.backGroundColor.rgb(), self.lineColor.rgb()]:
                self.image.setPixel(x, y, color)
                x -= 1
            
            self.redraw()

            lborder = x + 1

            sign = [1, -1]

            for i in sign:
                x = lborder
                y = point.y() + i

                while x <= rborder:
                    is_exist = False
                    while self.image.pixelColor(x, y).rgb() not in [self.backGroundColor.rgb(), self.lineColor.rgb()] and x <= rborder:
                        is_exist = True
                        x += 1

                    if is_exist:
                        stack.append(QPoint(x - 1, y))

                    xi = x
                    while self.image.pixelColor(x, y).rgb() not in [self.backGroundColor.rgb(), self.lineColor.rgb()] and x <= rborder:
                        x += 1
                    if x == xi:
                        x += 1
        print('done')

        end = perf_counter()

        if not self.do_slow_drawing.isChecked():
            self.time_label.setText(f"{end - start:.6}")

        self.drawEdges()
    
    def redraw(self):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
    
    def update_seed(self, seed:QPoint):
        self.seed_point = seed
        self.seed_x.setText(str(seed.x()))
        self.seed_y.setText(str(seed.y()))


class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, win:Window, *args):
        super().__init__(*args)
        self.window = win
        
        self.last_x = None
        self.last_y = None

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            if self.window.choose_seed.isChecked():
                self.window.update_seed(event.scenePos())
            else:
                posx = event.scenePos().x()
                posy = event.scenePos().y()

                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    if posy != self.last_y:
                        der = (posx - self.last_x) / (posy - self.last_y)
                    else:
                        der = 2
                    if abs(der) <= 1:
                        posx = self.last_x
                    else:
                        posy = self.last_y
                
                self.window.addPoint(posx, posy)
                    
                self.last_x = posx
                self.last_y = posy

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

