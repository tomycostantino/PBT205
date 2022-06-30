import tkinter as tk
import tkmacosx as tkmac

from tkinter.messagebox import askquestion
from interface.query_ui import QueryUI
from interface.person_ui import PersonUI
from interface.tracker_ui import TrackerUI
from person import Person
from query import Query
from tracker import Tracker


class RootComponent(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Contract Tracing')
        self.geometry('200x100')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        self._mode = ''

        startup_frame = tk.Frame(self, width=200, height=100)
        startup_frame.pack(side=tk.TOP, expand=True, fill='both')

        title_label = tk.Label(startup_frame, text='Start in Mode:', fg='black', font=("Calibri", 14, "bold"))
        title_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        person_button = tkmac.Button(startup_frame, text="Person",
                                     command=lambda: self.on_click('person'))
        person_button.pack(side=tk.TOP, anchor='center', fill='both')

        query_button = tkmac.Button(startup_frame, text="Query",
                                    command=lambda: self.on_click('query'))
        query_button.pack(side=tk.TOP, anchor='center', fill='both')

        tracker_button = tkmac.Button(startup_frame, text='Tracker',
                                      command=lambda: self.on_click('tracker'))
        tracker_button.pack(side=tk.TOP, anchor='center', fill='both')

    def _update_ui(self):
        self.after(1000, self._update_ui)

    def _create_widgets(self):
        self._top_window = tk.Toplevel(self)
        self._top_window.protocol('WM_DELETE_WINDOW', self._on_closing)
        self.withdraw()

        # create frame
        frame = tk.Frame(self._top_window, width=500, height=300)
        frame.pack(side=tk.TOP, expand=True, fill='both')

        if self._mode == 'person':
            ui = PersonUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'query':
            ui = QueryUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'tracker':
            ui = TrackerUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

    def _on_closing(self):
        result = askquestion('Quit', 'Do you want to quit?')
        if result == 'yes':
            self.destroy()
            self.quit()

    def _back_to_start(self):
        self._top_window.destroy()
        self._top_window.quit()
        self.deiconify()

    def on_click(self, mode: str):
        self._mode = mode
        self._create_widgets()
