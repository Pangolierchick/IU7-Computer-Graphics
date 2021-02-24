import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAIN_WINDOW_WIDTH = 1300
MAIN_WINDOW_HEIGHT = 750

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.draw_main()
    

    def draw_main(self):
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")
        self.resizable(1, 0)
        self.title('lab 2')

        self.plt_win = plt.figure()
        plt.grid(True)
        plt.autoscale(True)

        ax = self.plt_win.add_subplot(111)
        bar = FigureCanvasTkAgg(self.plt_win, self)
        bar.get_tk_widget().grid(row=0, column=2, rowspan=20, sticky='nsew')
        ax.set_title('Lab 2')

        tk.Label(self, text='ПОВОРОТ').grid(row=0, column=0, columnspan=2, rowspan=1)

        tk.Label(self, text='Угол').grid(row=1, column=0, columnspan=2)
        self.rotate_angle = tk.Entry(self)
        self.rotate_angle.grid(row=2, column=0, columnspan=2)

        rotate = tk.Button(self, text='Повернуть')
        rotate.grid(row=3, column=0, columnspan=2, sticky='n')

        tk.Label(self, text='МАСШТАБИРОВАНИЕ').grid(row=4, column=0, columnspan=2, sticky='n')
        tk.Label(self, text='x').grid(row=5, column=0, sticky='n')
        tk.Label(self, text='y').grid(row=5, column=1, sticky='n')
        self.x_scale = tk.Entry(self)
        self.x_scale.grid(row=6, column=0)
        self.y_scale = tk.Entry(self)
        self.y_scale.grid(row=6, column=1)

        scale = tk.Button(self, text='Масштабировать')
        scale.grid(row=7, column=0, columnspan=2)    

        tk.Label(self, text='ЦЕНТР МАСШТАБИРОВАНИЯ И ПОВОРОТА').grid(row=8, column=0, columnspan=2, sticky='s')
        tk.Label(self, text='x').grid(row=9, column=0, sticky='s')
        tk.Label(self, text='y').grid(row=9, column=1, sticky='s')
        self.x_center = tk.Entry(self)
        self.x_center.grid(row=10, column=0)
        self.y_center = tk.Entry(self)
        self.y_center.grid(row=10, column=1)

        default = tk.Button(self, text='Вернуть в исходное состояние')
        default.grid(row=11, column=0, columnspan=2, sticky='s', pady=25)
        
        back = tk.Button(self, text='Назад')
        back.grid(row=12, column=0, columnspan=2, sticky='s')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        # self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
