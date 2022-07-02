import tkinter as tk
import tkmacosx as tkmac

from tkinter.messagebox import askquestion
from interface.query_ui import QueryUI
from interface.person_ui import PersonUI
from interface.tracker_ui import TrackerUI


class RootComponent(tk.Tk):
    def __init__(self):
        super().__init__()
        self.eval('tk::PlaceWindow . center')
        self.geometry('200x100')
        self.resizable(False, False)
        self.title('Contract Tracing')
        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        self._mode = ''

        commands_frame = tk.Frame(self)
        commands_frame.pack(side=tk.TOP, expand=True, fill='both')

        title_label = tk.Label(commands_frame, text='Use it as:', fg='black', font=("Calibri", 14, "bold"))
        title_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        person_button = tkmac.Button(commands_frame, text="Person",
                                     command=lambda: self._on_click('person'))
        person_button.pack(side=tk.TOP, anchor='center', fill='both')

        query_button = tkmac.Button(commands_frame, text="Query",
                                    command=lambda: self._on_click('query'))
        query_button.pack(side=tk.TOP, anchor='center', fill='both')

        tracker_button = tkmac.Button(commands_frame, text='Tracker',
                                      command=lambda: self._on_click('tracker'))
        tracker_button.pack(side=tk.TOP, anchor='center', fill='both')

        exit_button = tkmac.Button(commands_frame, text='Exit', height=10, width=10,
                                   command=self._on_closing)
        exit_button.pack(side=tk.TOP, anchor='center')

    def _update_ui(self):
        self.after(1000, self._update_ui)

    def _create_widgets(self):
        self.withdraw()

        self._top_window = tk.Toplevel(self)
        self._top_window.protocol('WM_DELETE_WINDOW', self._on_closing)

        # create widgets
        if self._mode == 'person':
            ui = PersonUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'query':
            ui = QueryUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'tracker':
            ui = TrackerUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        # create frame
        lower_frame = tk.Frame(self._top_window)
        lower_frame.pack(side=tk.TOP, expand=True, fill='both')

        return_button = tkmac.Button(lower_frame, text='Return', command=self._back_to_start)
        return_button.pack(side=tk.TOP, anchor='center', fill='both')

    def _on_closing(self):
        result = askquestion('Quit', 'Do you want to quit?')
        if result == 'yes':
            self.destroy()
            self.quit()

    def _back_to_start(self):
        self._top_window.withdraw()
        self._top_window.update()
        self.deiconify()

    def _on_click(self, mode: str):
        self._mode = mode
        self._create_widgets()
