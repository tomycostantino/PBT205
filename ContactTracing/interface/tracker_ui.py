# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from tracker import Tracker
from interface.styling import *


class TrackerUI(tk.Frame):
    def __init__(self, tracker, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        search_button = tkmac.Button(upper_frame, text='Add infected person', command=self._add_infected_person)
        search_button.pack(side=tk.TOP, anchor='center')

    def _add_infected_person(self):
        self._popup_window = tk.Toplevel(self)
        self._popup_window.wm_title("Add infected person")
        self._popup_window.geometry("300x150")

        label = tk.Label(self._popup_window, text='Please enter name of the person\n you want to mark as infected:', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._full_name = tk.Text(self._popup_window, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        submit_button = tkmac.Button(self._popup_window, text='Submit',
                                     command=lambda: self._submit(self._full_name.get('1.0', 'end-1c')))
        submit_button.pack(side=tk.TOP, anchor='center')

    def _submit(self, personId: str):

        if len(personId) == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            return

        else:
            if self._tracker.add_infected_person(personId):
                tkinter.messagebox.showinfo("Contact Tracing", "Person successfully added")
                self._full_name.delete('1.0', 'end-1c')
                self._popup_window.destroy()

            else:
                tkinter.messagebox.showinfo("Contact Tracing", "Person is not in the database")
                self._full_name.delete('1.0', 'end-1c')

