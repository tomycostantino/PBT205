# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac

from tkinter.messagebox import askquestion
from interface.query_ui import QueryUI
from interface.person_ui import PersonUI
from interface.tracker_ui import TrackerUI


class RootComponent(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.eval('tk::PlaceWindow . center')
        self.geometry('200x100')
        self.resizable(False, False)
        self.title('Contract Tracing')
        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        # Know the mode to use so it can interchange between Person, Query, and Tracker UIs
        self._mode = ''

        # Create commands frame
        commands_frame = tk.Frame(self)
        commands_frame.pack(side=tk.TOP, expand=True, fill='both')

        # Title
        title_label = tk.Label(commands_frame, text='Use it as:', fg='black', font=("Calibri", 14, "bold"))
        title_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        # Choices
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

    def _create_widgets(self):
        # Change interfaces as users interact with the application
        self.withdraw()

        self._top_window = tk.Toplevel(self)
        self._top_window.geometry('250x350')
        self._top_window.protocol('WM_DELETE_WINDOW', self._on_closing)

        # create widgets based on the chosen mode
        if self._mode == 'person':
            ui = PersonUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'query':
            ui = QueryUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        elif self._mode == 'tracker':
            ui = TrackerUI(self._top_window)
            ui.pack(side=tk.TOP, expand=True, fill='both')

        # create frame for return button
        lower_frame = tk.Frame(self._top_window)
        lower_frame.pack(side=tk.TOP, expand=True, fill='both')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_start)
        return_button.pack(side=tk.TOP, anchor='center')

    def _on_closing(self):
        # Pop up a window to ask if the user really wants to exit
        result = askquestion('Quit', 'Do you want to quit?')
        if result == 'yes':
            self.destroy()
            self.quit()

    def _back_to_start(self):
        # Return home button
        self._top_window.withdraw()
        self._top_window.update()
        self.deiconify()

    def _on_click(self, mode: str):
        # Change modes and create widgets
        self._mode = mode
        self._create_widgets()
