# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from interface.grid import Grid
from datetime import datetime
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

        lower_frame = tk.Frame(self, width=200, height=75)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        # Title
        label = tk.Label(upper_frame, text='You are in Tracker mode', fg='black', font=("Calibri", 14, "bold"))
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        # In a future this button should open a window to search the database from the GUI
        add_infected = tkmac.Button(upper_frame, text='Add infected person', command=self._add_infected_person)
        add_infected.pack(side=tk.TOP, anchor='center')

        # Create grid
        display_grid = tkmac.Button(upper_frame, text='Display grid', command=self._display_grid)
        display_grid.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _add_infected_person(self):
        self._popup_window = tk.Toplevel(self)
        self._popup_window.wm_title("Add infected person")
        # self._popup_window.geometry("300x150")

        label = tk.Label(self._popup_window, text='Please enter name of the person\n you want to mark as infected:', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._full_name = tk.Text(self._popup_window, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        label = tk.Label(self._popup_window, text='Insert the infected date dd/mm/yyyy \n'
                                                  'Leave in blank for today', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._infected_date = tk.Text(self._popup_window, height=3, width=20, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._infected_date.pack(side=tk.TOP)

        submit_button = tkmac.Button(self._popup_window, text='Submit',
                                     command=lambda: self._submit_infected_person(self._full_name.get('1.0', 'end-1c')))
        submit_button.pack(side=tk.TOP, anchor='center')

    def _submit_infected_person(self, personId: str):

        if len(personId) == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            return

        else:
            if self._tracker.check_if_person_exists('currently_infected_people', personId):
                tkinter.messagebox.showinfo("Contact Tracing", "Person already infected")

            elif self._tracker.check_if_person_exists('positions', personId):
                if self._infected_date.get('1.0', 'end-1c') == '':
                    # Get current time
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    # Split date and time to have them separated
                    dt = dt_string.split(' ')
                    self._tracker.add_infected_person(personId, dt[0])

                else:
                    self._tracker.add_infected_person(personId, self._infected_date.get('1.0', 'end-1c'))

                tkinter.messagebox.showinfo("Contact Tracing", "Person successfully added")
                self._full_name.delete('1.0', 'end-1c')
                self._infected_date.delete('1.0', 'end-1c')
                self._popup_window.destroy()

            else:
                tkinter.messagebox.showinfo("Contact Tracing", "No registry of such person\n"
                                                               "so it cannot be marked as infected")
                self._full_name.delete('1.0', 'end-1c')

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

        self._grid = Grid(self._popup_window)
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

    def _back_to_mainmenu(self):
        self.master.deiconify()
        self.destroy()
