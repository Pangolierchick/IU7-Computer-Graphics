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

def get_dots(dots_table:list) -> list:
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
    tangents = []


def get_x_out(circle1:sy.Circle, x_p:float, y_p:float):
    xt_1 = (((circle1.radius**2) * (x_p - circle1.center.x) + circle1.radius * (y_p - circle1.center.y) * 
            math.sqrt((x_p - circle1.center.x)**2 + (y_p - circle1.center.y)**2 - circle1.radius**2)) / 
            ((x_p - circle1.center.x)**2 + (y_p - circle1.center.y))) + circle1.center.x

    xt_2 = (((circle1.radius**2) * (x_p - circle1.center.x) - circle1.radius * (y_p - circle1.center.y) * 
            math.sqrt((x_p - circle1.center.x)**2 + (y_p - circle1.center.y)**2 - circle1.radius**2)) / 
            ((x_p - circle1.center.x)**2 + (y_p - circle1.center.y))) + circle1.center.x
    
    return xt_1, xt_2

def get_y_out(circle1:sy.Circle, x_p:float, y_p:float):
    yt_1 = (((circle1.radius**2) * (y_p - circle1.center.x) - circle1.radius * (y_p - circle1.center.y) * 
            math.sqrt((x_p - circle1.center.x)**2 + (y_p - circle1.center.y)**2 - circle1.radius**2)) / 
            ((x_p - circle1.center.x)**2 + (y_p - circle1.center.y))) + circle1.center.y
    
    yt_2 = (((circle1.radius**2) * (y_p - circle1.center.x) + circle1.radius * (y_p - circle1.center.y) * 
            math.sqrt((x_p - circle1.center.x)**2 + (y_p - circle1.center.y)**2 - circle1.radius**2)) / 
            ((x_p - circle1.center.x)**2 + (y_p - circle1.center.y))) + circle1.center.y
    
    return yt_1, yt_2

def get_x_inner(circle:sy.Circle, x_p:float, y_p:float):
    return get_x_out(circle, x_p, y_p)

def get_y_inner(circle:sy.Circle, x_p:float, y_p:float):
    return get_y_out(circle, x_p, y_p)


def find_tangents_inters(circle1:sy.Circle, circle2:sy.Circle):
    # r0 -> a, b
    # r1 -> c, d

    x_p = (circle1.radius * circle2.center.x + circle2.radius * circle1.center.x) / (circle1.radius + circle2.radius)
    y_p = (circle1.radius * circle2.center.y + circle2.radius * circle1.center.y) / (circle1.radius + circle2.radius)

    tan_int = sy.Point(x_p, y_p)

    xt_1, xt_2 = get_x_out(circle1, x_p, y_p)
    yt_1, yt_2 = get_y_out(circle1, x_p, y_p)

    xt_3, xt_4 = get_x_inner(circle2, x_p, y_p)
    yt_3, yt_4 = get_y_inner(circle2, x_p, y_p)

    tangents = (sy.Line(sy.Point(xt_1, yt_1), sy.Point(xt_3, yt_3)), sy.Line(sy.Point(xt_2, yt_2), sy.Point(xt_4, yt_4)))
    return tangents


def find_area():
    pass
