import math
import sympy as sy
import interface as ie
from itertools import combinations


class myPoint:
    sy_point = None
    ind = None
    set_num = None

    def __init__(self, coord:tuple, set_num:int, ind:int, ) -> None:
        self.sy_point = sy.Point(coord[0], coord[1])
        self.ind = int(ind)
        self.set_num = int(set_num)

def get_dots(dots_table:list) -> list, list:
    dots_1 = []
    dots_2 = []
    
    for ind, record in enumerate(dots_table): # FIXME
        fields = record.split(" ; ")
        dot = myPoint((fields[0], fields[1]), fields[2], ind)
        if int(fields[2]) == 1:
            dots_1.append(dot)
        else:
            dots_2.append(dot)
    
    return dots_1, dots_2

def find_circles(dots_list:tuple) -> list:
    circles = []
    for pos_circle in combinations(dots_list, 3):
        try:
            circle = sy.Circle(pos_circle[0].sy_point, pos_circle[1].sy_point, pos_circle[2].sy_point)
        except sy.GeometryError:
            continue
        circles.append(circle)
    
    return circles

def find_tangents(circles_1:list, circles_2:list) -> list:
    pass

def find_tangents_inters():
    pass

def find_area():
    pass
