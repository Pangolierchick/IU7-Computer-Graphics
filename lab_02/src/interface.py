import tkinter as tk
from matplotlib import markers
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geom as g
import math

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
        # plt.autoscale(True)
        plt.xlim([-15, 15])
        plt.ylim([-15, 15])

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

        tk.Label(self, text='ПЕРЕНОС').place(x=160, y=450)
        tk.Label(self, text='x').place(x=125, y=470)
        tk.Label(self, text='y').place(x=270, y=470)
        self.move_x_center = tk.Entry(self, width=10)
        self.move_x_center.place(x=75, y=500)
        self.move_y_center = tk.Entry(self, width=10)
        self.move_y_center.place(x=225, y=500)

        default = tk.Button(self, text='Вернуть в исходное состояние')
        default.place(x=80, y=550)
        
        back = tk.Button(self, text='Назад')
        back.place(x=160, y=580)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        self.draw_paint()
    

    def draw_paint(self):
        self.paint = g.Picture()

        self.paint.rotate(math.radians(45))

        rec = self.paint.getMainRectangle()

        # --------------------- MAIN RECTANGLE ---------------------
        plt.plot((rec[0].x, rec[1].x), (rec[0].y, rec[1].y), 'b-')
        plt.plot((rec[1].x, rec[2].x), (rec[1].y, rec[2].y), 'b-')
        plt.plot((rec[2].x, rec[3].x), (rec[2].y, rec[3].y), 'b-')
        plt.plot((rec[3].x, rec[0].x), (rec[3].y, rec[0].y), 'b-')
        # ----------------------------------------------------------

        rhombus = self.paint.getCenterRhombus()

        # --------------------- CENTRAL RHOMBUS --------------------
        plt.plot((rhombus[0].x, rhombus[1].x), (rhombus[0].y, rhombus[1].y), 'b-')
        plt.plot((rhombus[2].x, rhombus[3].x), (rhombus[2].y, rhombus[3].y), 'b-')
        plt.plot((rhombus[0].x, rhombus[3].x), (rhombus[0].y, rhombus[3].y), 'b-')
        plt.plot((rhombus[1].x, rhombus[2].x), (rhombus[1].y, rhombus[2].y), 'b-')
        # ----------------------------------------------------------

        cross = self.paint.getCenterCross()

        # ------------------------- CROSS --------------------------
        plt.plot((cross[0].x, cross[1].x), (cross[0].y, cross[1].y), 'b-')
        plt.plot((cross[2].x, cross[3].x), (cross[2].y, cross[3].y), 'b-')
        # ----------------------------------------------------------

        central_circle = self.paint.getCenterCircle()

        cc_x = []
        cc_y = []

        for i in central_circle:
            cc_x.append(i.x)
            cc_y.append(i.y)

        plt.plot(cc_x, cc_y, 'b-')

        left_circle = self.paint.getLeftHalfCircle()

        lc_x = []
        lc_y = []

        for i in left_circle:
            lc_x.append(i.x)
            lc_y.append(i.y)
        
        plt.plot(lc_x[:g.CIRCLE_APPROXIMATION_DOTS], lc_y[:g.CIRCLE_APPROXIMATION_DOTS], 'b-')
        plt.plot(lc_x[g.CIRCLE_APPROXIMATION_DOTS:], lc_y[g.CIRCLE_APPROXIMATION_DOTS:], 'b-')

        right_circle = self.paint.getRightHalfCircle()

        rc_x = []
        rc_y = []

        for i in right_circle:
            rc_x.append(i.x)
            rc_y.append(i.y)
        
        plt.plot(rc_x[:g.CIRCLE_APPROXIMATION_DOTS], rc_y[:g.CIRCLE_APPROXIMATION_DOTS], 'b-')
        plt.plot(rc_x[g.CIRCLE_APPROXIMATION_DOTS:], rc_y[g.CIRCLE_APPROXIMATION_DOTS:], 'b-')



        
