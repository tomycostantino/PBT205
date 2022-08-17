# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import numpy as np
from interface.styling import *


class Grid(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._canvas = tk.Canvas(self, width=500, height=500)
        self._canvas.pack(side=tk.TOP, expand=True, fill='both')

    def _create_canvas(self, rows, columns, to_color: list = None):

        for i in range(1, rows + 1):
            for j in range(1, columns + 1):
                if (i, j) in to_color:
                    self._canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='red')
                else:
                    self._canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50, fill='grey')

    def draw_grid(self, rows, columns, to_color):
        self.clear_canvas()
        to_color = [tuple(map(int, color[0].split(', '))) for color in to_color]
        self._create_canvas(rows, columns, to_color)

    def clear_canvas(self):
        self._canvas.delete('all')
