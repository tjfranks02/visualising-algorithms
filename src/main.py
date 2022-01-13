from tkinter import *
from tkinter import ttk
import bst as bst

root = Tk()

canvas = Canvas(root, width=500, height=400, background='gray75')
canvas.create_oval(10, 10, 50, 50, fill='red', outline='blue')
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80, smooth="1")

root.mainloop()