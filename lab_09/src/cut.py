from PyQt5.QtCore import QLine, QPointF

class Vector:
    def __init__(self, p1: QPointF, p2:QPointF=None):
        if p2 is not None:
            self.x = p2.x() - p1.x()
            self.y = p2.y() - p1.y()
        else:
            self.x = p1.x()
            self.y = p1.y()

    def vecProduct(self, v):
        return self.x * v.y - self.y * v.x

    def scalProduct(self, v):
        return self.x * v.x + self.y * v.y

    def __str__(self):
        return f'[{self.x}, {self.y}]'


def getNormal(d1:QPointF, d2:QPointF, d_check:QPointF) -> Vector:
    vec = Vector(d1, d2)

    if vec.x == 0:
        normal = Vector(QPointF(1, 0))
    else:
        normal = Vector(QPointF(-vec.y / vec.x, 1))

    if Vector(d2, d_check).scalProduct(normal) < 0:
        normal.x *= -1
        normal.y *= -1

    return normal

def getNormals(cutter:list[QPointF]) -> list[Vector]:
    normals = []

    cut_len = len(cutter)

    for i, v in enumerate(cutter):
        normals.append(getNormal(cutter[i], cutter[(i + 1) % cut_len], cutter[(i + 2) % cut_len]))

    return normals

def checkCutter(cutter:list[QPointF]) -> bool:
    if len(cutter) < 3:
        return False

    v1 = Vector(cutter[0], cutter[1])
    v2 = Vector(cutter[1], cutter[2])

    if v1.vecProduct(v2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(3, len(cutter)):
        vi = Vector(cutter[i - 2], cutter[i - 1])
        vj = Vector(cutter[i - 1], cutter[i])

        if sign * vi.vecProduct(vj) < 0:
            return False


    if sign < 0:
        cutter.reverse()

    return True

def isVisible(point:QPointF, d1:QPointF, d2:QPointF) -> bool:
    fvec = Vector(d1, d2)
    svec = Vector(d1, point)

    prod = fvec.vecProduct(svec)

    return prod >= 0


def getIntersection(section:list[QPointF], edge:list[QPointF], normal:Vector) -> QPointF:
    vec = Vector(section[0], section[1])
    w_vec = Vector(edge[0], section[0])

    vec_prod = vec.scalProduct(normal)
    w_vec_prod = w_vec.scalProduct(normal)

    diff = QPointF(section[1].x() - section[0].x(), section[1].y() - section[0].y())
    t = -w_vec_prod / vec_prod

    return QPointF(section[0].x() + diff.x() * t, section[0].y() + diff.y() * t)


def getCut(figure:list[QPointF], edge:list[QPointF], normal:Vector) -> list[QPointF]:
    res_fig = []
    figure_len = len(figure)

    if figure_len < 3:
        return []

    pcheck = isVisible(figure[0], edge[0], edge[1])

    for i in range(1, figure_len + 1):
        ccheck = isVisible(figure[i % figure_len], edge[0], edge[1])

        if pcheck:
            if ccheck:
                res_fig.append(figure[i % figure_len])
            else:
                res_fig.append(getIntersection([figure[i - 1], figure[i % figure_len]], edge, normal))
        else:
            if ccheck:
                res_fig.append(getIntersection([figure[i - 1], figure[i % figure_len]], edge, normal))
                res_fig.append(figure[i % figure_len])

        pcheck = ccheck

    return res_fig


def sutherlandhodgman(figure:list[QPointF], cut:list[QPointF], normals:list[Vector]) -> list[QPointF]:
    res_figure = figure

    for i, _ in enumerate(cut):
        edge = [cut[i], cut[(i + 1) % len(cut)]]
        print(f"Сторона - {edge}, нормаль - {str(normals[i])}")
        res_figure = getCut(res_figure, edge, normals[i])

        if len(res_figure) < 3:
            print('Empty.')
            return []

    return res_figure


def cut(figure, cutter):
    if not checkCutter(cutter):
        print('Something went wrong. Exitting')
        return []

    normals = getNormals(cutter)
    figure = sutherlandhodgman(figure, cutter, normals)

    print(figure)

    return figure
