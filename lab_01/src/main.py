import tkinter
import interface
import geom as g
import sympy as s
import logging as log

def main():
    interface.ROOT_WINDOW = interface.RootWindow()
    interface.ROOT_WINDOW.mainloop()


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)
    
    main()

    table = [
        '0 ; -3 ; 1',
        '3  ; 0 ; 1',
        '0 ; 3 ; 1',
        '8 ; 4 ; 2',
        '9 ; 5 ; 2',
        '8 ; 6 ; 2',
    ]

    pic = g.solve_problem(table)

    print(pic.area)
