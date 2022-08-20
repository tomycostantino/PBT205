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

        self._user_data = []

    def _create_canvas(self, rows, columns, data):

        self._user_data = data
        to_color = [tuple(map(int, color['position'].split(', '))) for color in data]

        buttons = []
        button_idx = 0

        for i in range(1, rows + 1):

            for j in range(1, columns + 1):

                if (i, j) in to_color:
                    buttons.append(tkmac.Button(self._canvas, text='{}, {}'.format(i, j), bg='red',
                                          command=lambda: self._display_info((i, j))))
                    buttons[button_idx].grid(row=i, column=j)
                    self._canvas.create_window(j * 50, i * 50, window=buttons[button_idx])
                    self._canvas.create_window((i * 50) + 25, (j * 50) + 25, window=buttons[button_idx], anchor='center', width=50, height=50)

                    button_idx += 1

                else:
                    self._canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50, fill='grey')

    def _get_index_by_position(self, position):
        positions_list = [tuple(map(int, color['position'].split(', '))) for color in self._user_data]
        for p in positions_list:
            if p[0] == position[0] and p[1] == position[1]:
                return positions_list.index(p)

    def draw_grid(self, rows, columns, data):
        self.clear_canvas()
        self._create_canvas(rows, columns, data)

    def clear_canvas(self):
        self._canvas.delete('all')

    def _display_info(self, position):
        self._popup = tk.Toplevel()
        self._popup.wm_title('Info')
        self._popup.geometry('300x150')

        data = self._user_data[self._get_index_by_position(position)]

        infected_label = tk.Label(self._popup, text='Infected person: {}'.format(data['infected_person']), fg='black', font=LABEL)
        infected_label.pack(side=tk.TOP, expand=False, anchor='center')

        name_label = tk.Label(self._popup, text='Close contact: {}'.format(data['contact']), fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=False, anchor='center')

        infected_date_label = tk.Label(self._popup, text='Date: {}'.format(data['date']), fg='black', font=LABEL)
        infected_date_label.pack(side=tk.TOP, expand=False, anchor='center')

        position_label = tk.Label(self._popup, text='Position: {}'.format(data['position']), fg='black', font=LABEL)
        position_label.pack(side=tk.TOP, expand=False, anchor='center')
