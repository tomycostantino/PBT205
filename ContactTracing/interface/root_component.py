# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac

from tracker import Tracker
from tkinter.messagebox import askquestion
from interface.person_ui import PersonUI
from interface.tracker_ui import TrackerUI
from interface.geometry import *


class RootComponent(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.eval('tk::PlaceWindow . center')
        self.geometry(MAIN_WINDOW)
        self.resizable(True, True)
        self.title('Tracker')
        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        self.tracker = Tracker()
        self.tracker.run()

        # Create commands frame
        commands_frame = tk.Frame(self)
        commands_frame.pack(side=tk.TOP, expand=True, fill='both')

        # Title
        title_label = tk.Label(commands_frame, text='Run as:', fg='black', font=("Calibri", 14, "bold"))
        title_label.pack(side=tk.TOP, expand=True, anchor='center')

        # Choices
        person_button = tkmac.Button(commands_frame, text="Person",
                                     command=lambda: self._create_window(person_button.cget("text").lower()))
        person_button.pack(side=tk.TOP, anchor='center')

        tracker_button = tkmac.Button(commands_frame, text='Tracker',
                                      command=lambda: self._create_window(tracker_button.cget("text").lower()))
        tracker_button.pack(side=tk.TOP, anchor='center')

        exit_button = tkmac.Button(commands_frame, text='Exit', command=self._on_closing)
        exit_button.pack(side=tk.TOP, anchor='center', pady=10)

    def _create_window(self, mode: str):
        # Change interfaces as users interact with the application
        self.withdraw()

        # create widgets based on the chosen mode
        if mode == 'person':
            ui = PersonUI(self)
            ui.geometry("+%d+%d" % (self._center_popup(PERSON_WINDOW)))
            ui.protocol('WM_DELETE_WINDOW', lambda: self._back_to_start(ui))

        elif mode == 'tracker':
            ui = TrackerUI(self.tracker, self)
            ui.geometry("+%d+%d" % (self._center_popup(TRACKER_WINDOW)))
            ui.protocol('WM_DELETE_WINDOW', lambda: self._back_to_start(ui))

    def _on_closing(self):
        # Pop up a window to ask if the user really wants to exit
        result = askquestion('Quit', 'Do you want to quit?')
        if result == 'yes':
            self.destroy()
            self.quit()

    def _back_to_start(self, ui):
        # Destroy the current window and return to the start window
        ui.destroy()
        self.deiconify()

    def _center_popup(self, size):

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
        return (x_center - (x / 2), y_center - (y / 2))
