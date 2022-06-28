import tkinter as tk
import tkmacosx as tkmac

from tkinter.messagebox import askquestion
from interface.initial_popup import InitialPopup
from person import Person
from query import Query
from tracker import Tracker


class RootComponent(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Contract Tracing')
        self.geometry('300x300')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._on_closing)
        self._create_widgets()
        #self.bind('<Return>', self.on_enter)
        #self.bind('<Escape>', self.on_closing)

    def _update_ui(self):
        self.after(1000, self._update_ui)

    def _get_mode(self):
        self.wm_withdraw()
        popup = InitialPopup(self)
        self.wait_window(popup)
        mode = popup.get_mode()
        # popup.destroy()
        return mode

    def _create_widgets(self):
        mode = self._get_mode()

        if mode == 'person':
            pass

        elif mode == 'query':
            pass

        elif mode == 'tracker':
            pass

    def _on_closing(self):
        result = askquestion('Quit', 'Do you want to quit?')
        if result == 'yes':
            self.destroy()
            self.quit()
