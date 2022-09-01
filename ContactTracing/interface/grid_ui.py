# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
from grid import Grid
from interface.autocomplete_widget import Autocomplete
from interface.styling import *
from interface.geometry import *


class GridUI(tk.Toplevel):
    # Class to visualize the grid
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(GRID_WINDOW)

        self._grid = Grid()

        # Create frames to split UI
        upper_frame = tk.Frame(self)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self)
        lower_frame.pack(side=tk.TOP, expand=True, fill='both')

        # Title
        label = tk.Label(upper_frame, text='You are in Grid mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        # Grid widgets
        grid_name = tk.Text(upper_frame, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        grid_name.pack(side=tk.TOP)

        # When the button is pressed it will send the data to the tracker and wait for a response
        submit_button = tkmac.Button(upper_frame, text='Submit', command=lambda: self._submit(grid_name))
        submit_button.pack(side=tk.TOP, anchor='center')

        self._canvas = tk.Canvas(lower_frame, width=500, height=500)
        self._canvas.pack(side=tk.TOP, expand=True, fill='both')

        return_button = tkmac.Button(lower_frame, text='Return home', width=130, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center', pady=30)

        self._user_data = []
        self._buttons = []

    def _submit(self, grid_name: tk.Text):
        self._grid.publish_query(grid_name.get('1.0', 'end-1c'))

        data = []
        while not data:
            data = self._grid.retrieve_messages()

        self.draw_grid(10, 10, data, grid_name.get('1.0', 'end-1c'))
        grid_name.delete('1.0', 'end')

    def _create_canvas(self, n_rows, n_columns, data):
        # Draw the canvas grid with the buttons in it
        self._user_data = data

        # Lists of positions that are close contacts
        to_color = [tuple(map(int, color['position'].split(', '))) for color in self._user_data]
        idx = 0
        for i in range(1, n_rows + 1):
            # Draw rows
            for j in range(1, n_columns + 1):
                # Draw columns
                if (i, j) in to_color:
                    self._buttons.append(tkmac.Button(self._canvas, text='{}, {}'.format(i, j), bg='red',
                                                      command=lambda c=idx: self._display_info(
                                                          self._buttons[c].cget("text"))))
                    self._buttons[idx].grid(row=i, column=j)

                    self._canvas.create_window(j * 50, i * 50, window=self._buttons[idx])
                    self._canvas.create_window((i * 50) + 25, (j * 50) + 25, window=self._buttons[idx], anchor='center',
                                               width=50, height=50)

                    idx += 1
                else:
                    # Draw grey rectangle if not in color
                    self._canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='grey')

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

        infected_label = tk.Label(popup, text='Infected person: {}'.format(data['infected']), fg='black',
                                  font=LABEL)
        infected_label.pack(side=tk.TOP, expand=False, anchor='center')

        name_label = tk.Label(popup, text='Close contact: {}'.format(data['contact']), fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=False, anchor='center')

        infected_date_label = tk.Label(popup, text='Date: {}'.format(data['date']), fg='black', font=LABEL)
        infected_date_label.pack(side=tk.TOP, expand=False, anchor='center')

        position_label = tk.Label(popup, text='Position: {}'.format(data['position']), fg='black', font=LABEL)
        position_label.pack(side=tk.TOP, expand=False, anchor='center')

    def _back_to_mainmenu(self):
        '''
        Bring back master window and destroy this one
        '''
        self.master.deiconify()
        self.destroy()

