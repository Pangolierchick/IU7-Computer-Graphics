import functools
import math
import sympy as sy
import interface as ie
from itertools import combinations
import logging as log


class GeomError(Exception):
    pass


class NotEnoughDots(GeomError):
    def __init__(self, expression, message):
        self.message = message
        self.expression = expression

class NotEnoughCircles(GeomError):
    def __init__(self, expression, message):
        self.message = message
        self.expression = expression

class UnsolvableProblem(GeomError):
    def __init__(self, expression, message):
        self.message = message
        self.expression = expression

class myPoint:
    def __init__(self, coord:tuple, set_num:int, ind:int, ) -> None:
        self.sy_point = sy.Point(coord[0], coord[1], evaluate=False)
        self.ind = int(ind)
        self.set_num = int(set_num)

class Picture:
    area = None
    def __init__(self, circle1, circle2, tangent1:tuple, tangent2:tuple, i_c:tuple):
        self.tangent1 = tangent1
        self.tangent2 = tangent2

        self.circle1 = circle1
        self.circle2 = circle2

        self.i_p = i_c

        # self.get_area()

    def get_area(self) -> float:
        if (self.area is not None):
            return self.area

        left_quad_area = quadrangle_area(self.circle1.center, self.tangent1[0], sy.Point(self.i_p[0], self.i_p[1]), self.tangent2[0])
        right_quad_area = quadrangle_area(self.circle2.center, self.tangent1[1], sy.Point(self.i_p[0], self.i_p[1]), self.tangent2[1])

        log.debug(f'coord1 {self.tangent1[0]} {self.tangent2[0]} {self.circle1.center} {sy.Point(self.i_p[0], self.i_p[1])}')
        log.debug(f'coord2 {self.tangent1[1]} {self.tangent2[1]} {self.circle2.center} {sy.Point(self.i_p[0], self.i_p[1])}')

        log.info(f"Area: {left_quad_area} + {right_quad_area} = {left_quad_area + right_quad_area}")

        self.area = abs(left_quad_area - right_quad_area)

        return self.area

class myCircle(sy.Circle):
    def __init__(self, dot1, dot2, dot3):
        super().__init__()
        
    def set_points(self, dot1, dot2, dot3):
        self.dots = [dot1, dot2, dot3]


class Vector:
    def __init__(self, dot1, dot2):
        self.x = dot2.x - dot1.x
        self.y = dot2.y - dot1.y
    
    def mod(self) -> float:
        return math.sqrt(self.x**2 + (self.y**2))
    
    def scalar_prod(self, vec) -> float:
        return (self.x * vec.x + self.y * vec.y)
    
    def cos(self, vec) -> float:
        return (self.scalar_prod(vec)) / (self.mod() * vec.mod())
    
    def sin(self, vec) -> float:
        return math.sqrt(1 - self.cos(vec)**2)


def get_dots(dots_table:list) -> list:
    dots_1 = []
    dots_2 = []

    for record in dots_table:
        fields = record.split(" ; ")

        print(fields)
        print('field', fields[0])
        dot = myPoint((fields[1], fields[2]), fields[3], fields[0])
        
        if int(fields[3]) == 1:
            dots_1.append(dot)
        else:
            dots_2.append(dot)
    
    return dots_1, dots_2

def find_circles(dots_list:tuple) -> list:
    circles = []
    for pos_circle in combinations(dots_list, 3):
        circle = myCircle(pos_circle[0].sy_point, pos_circle[1].sy_point, pos_circle[2].sy_point)
        
        if (type(circle) == myCircle):
            circle.set_points(pos_circle[0], pos_circle[1], pos_circle[2])
            circles.append(circle)

    return circles

def find_pictures(circles_1:list, circles_2:list) -> list:
    pictures = []

    for circle_1 in circles_1:
        for circle_2 in circles_2:
            tangents = find_circles_tangent(circle_1, circle_2)

            if tangents:
                picture = Picture(circle_1, circle_2, tangents[0], tangents[1], tangents[2])
                pictures.append(picture)
    
    return pictures

