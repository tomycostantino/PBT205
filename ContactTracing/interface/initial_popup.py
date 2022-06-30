import tkinter as tk
import tkmacosx as tkmac


class InitialPopup(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = ''
        self.create_widgets()

    def create_widgets(self):
        '''
        frame = tk.Frame(self)
        frame.config(width=200, height=110)
        frame.pack_propagate(0)
        frame.pack(side=tk.TOP, expand=True, fill='both')
        '''

        title_label = tk.Label(self, text='Start in Mode:', fg='black', font=("Calibri", 14, "bold"))
        title_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        person_button = tkmac.Button(self, text="Person",
                                     command=lambda: self.on_click('person'))
        person_button.pack(side=tk.TOP, anchor='center', fill='both')

        query_button = tkmac.Button(self, text="Query",
                                    command=lambda: self.on_click('query'))
        query_button.pack(side=tk.TOP, anchor='center', fill='both')

        tracker_button = tkmac.Button(self, text='Tracker',
                                      command=lambda: self.on_click('tracker'))
        tracker_button.pack(side=tk.TOP, anchor='center', fill='both')

    def on_click(self, mode: str):
        if mode == 'person':
            self._mode = 'person'
            print(self._mode)
            return self._mode

        elif mode == 'query':
            self._mode = 'query'
            print(self._mode)
            return self._mode

        else:
            self._mode = 'tracker'
            print(self._mode)
            return self._mode

    def get_mode(self):
        return self._mode
