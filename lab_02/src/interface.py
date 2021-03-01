import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geom as g
import math
from copy import deepcopy

MAIN_WINDOW_WIDTH = 1300
MAIN_WINDOW_HEIGHT = 750

class mainWindow(tk.Tk):
    pic_condition_stack = []

    def __init__(self):
        super().__init__()
        self.draw_main()
    

    def draw_main(self):
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")
        self.resizable(1, 0)
        self.title('lab 2')

        self.plt_win = plt.figure(frameon=False)

        bar = FigureCanvasTkAgg(self.plt_win, self)
        bar.get_tk_widget().place(x=400, y=0, relheight=1, relwidth=0.7)

        tk.Label(self, text='ПОВОРОТ').place(x=165, y=50)

        tk.Label(self, text='Угол').place(x=180, y=80)
        self.rotate_angle = tk.Entry(self)
        self.rotate_angle.place(x=105, y=110)

        rotate = tk.Button(self, text='Повернуть', command=self.rotate_picture)
        rotate.place(x=145, y=140)

        tk.Label(self, text='МАСШТАБИРОВАНИЕ').place(x=125, y=200)
        tk.Label(self, text='x').place(x=125, y=230)
        tk.Label(self, text='y').place(x=270, y=230)
        self.x_scale = tk.Entry(self, width=10)
        self.x_scale.place(x=75, y=260)
        self.y_scale = tk.Entry(self, width=10)
        self.y_scale.place(x=225, y=260)

        scale = tk.Button(self, text='Масштабировать', command=self.scale_picture)
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
        self.move_x = tk.Entry(self, width=10)
        self.move_x.place(x=75, y=500)
        self.move_y = tk.Entry(self, width=10)
        self.move_y.place(x=225, y=500)

        move = tk.Button(self, text='Переместить', command=self.move_picture)
        move.place(x=130, y=530)

        default = tk.Button(self, text='Вернуть в исходное состояние', command=self.reset_picture)
        default.place(x=80, y=580)
        
        back = tk.Button(self, text='Назад', command=self.go_back)
        back.place(x=160, y=610)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        self.set_default_values()

        self.paint = g.Picture()
        self.draw_paint()
    
    def go_back(self):
        print(f"Go back! Stack len {len(self.pic_condition_stack)}")

        try:
            self.paint = self.pic_condition_stack.pop()
        except IndexError:
            print("end of stack of changes")
            return
        
        self.draw_paint()
    
    def set_default_values(self):
        self.rotate_angle.insert(0, 0)
        self.x_center.insert(0, 0)
        self.x_scale.insert(0, 1)
        self.move_x.insert(0, 0)
        self.y_center.insert(0, 0)
        self.y_scale.insert(0, 1)
        self.move_y.insert(0, 0)

    def move_picture(self):
        try:
            x = float(self.move_x.get())
            y = float(self.move_y.get())
        except ValueError:
            messagebox.showerror(title='Ошибка', message='Неправильный ввод координат смещения')
            return

        print(f'Moving to {x}, {y}')
        self.save_condition()
        self.paint.move(x, y)
        self.draw_paint()

    def rotate_picture(self):
        try:
            angle = math.radians(float(self.rotate_angle.get()))
            cx = float(self.x_center.get())
            cy = float(self.y_center.get())
        except ValueError:
            messagebox.showerror(title='Ошибка', message='Неправильный ввод центра поворота или угла')
            return

        print(f'Rotating from {cx}, {cy} to {angle:.3}')

        self.save_condition()
        self.paint.rotate(angle, cx, cy)
        self.draw_paint()
    
    def save_condition(self):
        self.pic_condition_stack.append(deepcopy(self.paint))

    def scale_picture(self):
        try:
            kx = float(self.x_scale.get())
            ky = float(self.y_scale.get())
            cx = float(self.x_center.get())
            cy = float(self.y_center.get())
        except ValueError:
            messagebox.showerror(title='Ошибка', message='Неправильный ввод центра масштабирования или коэффициентов масштабирования')
            return
        
        self.save_condition()
        self.paint.scale(kx, ky, cx, cy)
        self.draw_paint()
    
    def reset_picture(self):
        self.pic_condition_stack = []
        self.paint.restart()
        self.draw_paint()
    

    def draw_paint(self):
        plt.cla()
        plt.grid(True)
        # plt.autoscale(True)
        plt.xlim([-15, 15])
        plt.ylim([-15, 15])

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

        up_part, down_part = self.paint.center_circle_wrap()

        plt.plot(up_part[0], up_part[1], 'b-')
        plt.plot(down_part[0], down_part[1], 'b-')

        up_part, down_part = self.paint.lh_circle_wrap()

        plt.plot(up_part[0], up_part[1], 'b-')
        plt.plot(down_part[0], down_part[1], 'b-')

        up_part, down_part = self.paint.rh_circle_wrap()

        plt.plot(up_part[0], up_part[1], 'b-')
        plt.plot(down_part[0], down_part[1], 'b-')

        plt.draw()



        
