import tkinter as tk
import tkmacosx as tkmac

from tracker import Tracker


class TrackerUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        upper_frame = tk.Frame(self, width=200, height=75)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self, width=200, height=75)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        label = tk.Label(upper_frame, text='You are in Tracker mode', fg='black', font=("Calibri", 14, "bold"))
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        start_button = tkmac.Button(upper_frame, text='Start tracking', command=self._start)
        start_button.pack(side=tk.TOP, anchor='center', fill='both')

        search_button = tkmac.Button(upper_frame, text='Search database', command=self._search_database)
        search_button.pack(side=tk.TOP, anchor='center', fill='both')

    def _start(self):
        tr = Tracker()
        tr.run()
        # self._tracker = Tracker()
        # self._tracker.run()

    def _search_database(self):
        print('New search')
