#!/usr/bin/python3
# canvas.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
from tkinter import ttk

root = Tk()

canvas = Canvas(root)
canvas.pack()
canvas.config(width=600, height=600)


#rect = canvas.create_rectangle(130, 100, 480, 360)
rect = canvas.create_rectangle(0, 0, 100, 100)
canvas.itemconfigure(rect, fill='grey')

for i in range(0, 10):
    for j in range(0, 10):
        rect = canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50)
        canvas.itemconfigure(rect, fill='grey')


root.mainloop()
