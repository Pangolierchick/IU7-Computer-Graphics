from PyQt5.QtCore import QLine, QPoint


def checkConvex(polygon):
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
