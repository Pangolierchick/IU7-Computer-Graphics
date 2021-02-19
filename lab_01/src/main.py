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

    main()