def get_x_out(circle:myCircle, x_p:float, y_p:float):
    a = (circle.radius**2) * (x_p - circle.center.x)
    b = (circle.radius) * (y_p - circle.center.y)
    c = (math.sqrt((x_p - circle.center.x)**2 + (y_p - circle.center.y)**2 - (circle.radius**2)))
    d = ((x_p - circle.center.x)**2 + (y_p - circle.center.y)**2)


    xt_1 = ((a + b * c) / (d)) + circle.center.x
    xt_2 = ((a - b * c) / (d)) + circle.center.x

    return xt_1, xt_2

def get_y_out(circle:myCircle, x_p:float, y_p:float):
    a = (circle.radius**2) * (y_p - circle.center.y)
    b = (circle.radius) * (x_p - circle.center.x)
    c = (math.sqrt((x_p - circle.center.x)**2 + (y_p - circle.center.y)**2 - (circle.radius**2)))
    d = ((x_p - circle.center.x)**2 + (y_p - circle.center.y)**2)


    yt_1 = ((a - b * c) / (d)) + circle.center.y
    yt_2 = ((a + b * c) / (d)) + circle.center.y

    return yt_1, yt_2

def get_x_inner(circle:myCircle, x_p:float, y_p:float):
    return get_x_out(circle, x_p, y_p)

def get_y_inner(circle:myCircle, x_p:float, y_p:float):
    return get_y_out(circle, x_p, y_p)

@functools.lru_cache
def find_circles_tangent(circle1:myCircle, circle2:myCircle) -> tuple:
    # r0 -> a, b
    # r1 -> c, d

    if (circle1.intersect(circle2) or circle1.encloses(circle2)):
        log.warn("Tangents don't exist")
        return tuple()

    x_p = (circle1.radius * circle2.center.x + circle2.radius * circle1.center.x) / (circle1.radius + circle2.radius)
    y_p = (circle1.radius * circle2.center.y + circle2.radius * circle1.center.y) / (circle1.radius + circle2.radius)

    log.info(f'Tangents intersection ({x_p}, {y_p})')

    try:
        xt_1, xt_2 = get_x_out(circle1, x_p, y_p)
        yt_1, yt_2 = get_y_out(circle1, x_p, y_p)
    except Exception as e:
        return tuple()

    xt_3, xt_4 = get_x_inner(circle2, x_p, y_p)
    yt_3, yt_4 = get_y_inner(circle2, x_p, y_p)


    log.info(f'First tangent ({xt_1}, {yt_1}) ({xt_3}, {yt_3})')
    log.info(f'Second tangent ({xt_2}, {yt_2}) ({xt_4}, {yt_4})')

    return ((sy.Point(xt_1, yt_1), sy.Point(xt_3, yt_3)), (sy.Point(xt_2, yt_2), sy.Point(xt_4, yt_4)), (x_p, y_p))



def solve_problem(dots_table:list) -> Picture:
    dots_1, dots_2 = get_dots(dots_table)

    if (not dots_1 or not dots_2):
        raise NotEnoughDots(len(dots_1) + len(dots_2), 'Not enough dots given. Have to be at least 6')

    
    circles_1 = find_circles(dots_1)
    circles_2 = find_circles(dots_2)

    if (not circles_1 or not circles_2):
        raise NotEnoughCircles(len(circles_1) + len(circles_2), 'Not enough circles. Have to be at least 2')

    pictures = find_pictures(circles_1, circles_2)

    if not len(pictures):
        raise UnsolvableProblem(len(pictures), 'This problem cant be solved. Not enough tangents')
    
    min_area = pictures[0]

    for picture in pictures[1:]:
        if picture.get_area() < min_area.get_area():
            min_area = picture
    
    return min_area

@functools.lru_cache
def quadrangle_area(a, b, c, d):
    d1 = Vector(a, c)
    d2 = Vector(b, d)

    return d1.mod() * d2.mod() * d1.sin(d2) / 2
