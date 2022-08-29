# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
from interface.styling import *


class GridUI(tk.Frame):
    # Class to visualize the grid
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._canvas = tk.Canvas(self, width=500, height=500)
        self._canvas.pack(side=tk.TOP, expand=True, fill='both')

        self._user_data = []
        self._buttons = []

    def _create_canvas(self, rows, columns, data):
        # Draw the canvas grid with the buttons in it
        self._user_data = data

        # Lists of positions that are close contacts
        to_color = [tuple(map(int, color['position'].split(', '))) for color in data]
        idx = 0
        for i in range(1, rows + 1):
            # Draw rows
            for j in range(1, columns + 1):
                # Draw columns
                if (i, j) in to_color:
                    self._buttons.append(tkmac.Button(self._canvas, text='{}, {}'.format(i, j), bg='red',
                                                      command=lambda c=idx: self._display_info(self._buttons[c].cget("text"))))
                    self._buttons[idx].grid(row=i, column=j)

                    self._canvas.create_window(j * 50, i * 50, window=self._buttons[idx])
                    self._canvas.create_window((i * 50) + 25, (j * 50) + 25, window=self._buttons[idx], anchor='center', width=50, height=50)

                    idx += 1
                else:
                    # Draw grey rectangle if not in color
                    self._canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50, fill='grey')

    def _get_position_index(self, position):
        positions_list = [tuple(map(int, color['position'].split(', '))) for color in self._user_data]
        for p in positions_list:
            if p[0] == position[0] and p[1] == position[1]:
                return positions_list.index(p)

    def draw_grid(self, rows, columns, data, name):
        self.clear_canvas()
        self._canvas.create_text(300, 30, text='You are visualising: ' + name, fill='black')
        self._create_canvas(rows, columns, data)

    def clear_canvas(self):
        self._canvas.delete('all')
        if self._canvas.winfo_children():
            for button in self._canvas.winfo_children():
                button.destroy()
        self._buttons = []

    def _display_info(self, position):
        popup = tk.Toplevel()
        popup.wm_title('Info')
        popup.geometry('200x200')

        p_tuple = tuple(map(int, position.split(', ')))
        index = self._get_position_index(p_tuple)
        data = self._user_data[index]

        infected_label = tk.Label(popup, text='Infected person: {}'.format(data['infected_person']), fg='black',
                                  font=LABEL)
        infected_label.pack(side=tk.TOP, expand=False, anchor='center')

        name_label = tk.Label(popup, text='Close contact: {}'.format(data['contact']), fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=False, anchor='center')

        infected_date_label = tk.Label(popup, text='Date: {}'.format(data['date']), fg='black', font=LABEL)
        infected_date_label.pack(side=tk.TOP, expand=False, anchor='center')

        position_label = tk.Label(popup, text='Position: {}'.format(data['position']), fg='black', font=LABEL)
        position_label.pack(side=tk.TOP, expand=False, anchor='center')

