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
        display_grid = tkmac.Button(upper_frame, text='Display grid', width=150, command=self._display_grid)
        display_grid.pack(side=tk.TOP, anchor='center')

        query_button = tkmac.Button(upper_frame, text="Query", width=150,
                                    command=self._create_query_window)
        query_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _create_add_infected_window(self):
        add_infected_ui = AddInfectedUI(self._tracker, self)
        add_infected_ui.geometry("+%d+%d" % (self._center_popup(ADD_INFECTED_WINDOW)))

    def _display_grid(self):
        self._popup_window = tk.Toplevel(self)
        self._popup_window.wm_title("Display grid")
        self._popup_window.geometry("600x700")
        # Title
        label = tk.Label(self._popup_window, text='You are in Grid mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        # Grid widgets
        self._grid_name = tk.Text(self._popup_window, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._grid_name.pack(side=tk.TOP)

        # When the button is pressed it will send the data to the tracker and wait for a response
        submit_button = tkmac.Button(self._popup_window, text='Submit', command=self._submit_grid)
        submit_button.pack(side=tk.TOP, anchor='center')

        self._grid = GridUI(self._popup_window)
        self._grid.pack(side=tk.TOP, expand=True, fill='both')

    def _submit_grid(self):
        name = self._grid_name.get('1.0', 'end-1c')
        if len(name) == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            self._grid.clear_canvas()
            self._grid_name.delete('1.0', 'end-1c')
            return

        elif not self._tracker.check_if_person_exists('positions', name):
            tkinter.messagebox.showinfo("Contact Tracing", "No registry of such user")
            self._grid_name.delete('1.0', 'end-1c')
            self._grid.clear_canvas()
            return

        else:
            to_color = self._tracker.get_close_contact(self._grid_name.get('1.0', 'end-1c'))
            self._grid.draw_grid(10, 10, to_color, self._grid_name.get('1.0', 'end-1c'))
            self._grid_name.delete('1.0', 'end-1c')

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

