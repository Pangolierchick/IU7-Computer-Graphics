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

        self.plt_win = plt.figure(frameon=False)
        plt.grid(True)
        plt.autoscale(True)

        bar = FigureCanvasTkAgg(self.plt_win, self)
        bar.get_tk_widget().place(x=400, y=0, relheight=1, relwidth=0.7)

        tk.Label(self, text='ПОВОРОТ').place(x=165, y=50)

        tk.Label(self, text='Угол').place(x=180, y=80)
        self.rotate_angle = tk.Entry(self)
        self.rotate_angle.place(x=105, y=110)

        rotate = tk.Button(self, text='Повернуть')
        rotate.place(x=145, y=140)

        tk.Label(self, text='МАСШТАБИРОВАНИЕ').place(x=125, y=200)
        tk.Label(self, text='x').place(x=125, y=230)
        tk.Label(self, text='y').place(x=270, y=230)
        self.x_scale = tk.Entry(self, width=10)
        self.x_scale.place(x=75, y=260)
        self.y_scale = tk.Entry(self, width=10)
        self.y_scale.place(x=225, y=260)

        scale = tk.Button(self, text='Масштабировать')
        scale.place(x=120, y=290)

        tk.Label(self, text='ЦЕНТР МАСШТАБИРОВАНИЯ И ПОВОРОТА').place(x=50, y=350)
        tk.Label(self, text='x').place(x=125, y=380)
        tk.Label(self, text='y').place(x=270, y=380)
        self.x_center = tk.Entry(self, width=10)
        self.x_center.place(x=75, y=410)
        self.y_center = tk.Entry(self, width=10)
        self.y_center.place(x=225, y=410)

        tk.Label(self, text='ПЕРЕНОС').place(x=50, y=440)
        tk.Label(self, text='x').place(x=125, y=470)
        tk.Label(self, text='y').place(x=270, y=470)
        self.move_x_center = tk.Entry(self, width=10)
        self.x_center.place(x=75, y=500)
        self.y_center = tk.Entry(self, width=10)
        self.y_center.place(x=225, y=500)

        default = tk.Button(self, text='Вернуть в исходное состояние')
        default.place(x=80, y=550)
        
        back = tk.Button(self, text='Назад')
        back.place(x=160, y=580)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
