from typing import List
import numpy as np
import math as m
import functools

@functools.lru_cache
def up_circle(x):
    return m.sqrt(4 - (x - 5)**2)

def down_circle(x):
    return -1 * up_circle(x)

@functools.lru_cache
def up_center_circle(x):
    return m.sqrt(1 - x**2)

def down_center_circle(x):
    return -1 * up_center_circle(x)

class Point():
    def __init__(self, x, y, z=1):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


class Picture():
    def __init__(self):
        self.getCenterCircle()
        self.getCenterCross()
        self.getCenterRhombus()
        self.getLeftHalfCircle()
        self.getRightHalfCircle()
        self.getMainRectangle()
    
    def getCenterCircle(self) -> list:
        self.center_circle = []

        for i in np.linspace(-1, 1, num=25):
            self.center_circle.append(Point(i, up_center_circle(i)))
        
        for i in np.linspace(-1, 1, num=25):
            self.center_circle.append(Point(i, down_center_circle(i)))


    def getCenterCross(self) -> list:
        self.cross = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]

    def getCenterRhombus(self) -> list:
        self.center_rhombus = [Point(0, -2), Point(-5, 0), Point(0, 2), Point(5, 0)]
        return self.center_rhombus

    def getLeftHalfCircle(self) -> list:
        self.left_circle = []

        for i in np.linspace(3, 5, num=25):
            self.left_circle.append(Point(i, up_circle(i), 1))
        
        for i in np.linspace(3, 5, num=25):
            self.left_circle.append(Point(i, down_circle(i), 1))
        
        return self.left_circle

    def getRightHalfCircle(self) -> list:
        self.right_circle = []

        for i in np.linspace(5, 7, num=25):
            self.right_circle.append(Point(i, up_circle(i), 1))
        
        for i in np.linspace(5, 7, num=25):
            self.right_circle.append(Point(i, down_circle(i), 1))
        
        return self.right_circle
    
    def getMainRectangle(self) -> list:
        self.main_rectangle = [Point(-5, -2), Point(-5, 2), Point(5, 2), Point(5, -2)]
        return self.main_rectangle
    

    def restart(self):
        self.__init__()
    
    def scale():
        pass


