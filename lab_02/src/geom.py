from typing import List
import numpy as np
import math as m
import functools


CIRCLE_APPROXIMATION_DOTS = 25

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
    
    def move(self, x:float, y:float, z:float=0):
        '''
        Adding x, y, z to dot's coordinatesx
        '''
        self.x += x
        self.y += y
        self.z += z
    
    def rotate(self, angle:float, cx:float=0, cy:float=0):
        '''
        rotate dot to angle from (cx, yx)
        '''
        copy_x = self.x
        copy_y = self.y
        self.x = cx + (copy_x - cx) * m.cos(angle) - (copy_y - cy) * m.sin(angle)
        self.y = cy + (copy_y - cy) * m.cos(angle) + (copy_x - cx) * m.sin(angle)
    
    def scale(self, kx:float, ky:float, cx:float=0, cy:float=0):
        '''
        scale dot's coord with x and y from (cx, yx)
        '''
        self.x = cx + kx * (self.x - cx)
        self.y = cy + ky * (self.y - cy)
    
    def __str__(self) -> str:
        return f'({round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)})'

class Picture():
    picture_dots = []
    def __init__(self):
        self.picture_dots = []
        
        self.center_circle  = None
        self.cross          = None
        self.center_rhombus = None
        self.left_circle    = None
        self.right_circle   = None
        self.main_rectangle = None

        self.getCenterCircle()
        self.getCenterCross()
        self.getCenterRhombus()
        self.getLeftHalfCircle()
        self.getRightHalfCircle()
        self.getMainRectangle()
    
    def getCenterCircle(self) -> list:
        if self.center_circle is None:
            self.center_circle = []

            for i in np.linspace(-1, 1, num=CIRCLE_APPROXIMATION_DOTS):
                self.center_circle.append(Point(i, up_center_circle(i)))
            
            for i in np.linspace(-1, 1, num=CIRCLE_APPROXIMATION_DOTS):
                self.center_circle.append(Point(i, down_center_circle(i)))
            
            self.picture_dots.extend(self.center_circle)
        return self.center_circle


    def getCenterCross(self) -> list:
        if (self.cross is None):
            self.cross = []
            self.cross = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]
            self.picture_dots.extend(self.cross)

        return self.cross

    def getCenterRhombus(self) -> list:
        if self.center_rhombus is None:
            self.center_rhombus = []

            self.center_rhombus = [Point(0, -2), Point(-5, 0), Point(0, 2), Point(5, 0)]
            self.picture_dots.extend(self.center_rhombus)

        return self.center_rhombus

    def getLeftHalfCircle(self) -> list:
        if self.left_circle is None:
            self.left_circle = []
            for i in np.linspace(3, 5, num=CIRCLE_APPROXIMATION_DOTS):
                self.left_circle.append(Point(i - 10, up_circle(i), 1))
            
            for i in np.linspace(3, 5, num=CIRCLE_APPROXIMATION_DOTS):
                self.left_circle.append(Point(i - 10, down_circle(i), 1))
            
            self.picture_dots.extend(self.left_circle)

        return self.left_circle

    def getRightHalfCircle(self) -> list:
        if self.right_circle is None:
            self.right_circle = []

            for i in np.linspace(5, 7, num=CIRCLE_APPROXIMATION_DOTS):
                self.right_circle.append(Point(i, up_circle(i), 1))
            
            for i in np.linspace(5, 7, num=CIRCLE_APPROXIMATION_DOTS):
                self.right_circle.append(Point(i, down_circle(i), 1))
            
            self.picture_dots.extend(self.right_circle)

        return self.right_circle
    
    def getMainRectangle(self) -> list:
        if self.main_rectangle is None:
            self.main_rectangle = []
            self.main_rectangle = [Point(-5, -2), Point(-5, 2), Point(5, 2), Point(5, -2)]
            self.picture_dots.extend(self.main_rectangle)

        return self.main_rectangle
    

    def restart(self):
        self.__init__()
    
    def scale(self, x:float, y:float, cx:float=0, cy:float=0):
        for ind, val in enumerate(self.picture_dots):
            val.scale(x, y, cx, cy)

    def move(self, x:float, y:float):
        for ind, val in enumerate(self.picture_dots):
            val.move(x, y)

    def rotate(self, angle:float, cx:float=0, cy:float=0):
        for ind, val in enumerate(self.picture_dots):
            val.rotate(angle, cx, cy)
        

    def rh_circle_wrap(self):
        '''
        Conveniant wrap around getRightHalfCircle for matplotlib
        '''
        circle = self.getRightHalfCircle()

        ux = [i.x for i in circle[:CIRCLE_APPROXIMATION_DOTS]]
        uy = [i.y for i in circle[:CIRCLE_APPROXIMATION_DOTS]]

        dx = [i.x for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
        dy = [i.y for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
    
        return [ux, uy], [dx, dy]
    
    def lh_circle_wrap(self):
        '''
        Conveniant wrap around getLeftHalfCircle for matplotlib
        '''
        circle = self.getLeftHalfCircle()

        ux = [i.x for i in circle[:CIRCLE_APPROXIMATION_DOTS]]
        uy = [i.y for i in circle[:CIRCLE_APPROXIMATION_DOTS]]

        dx = [i.x for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
        dy = [i.y for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
    
        return [ux, uy], [dx, dy]
    
    def center_circle_wrap(self):
        '''
        Conveniant wrap around getCenterCircle for matplotlib
        '''
        circle = self.getCenterCircle()

        ux = [i.x for i in circle[:CIRCLE_APPROXIMATION_DOTS]]
        uy = [i.y for i in circle[:CIRCLE_APPROXIMATION_DOTS]]

        dx = [i.x for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
        dy = [i.y for i in circle[CIRCLE_APPROXIMATION_DOTS:]]
    
        return [ux, uy], [dx, dy]
