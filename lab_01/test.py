from tkinter import *

master = Tk()

Label(master, text="This is a test").grid(row=0, column=0)

mytext1 = Text(master, width=30,height=5)
mytext1.grid(row=1, column=0, sticky="nsew")

mytext2 = Text(master, width=30,height=5)
mytext2.grid(row=2, column=0, sticky="nsew")

master.columnconfigure(0, weight=1)
master.rowconfigure(0, weight=0) # not needed, this is the default behavior
master.rowconfigure(1, weight=1)
master.rowconfigure(2, weight=1)

master.mainloop()
