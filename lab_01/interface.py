import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

ADD  = 0
EDIT = 1

ACTION = None
IND_TO_EDIT = 0

class RootWindow():
    main_window = None
    mainCanvas = None
    dot_win = None

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x600+298+48")
        self.setup_main_window()

    def mainloop(self):
        self.main_window.mainloop()
        self.mainCanvas.mainloop()

    def setup_main_window(self):
        self.mainCanvas = tk.Canvas(self.main_window, bg='lavender')
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
        solve_problem.bind('<Button-1>')
        solve_problem.grid(row=7, column=0)
    

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
        self.dot_win.xentry.insert(0, dot_coord[0])
        
        self.dot_win.yentry.delete(0, tk.END)
        self.dot_win.yentry.insert(0, dot_coord[1])
        
        self.dot_win.set_entry.delete(0, tk.END)
        self.dot_win.set_entry.insert(0, dot_coord[2])
    
    def del_dot(self):
        ind = self.dots_list.curselection()[0]
        self.dots_list.delete(ind)
        self.check_list_box()
    
    def clear_table(self):
        self.dots_list.delete(0, tk.END)
        self.check_list_box()


    
    def check_list_box(self):
        if len(self.dots_list.get(0, tk.END)) == 0: # if listbox is empty we block buttons
            state = 'disabled'
        else:
            state = 'active'
        
        self.edit_dot_btn.configure(state=state)
        self.del_dot_btn.configure(state=state)
        

class AddDotWin(tk.Toplevel):
    vals = None

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.geometry('275x130')

        self.title('Add dot')

        self.xlabel = tk.Label(self, text='x', justify='center')
        self.xlabel.grid(row=0, column=0)

        self.ylabel = tk.Label(self, text='y', justify='center')
        self.ylabel.grid(row=0, column=1)

        # self.setlabel = tk.Label(self, text='Множество', justify='center')
        # self.setlabel.grid(row=0, column=2)

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


        # self.set_entry = tk.Spinbox(self, from_=1, to=2, width=10, justify='center')
        # self.set_entry.grid(row=1, column=2)

        self.add_btn = tk.Button(self, text='Ok')
        self.add_btn.grid(row=2, column=1)
        self.add_btn.bind("<Button-1>", lambda event: conf_dot(window, self))
        # self.add_btn.configure(command=lambda: self.get_entries())

    def get_entries(self) -> tuple:
        return [self.xentry.get(), self.yentry.get(), self.set_var.get()]


def find_in_listbox(listbox:tk.Listbox, record:str) -> bool:
    for i in listbox.get(0, tk.END):
        if i == record:
            return True
    return False



def conf_dot(root:RootWindow, dot_win:AddDotWin):
    items = dot_win.get_entries()

    try:
        items = list(map(float, items[:2])) + [int(items[2])]
    except ValueError:
        messagebox.showerror(title='Ошибка', message='Не все значения имеют вещественный тип. Проверьте ввод')
        return None

    if find_in_listbox(root.dots_list, f"{items[0]} ; {items[1]} ; {items[2]}"):
        messagebox.showerror(title='Ошибка', message='Такая точка уже добавлена.')
    else:

        ind = 0
        if ACTION == ADD:
            ind = 0
        else:
            ind = IND_TO_EDIT
            root.dots_list.delete(ind)

        root.dots_list.insert(ind, f"{items[0]} ; {items[1]} ; {items[2]}")

        dot_win.destroy()
    

    root.check_list_box()


window = RootWindow()

window.mainloop()
