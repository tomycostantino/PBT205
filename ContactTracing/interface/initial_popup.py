import tkinter as tk
import tkmacosx as tkmac


class InitialPopup(tk.Toplevel):
    def __init__(self, root: tk.Tk):
        tk.Toplevel.__init__(self, root)
        self.title('Contract Tracing')
        self.geometry('300x300')
        self.resizable(False, False)
        self.create_widgets()
        #self.eval('tk::PlaceWindow . center')
        self.title('Start in mode:')
        self._mode = ''

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.config(width=200, height=110)
        frame.pack_propagate(0)
        frame.pack(side=tk.TOP, expand=True, fill='both')

        person_button = tkmac.Button(frame, text="Person",
                                     command=lambda: self._on_click('person'))
        person_button.pack(side=tk.TOP, anchor='center', fill='both')

        query_button = tkmac.Button(frame, text="Testnet normal",
                                    command=lambda: self._on_click('query'))
        query_button.pack(side=tk.TOP, anchor='center', fill='both')

        tracker_button = tkmac.Button(frame, text='Spot futures',
                                      command=lambda: self._on_click('tracker'))
        tracker_button.pack(side=tk.TOP, anchor='center', fill='both')

    def _on_click(self, mode: str):
        if mode == 'person':
            self._mode = 'person'
            self.destroy()

        elif mode == 'query':
            self._mode = 'query'
            self.destroy()

        else:
            self._mode = 'tracker'
            self.destroy()

    def get_mode(self):
        return self._mode
