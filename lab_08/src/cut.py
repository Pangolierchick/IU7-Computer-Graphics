from PyQt5.QtCore import QLine, QPoint

COUNTER_CLOCKWISE = -1

class Point3d:
    def __init__(self, x:int=0, y:int=0, z:int=0, qpoint:QPoint=None):
        if qpoint is None:
            self.x_ = int(x)
            self.y_ = int(y)
        else:
            self.x_ = int(qpoint.x())
            self.y_ = int(qpoint.y())

        self.z_ = int(z)

    def x(self):
        return self.x_

    def y(self):
        return self.y_

    def z(self):
        return self.z_

    def __sub__(self, v):
        return Point3d(self.x_ - v.x(), self.y_ - v.y(), self.z_ - v.z())

    def scalarProduct(self, v) -> int:
        '''
        Performs scalar multiplication
        '''
        return v.x() * self.x_ + v.y() * self.y_ + v.z() * self.z_

    def vectorProduct(self, v):
        res = Point3d()

        res.x_ = self.y() * v.z() - v.y() * self.z()
        res.y_ = v.x() * self.z() - self.x() * v.z()
        res.z_ = self.x() * v.y() - self.y() * v.x()

        return res

    def __str__(self):
        return f'({self.x_}, {self.y_}, {self.z_})'

    def P(self, p2, t):
        res = Point3d()

        res.x_ = self.x_ + round((p2.x_ - self.x_) * t)
        res.y_ = self.y_ + round((p2.y_ - self.y_) * t)
        res.z_ = self.z_ + round((p2.z_ - self.z_) * t)

        return res

def sign(x):
    return int((x > 0) - (x < 0))

def twoD2ThreeDPoly(poly):
    new = []

    for p in poly:
        new.append(Point3d(qpoint=p))

    return new

def normalizePoly(poly, direction):
    res = []

    for i in range(len(poly) - 1):
        b = poly[i] - poly[i + 1]

        if direction == COUNTER_CLOCKWISE:
            res.append(Point3d(b.y(), -b.x(), 0))
        else:
            res.append(Point3d(-b.y(), b.x(), 0))

    return res

def checkConvexity(polygon):
    '''
      0 - вырожденный
     -1 - невыпуклый
      1 - выпуклый
    '''

    n = len(polygon)

    if n < 3:
        return 0

    flag = 0

    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n

        z  = ((polygon[j].x() - polygon[i].x()) * (polygon[k].y() - polygon[j].y()))

        z -= ((polygon[j].y() - polygon[i].y()) * (polygon[k].x() - polygon[j].x()))

        if z < 0:
            flag |= 1
        elif z > 0:
            flag |= 2

        if flag == 3:
            return -1

    if flag != 0:
        return 1
    else:
        return 0

def direction(poly):
    a = poly[0] - poly[1]
    b = Point3d()

    l = len(poly)

    tmp = Point3d()
    res = 0

    for i in range(1, l - 1):
        b = poly[i] - poly[i + 1]
        tmp = a.vectorProduct(b)

        if res == 0:
            res = sign(tmp.z())

        if tmp.z() and res != sign(tmp.z()):
            return 0

        a = b

    return res

def cutLine(poly, normVect, qp1:QPoint, qp2:QPoint):
    visible = False

    p1 = Point3d(qpoint=qp1)
    p2 = Point3d(qpoint=qp2)

    n = len(poly) - 1

    diff = p1 - p2

    tbot = 0
    ttop = 1

    for i in range(n):
        w = poly[i] - p1
        dsk = diff.scalarProduct(normVect[i])
        wsk = w.scalarProduct(normVect[i])

        if dsk == 0: # вырожден ли в отрезок
            if wsk < 0: # если точка вне окна
                return visible, p1, p2
        else:
            t = -wsk / dsk

            if dsk > 0: # поиск верхнего и нижнего пределов t
                if t > 1:
                    return visible, p1, p2
                else:
                    tbot = max(tbot, t)
            else:
                if t < 0:
                    return visible, p1, p2
                else:
                    ttop = min(ttop, t)
    if tbot <= ttop: # нет противоречия
        tmp = p1.P(p2, tbot)
        p2 = p1.P(p2, ttop)

        p1 = tmp

        visible = True

    return visible, p1, p2

