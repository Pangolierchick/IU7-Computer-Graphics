from os import X_OK
from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter, QTextImageFormat
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import sys
from dataclasses import dataclass


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

        self.backGroundColor = QColorConstants.Magenta

        self.last_point = None
        self.edges = []
        self.points = []
    
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
        for edge in self.edges:
            self.scene.addLine(edge.l.x(), edge.l.y(), edge.r.x(), edge.r.y())
            # painter.drawLine(edge.l.x(), edge.l.y(), edge.r.x(), edge.r.y())
    
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

        return _min.x(), _max.x()
    
    
    def __min_maxY(self):
        _min = self.points[0]
        _max = self.points[0]

        for i in range(1, len(self.points)):
            _min = min(_min, self.points[i], key=lambda x: x.y())
            _max = max(_max, self.points[i], key=lambda x: x.y())

        return _min.y(), _max.y()
    
    def __paintOverFigure(self):
        pix = QPixmap()
        painter = QPainter()

        left_x, right_x = self.__min_maxX()
        down_y, upper_y = self.__min_maxY()

        painter.begin(self.image)

        for y in range(upper_y + 10, down_y, -1):
            F = False

            for x in range(left_x - 10, right_x):
                pixel_color = QColor(self.image.pixel(x, y))

                # print("Curr color:", pixel_color.name())
                if pixel_color == QColorConstants.Black:
                    print(f'Found edge {x} {y}')
                    F = not F
                
                if F:
                    curr_color = self.backGroundColor
                else:
                    curr_color = QColorConstants.Blue
            

                painter.setPen(curr_color)
                
                # print(f'Drawing pixel {x} {y} with color: {curr_color.name()}')
                painter.drawPoint(x, y)

            
            if self.do_slow_drawing.isChecked():
                self.delay()
                pix.convertFromImage(self.image)
                self.scene.addPixmap(pix)
        
        if not self.do_slow_drawing.isChecked():
            pix.convertFromImage(self.image)
            self.scene.addPixmap(pix)
        
        painter.end()
        self.drawEdges()



class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, win:Window, *args):
        super().__init__(*args)
        self.window = win

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.window.addPoint(x_coord=event.scenePos().x(), y_coord=event.scenePos().y())
            self.window.drawPolyHandler(event.scenePos())
    
            print(event.scenePos().x(), event.scenePos().y())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

