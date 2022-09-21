# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from interface.query_ui import QueryUI
from interface.grid_ui import GridUI
from interface.add_infected_ui import AddInfectedUI
from interface.styling import *
from interface.geometry import *


class TrackerUI(tk.Toplevel):
    def __init__(self, tracker, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(TRACKER_WINDOW)

        self._tracker = tracker

        # Create frames to split UI
        upper_frame = tk.Frame(self)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self)
        lower_frame.pack(side=tk.TOP, expand=True, fill='both')

        # Title
        label = tk.Label(upper_frame, text='Actions', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        add_infected = tkmac.Button(upper_frame, text='Add infected person', width=150,
                                    command=self._create_add_infected_window)
        add_infected.pack(side=tk.TOP, anchor='center')

        # Create grid
        display_grid = tkmac.Button(upper_frame, text='Display grid', width=150, command=self._create_grid_window)
        display_grid.pack(side=tk.TOP, anchor='center')

        query_button = tkmac.Button(upper_frame, text="Search Database", width=150,
                                    command=self._create_query_window)
        query_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center', pady=10)

    def _create_add_infected_window(self):
        add_infected_ui = AddInfectedUI(self)
        add_infected_ui.geometry("+%d+%d" % (self._center_popup(ADD_INFECTED_WINDOW)))

    def _create_grid_window(self):
        ui = GridUI(self)
        ui.geometry("+%d+%d" % (self._center_popup(GRID_WINDOW)))

    def _create_query_window(self):
        ui = QueryUI(self)
        ui.geometry("+%d+%d" % (self._center_popup(QUERY_WINDOW)))

    def _center_popup(self, size: str) -> tuple:

        '''
        # Center the popup window on the screen
        :param size:
        :return:
        '''

        '''
        Calculate the center of the screen
        '''
        x_center = self.winfo_screenwidth() / 2
        y_center = self.winfo_screenheight() / 2

        '''
        Split the values as the size param comes in as a string in format: 180x100
        '''
        size_str = size.split('x')
        x = int(size_str[0])
        y = int(size_str[1])

        '''
        Return the value to begin the popup window so the center is aligned with the center of the screen
        '''
        return x_center - (x / 2), y_center - (y / 2)

    def _back_to_mainmenu(self):
        self.master.deiconify()
        self.destroy()

