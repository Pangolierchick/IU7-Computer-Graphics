from os import X_OK
from PyQt5 import QtWidgets, uic
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColorConstants, QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import sys
from dataclasses import dataclass

@dataclass
class Dot:
    x:int
    y:int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

@dataclass
class Edge:
    l: Dot
    r: Dot

    def __init__(self, l:Dot, r:Dot):
        self.l = l
        self.r = r


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)

        self.scene = MyScene(self, 0, 0, 1191, 725)
        self.main_scene.setScene(self.scene)


        self.add_dot_btn.clicked.connect(self.addPoint)
        self.clean_screen_btn.clicked.connect(self.clean)
        self.color_chooser.clicked.connect(self.__chooseColor)
        
        self.color = QColorConstants.Black
        self.pen = QPainter()
        
        
        self.scene.addLine(0, 0, 1191, 725)
    
    def __getPoint(self):
        return Dot(self.x_spinbox.value(), self.y_spinbox.value())
    
    def addPoint(self, x=None, y=None):
        if x is not None and y is not None:
            x = QTableWidgetItem(str(x))
            y = QTableWidgetItem(str(y))
        else:
            dot = self.__getPoint()
            x = QTableWidgetItem(str(dot.x))
            y = QTableWidgetItem(str(dot.y))

        curr_rows = self.coord_table.rowCount()

        self.coord_table.insertRow(curr_rows)
        self.coord_table.setItem(curr_rows, 0, x)
        self.coord_table.setItem(curr_rows, 1, y)

    def __chooseColor(self):
        self.color = QColorDialog.getColor()
    
    def clean(self):
        self.scene.clear()
        self.coord_table.clear()
        self.coord_table.setRowCount(0)

class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, win:Window, *args):
        super().__init__(*args)
        self.window = win

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.window.addPoint(x=event.scenePos().x(), y=event.scenePos().y())
            print(event.scenePos().x(), event.scenePos().y())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

