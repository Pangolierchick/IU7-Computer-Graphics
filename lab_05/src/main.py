from os import X_OK
from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter, QTextImageFormat
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import sys
from dataclasses import dataclass
from time import perf_counter


@dataclass
class Edge:
    l: QPoint
    r: QPoint

    def __init__(self, l:QPoint, r:QPoint):
        self.l = l
        self.r = r


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)

        self.scene = MyScene(self, 0, 0, 1191, 725)
        self.main_scene.setScene(self.scene)
        self.image = QImage(1191, 725, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(QColorConstants.White)

        self.add_dot_btn.clicked.connect(self.addPoint)
        self.clean_screen_btn.clicked.connect(self.clean)
        self.color_chooser.clicked.connect(self.__chooseColor)
        self.close_figure_btn.clicked.connect(self.__closePoly)
        self.paint_figure_btn.clicked.connect(self.__paintOverFigure)
        
        self.color = QColorConstants.Black
        self.pen = QPen(self.color)


        self.last_point = None
        self.edges = []
        self.points = []

        self.backGroundColor = QColorConstants.Magenta

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
    
    def __min_maxX(self):
        _min = self.points[0]
        _max = self.points[0]

        for i in range(1, len(self.points)):
            _min = min(_min, self.points[i], key=lambda x: x.x())
            _max = max(_max, self.points[i], key=lambda x: x.x())

        return int(_min.x()), int(_max.x())
    
    
    def __min_maxY(self):
        _min = self.points[0]
        _max = self.points[0]

        for i in range(1, len(self.points)):
            _min = min(_min, self.points[i], key=lambda x: x.y())
            _max = max(_max, self.points[i], key=lambda x: x.y())

        return int(_min.y()), int(_max.y())
    
    def __delay(self):
        QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)
    
    def trace_edge(self, edge):
        if edge.l.y() == edge.r.y():
            return
        

        if edge.l.y() > edge.r.y():
            edge.l, edge.r = edge.r, edge.l
        
        step_x = (edge.r.x() - edge.l.x()) / (edge.r.y() - edge.l.y())

        x = edge.l.x()
        y = edge.l.y()

        pix = QPixmap()
        painter = QPainter()
        painter.begin(self.image)

        painter.setPen(QColorConstants.Green)

        while y < edge.r.y():
            if QColor(self.image.pixel(int(x) + 1, y)) != QColorConstants.Green:
                painter.drawPoint(int(x) + 1, y)
            else:
                painter.drawPoint(int(x), y)
            
            x += step_x
            y += 1

        painter.end()

        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)



    def trace_figure(self):
        for edge in self.edges:
            self.trace_edge(edge)
    

    def __paintOverFigure(self):
        pix = QPixmap()
        painter = QPainter()

        left_x, right_x = self.__min_maxX()
        down_y, upper_y = self.__min_maxY()

        start = perf_counter()

        self.trace_figure()

        painter.begin(self.image)
        y = upper_y
        while y > down_y - 1:
            curr_color = QColorConstants.White
            inv_color  = self.backGroundColor

            curr_point_scan_string = left_x
            x = left_x
            while x < right_x + 3:
                painter.setPen(curr_color)
                if QColor(self.image.pixel(x, y)) == QColorConstants.Green:
                    painter.drawLine(curr_point_scan_string, y, x, y)
                    curr_color, inv_color = inv_color, curr_color
                    curr_point_scan_string = x

                x += 1
            painter.drawLine(curr_point_scan_string, y, x - 1, y + 1)

            
            if self.do_slow_drawing.isChecked():
                self.__delay()
                pix.convertFromImage(self.image)
                self.scene.addPixmap(pix)
            
            y -= 1
        
        if not self.do_slow_drawing.isChecked():
            pix.convertFromImage(self.image)
            self.scene.addPixmap(pix)
        
        painter.end()
        self.drawEdges()

        end = perf_counter()

        if not self.do_slow_drawing.isChecked():
            self.time_label.setText(f'Время: {end - start:.3}')


class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, win:Window, *args):
        super().__init__(*args)
        self.window = win
        self.last_point = None

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            pos = event.scenePos()
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                if self.last_point is not None:
                    x = pos.x() if pos.x() > pos.y() else self.last_point.x()
                    y = pos.y() if pos.x() < pos.y() else self.last_point.y()

                    print(x, y)

                    self.window.addPoint(x, y)
            else:
                self.window.addPoint(pos.x(), pos.y())
            
            self.last_point = pos

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

