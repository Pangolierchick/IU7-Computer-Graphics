from functools import reduce
from math import inf
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import geom as g

ADD  = 0
EDIT = 1

ACTION = None
IND_TO_EDIT = 0
ROOT_WINDOW = None

DOT_RADIUS = 5

CANVAS_HALF_WIDTH = 0.8 * 312
CANVAS_HALF_HEIGHT = 0.8 * 250

TASK = 'На плоскости заданы два множества точек. Найти пару окружностей, каждые из которых проходят хотя бы через три различные точки \
        одного и того же множества (окружности строятся на точках разных множеств) таких, что разность площадей четырехугольников, образованных\
        центрами окружностей, точками касания внутренних общих касательных и точки пересечения касательных, минимальна. Сделать в графическом режиме ввод изображения'

class RootWindow():
    main_window = None
    mainCanvas = None
    dot_win = None

    dots = []

    dot_num = 1

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x520+298+48")
        self.main_window.resizable(0, 0)
        self.setup_main_window()
        messagebox.showinfo(title='Условие задачи', message=TASK)

    def mainloop(self):
        self.main_window.mainloop()
        self.mainCanvas.mainloop()

    def setup_main_window(self):
        self.mainCanvas = tk.Canvas(self.main_window, bg='lavender', width=625, height=500)
        self.mainCanvas.grid(row=0, column=1, rowspan=8)

        self.main_window.title('lab 1')

        tk.Label(self.main_window, text='ТОЧКИ').grid(row=0, column=0)


        self.dots_list = tk.Listbox(self.main_window, selectmode=tk.EXTENDED, justify='center')
        self.dots_list.bind("<Double-Button-1>", lambda event: self.check_list_box())
        self.dots_list.grid(row=2, column=0)

        add_dot_btn = tk.Button(self.main_window, text='Добавить точку', width=15)
        add_dot_btn.bind('<Button-1>', lambda event: self.add_dot())
        add_dot_btn.grid(row=3, column=0)

        self.edit_dot_btn = tk.Button(self.main_window, text='Изменить точку', width=15)
        self.edit_dot_btn.bind('<Button-1>', lambda event: self.edit_dot())
        self.edit_dot_btn.grid(row=4, column=0)


        self.del_dot_btn = tk.Button(self.main_window, text='Удалить точку', width=15)
        self.del_dot_btn.bind('<Button-1>', lambda event: self.del_dot())
        self.del_dot_btn.grid(row=5, column=0)


        self.edit_dot_btn.configure(state='disabled')
        self.del_dot_btn.configure(state='disabled')

        clear_table = tk.Button(self.main_window, text='Очистить таблицу', width=15)
        clear_table.bind('<Button-1>', lambda event: self.clear_table())
        clear_table.grid(row=6, column=0)

        solve_problem = tk.Button(self.main_window, text='Решить задачу', width=15)
        solve_problem.bind('<Button-1>', lambda event: self.solve_problem())
        solve_problem.grid(row=7, column=0)


    def get_dots_from_table(self) -> list:
        for ind, dot in enumerate(self.dots_list.get(0, tk.END)):
            self.dots.append(list(map(float, dot.split(' ; '))))

        return self.dots

    def solve_problem(self):
        self.mainCanvas.delete('all')
        dots = self.get_dots_from_table()


        try:
            min_pic = g.solve_problem(self.dots_list.get(0, tk.END))
        except g.NotEnoughDots:
            messagebox.showerror(title='Ошибка', message='Ошибка: задача не может быть решена. Недостаточно точек (минимум 3 во мн. 1 и 3 во мн. 2)')
            return
        except g.NotEnoughCircles:
            messagebox.showerror(title='Ошибка', message='Ошибка: задача не может быть решена. Не было найдено достаточно окружностей')
            return
        except g.UnsolvableProblem:
            messagebox.showerror(title='Ошибка', message='Ошибка: задача не может быть решена. Не было найдено окружностей, для которых можно построить касательные')
            return

        
        x_offset = min_pic.i_p[0]
        y_offset = min_pic.i_p[1]

        c1x = min_pic.circle1.center.x - x_offset
        c1y = min_pic.circle1.center.y - y_offset
        
        c2x = min_pic.circle2.center.x - x_offset
        c2y = min_pic.circle2.center.y - y_offset

        t11x = min_pic.tangent1[0].x - x_offset
        t11y = min_pic.tangent1[0].y - y_offset
        t12x = min_pic.tangent1[1].x - x_offset
        t12y = min_pic.tangent1[1].y - y_offset
        
        t21x = min_pic.tangent2[0].x - x_offset
        t21y = min_pic.tangent2[0].y - y_offset
        t22x = min_pic.tangent2[1].x - x_offset
        t22y = min_pic.tangent2[1].y - y_offset


        some_x_dots = [c1x + min_pic.circle1.radius, c1x - min_pic.circle1.radius,
                       c2x + min_pic.circle2.radius, c2x - min_pic.circle2.radius]

        some_y_dots = [c1y + min_pic.circle1.radius, c1y - min_pic.circle1.radius,
                       c2y + min_pic.circle2.radius, c2y - min_pic.circle2.radius]

        right = max(some_x_dots)
        left  = min(some_x_dots)
        up    = max(some_y_dots)
        down  = max(some_y_dots)


        x_scale_r = abs(CANVAS_HALF_WIDTH // right) if right != 0 else inf
        x_scale_l = abs(CANVAS_HALF_WIDTH // left) if left != 0 else inf

        y_scale_u = abs(CANVAS_HALF_HEIGHT // up) if up != 0 else inf
        y_scale_d = abs(CANVAS_HALF_HEIGHT // down) if down != 0 else inf

        scale = min(x_scale_r, x_scale_l, y_scale_u, y_scale_d) - 1

        c1_x = int(scale * c1x + CANVAS_HALF_WIDTH)
        c1_y = int(-scale * c1y + CANVAS_HALF_HEIGHT)
        c1_r = int(scale * min_pic.circle1.radius)
        self.mainCanvas.create_oval(c1_x - c1_r, c1_y + c1_r, c1_x + c1_r, c1_y - c1_r, width=2, outline='red')


        c2_x = int(scale * c2x + CANVAS_HALF_WIDTH)
        c2_y = int(-scale * c2y + CANVAS_HALF_HEIGHT)
        c2_r = int(scale * min_pic.circle2.radius)
        self.mainCanvas.create_oval(c2_x - c2_r, c2_y + c2_r, c2_x + c2_r, c2_y - c2_r, width=2, outline='blue')

        t1_1_x = int(scale * t11x + CANVAS_HALF_WIDTH)
        t1_1_y = int(-scale * t11y + CANVAS_HALF_HEIGHT)
        t1_2_x = int(scale * t12x + CANVAS_HALF_WIDTH)
        t1_2_y = int(-scale * t12y + CANVAS_HALF_HEIGHT)
        self.mainCanvas.create_line(t1_1_x, t1_1_y, t1_2_x, t1_2_y, width=2)


        t2_1_x = int(scale * t21x + CANVAS_HALF_WIDTH)
        t2_1_y = int(-scale * t21y + CANVAS_HALF_HEIGHT)
        t2_2_x = int(scale * t22x + CANVAS_HALF_WIDTH)
        t2_2_y = int(-scale * t22y + CANVAS_HALF_HEIGHT)

        self.mainCanvas.create_line(t2_1_x, t2_1_y, t2_2_x, t2_2_y, width=2)

        self.mainCanvas.create_line(c1_x, c1_y, t1_1_x, t1_1_y, width=2)
        self.mainCanvas.create_line(c1_x, c1_y, t2_1_x, t2_1_y, width=2)
        self.mainCanvas.create_line(c2_x, c2_y, t1_2_x, t1_2_y, width=2)
        self.mainCanvas.create_line(c2_x, c2_y, t2_2_x, t2_2_y, width=2)

        user_dots_1 = list(map(lambda x: scale_dot(x.sy_point.x, x.sy_point.y, x_offset, y_offset, scale), min_pic.circle1.dots))
        user_dots_2 = list(map(lambda x: scale_dot(x.sy_point.x, x.sy_point.y, x_offset, y_offset, scale), min_pic.circle2.dots))

        ind = 0
        for dot in (user_dots_1):
            self.mainCanvas.create_text(dot[0] - 20, dot[1] + 20, text=f'{min_pic.circle1.dots[ind].ind}')
            self.mainCanvas.create_oval(dot[0] - DOT_RADIUS, dot[1] + DOT_RADIUS, dot[0] + DOT_RADIUS, dot[1] - DOT_RADIUS, fill='green')
            ind += 1
        
        ind = 0
        for dot in (user_dots_2):
            self.mainCanvas.create_text(dot[0] - 20, dot[1] + 20, text=f'{min_pic.circle2.dots[ind].ind}')
            self.mainCanvas.create_oval(dot[0] - DOT_RADIUS, dot[1] + DOT_RADIUS, dot[0] + DOT_RADIUS, dot[1] - DOT_RADIUS, fill='purple')
            ind += 1

        # print('area', float(min_pic.get_area()))

        messagebox.showinfo(title='Ответ', message=f'Ответ: минимальная разность площадей четырехугольников равна {float(min_pic.get_area()):.4}. Изображение Вы можете увидеть на экране. \
                                                     Точки мн. 1 изображены зеленым цветом, мн. 2 -- фиолетовым. Окружность мн. 1 красным цветом -- мн. 2 синим. Касательные -- черным.')


    def add_dot(self):
        global ACTION # sorry for that

        self.dot_win = AddDotWin(self.main_window)
        ACTION = ADD

    def edit_dot(self):
        global ACTION, IND_TO_EDIT # i'm so sorry ;(

        self.dot_win = AddDotWin(self.main_window)
        ACTION = EDIT

        ind = self.dots_list.curselection()[0]
        dot_coord = self.dots_list.get(ind).split(' ; ')

        IND_TO_EDIT = ind

        self.dot_win.xentry.delete(0, tk.END)
        self.dot_win.xentry.insert(0, dot_coord[1])

        self.dot_win.yentry.delete(0, tk.END)
        self.dot_win.yentry.insert(0, dot_coord[2])

        self.dot_win.set_var.set(dot_coord[3])

        self.dot_num -= 1

    def del_dot(self):
        ind = self.dots_list.curselection()[0]
        self.dots_list.delete(ind)
        self.check_list_box()
        self.recheck_listbox()
        self.dot_num -= 1

    def clear_table(self):
        self.dots_list.delete(0, tk.END)
        self.check_list_box()
        self.dot_num = 0
        self.mainCanvas.delete('all')


    def check_list_box(self):
        if len(self.dots_list.get(0, tk.END)) == 0: # if listbox is empty we block buttons
            state = tk.DISABLED
        else:
            state = tk.NORMAL

        self.edit_dot_btn.configure(state=state)
        self.del_dot_btn.configure(state=state)
    
    def recheck_listbox(self):
        old = self.dots_list.get(0, tk.END)
        ind = len(old)
        new = []

        for i in old:
            rec = i.split(' ; ')[1:]
            new.append(f'{ind} ; {rec[0]} ; {rec[1]} ; {rec[2]}')
            ind -= 1
        
        self.dots_list.delete(0, tk.END)

        for i, e in enumerate(new):
            self.dots_list.insert(i, e)


class AddDotWin(tk.Toplevel):
    vals = None

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.geometry('300x130')

        self.title('Add dot')

        self.xlabel = tk.Label(self, text='x', justify='center')
        self.xlabel.grid(row=0, column=0)

        self.ylabel = tk.Label(self, text='y', justify='center')
        self.ylabel.grid(row=0, column=1)

        self.xentry = tk.Entry(self, width=10, justify='center')
        self.xentry.grid(row=1, column=0)
        self.xentry.insert(0, '0')

        self.yentry = tk.Entry(self, width=10, justify='center')
        self.yentry.grid(row=1, column=1)
        self.yentry.insert(0, '0')

        self.set_var = tk.IntVar()
        self.set_var.set(1)

        set_1 = tk.Radiobutton(self, text='Множ. 1', variable=self.set_var, value=1)
        set_2 = tk.Radiobutton(self, text='Множ. 2', variable=self.set_var, value=2)

        set_1.grid(row=0, column=2)
        set_2.grid(row=1, column=2)

        self.add_btn = tk.Button(self, text='Ok')
        self.add_btn.grid(row=2, column=1)
        self.add_btn.bind("<Button-1>", lambda event: conf_dot(ROOT_WINDOW, self))


    def get_entries(self) -> tuple:
        return [ROOT_WINDOW.dot_num, self.xentry.get(), self.yentry.get(), self.set_var.get()]


def find_in_listbox(listbox:tk.Listbox, record:list) -> bool:
    for i in listbox.get(0, tk.END):
        if list(map(float, i.split(' ; ')[1:])) == record:
            return True
    return False



def conf_dot(root:RootWindow, dot_win:AddDotWin):
    items = dot_win.get_entries()

    try:
        items = [items[0]] + list(map(float, items[1:3])) + [int(items[3])]
        print(items)
    except ValueError:
        messagebox.showerror(title='Ошибка', message='Не все значения имеют вещественный тип. Проверьте ввод')
        return None

    # if find_in_listbox(root.dots_list, [items[1], items[2], items[3]]):
    #     messagebox.showerror(title='Ошибка', message='Такая точка уже добавлена.')
    # else:
    ind = 0
    if ACTION == ADD:
        pass
    else:
        ind = IND_TO_EDIT
        root.dots_list.delete(ind)

    root.dots_list.insert(ind, f"{items[0]} ; {items[1]} ; {items[2]} ; {items[3]}")

    dot_win.destroy()


    root.check_list_box()
    root.recheck_listbox()
    root.dot_num += 1


def scale_dot(x, y, x_off, y_off, scale):
    return (int(scale * (x - x_off) + CANVAS_HALF_WIDTH), int(-scale * (y - y_off) + CANVAS_HALF_HEIGHT))
