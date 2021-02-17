import tkinter
import interface
import geom as g
import sympy as sy
import logging as log
from pprint import pprint

def main():
    interface.ROOT_WINDOW = interface.RootWindow()
    interface.ROOT_WINDOW.mainloop()


if __name__ == '__main__':
    # log.basicConfig(level=log.disable)
    
    table = [
        '1 ; 0 ; -3 ; 1',
        '2 ; -1 ; -2 ; 1',
        '3 ; -2 ; -2 ; 1',
        '4 ; -2 ; -1 ; 1',
        '5 ; 1 ; 0 ; 2',
        '6 ; 2 ; 0 ; 2',
        '7 ; 3 ; 0 ; 2',
        '8 ; 2 ; 1 ; 2'
    ]

    # min_ = g.solve_problem(table)
    # print('------------------- DONE -------------------')
    # print(min_.area)

    # polygon = [sy.Point(0, 0), sy.Point(1, 0), sy.Point(1, 1), sy.Point(0, 1)]

    # lib_area = sy.Polygon(polygon[0], polygon[1], polygon[2], polygon[3]).area
    # my_area  = g.quadrangle_area(polygon[0], polygon[1], polygon[2], polygon[3])

    # print(lib_area, my_area) 

    main()
