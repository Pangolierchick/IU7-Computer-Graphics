import tkinter as tk


class RootWindow:
    main_window = None
    mainCanvas = None

    def __init__(self):
        self.main_window = tk.Tk()
        self.setup_main_window()

    def mainloop(self):
        self.main_window.mainloop()
        self.mainCanvas.mainloop()

    def setup_main_window(self):
        self.mainCanvas = tk.Canvas(self.main_window, bg='lavender')
        
        self.main_window.title('lab 1')
        
        x_label = tk.Label(self.main_window, text='x').grid(row=0, column=0)
        x_entry = tk.Entry(self.main_window).grid(row=1, column=0)

        y_label = tk.Label(self.main_window, text='y').grid(row=2, column=0)
        y_entry = tk.Entry(self.main_window).grid(row=3, column=0)

        set_var = tk.BooleanVar()
        set_var.set(1)

        set_1 = tk.Radiobutton(text="Множество 1", variable=set_var, value=1).grid(row=1, column=1)
        set_2 = tk.Radiobutton(text="Множество 2", variable=set_var, value=2).grid(row=3, column=1)

        btn_place = tk.Button(self.main_window, text='Добавить')
        btn_place.bind('<Button-1>')
        btn_place.grid(row=1, column=2)

        self.mainCanvas.grid(row=4, column=0, sticky='nsew', columnspan=3)

        self.main_window.columnconfigure((0, 1, 2), weight=1)

        self.main_window.rowconfigure(0, weight=0)
        self.main_window.rowconfigure(1, weight=0)
        self.main_window.rowconfigure(2, weight=0)
        self.main_window.rowconfigure(3, weight=0)
        self.main_window.rowconfigure(4, weight=3)


window = RootWindow()

window.mainloop()
