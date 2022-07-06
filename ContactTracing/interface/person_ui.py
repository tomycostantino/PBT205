import tkinter as tk
import tkmacosx as tkmac

from person import Person
from interface.styling import *


class PersonUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        upper_frame = tk.Frame(self, width=250, height=80)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self, width=200, height=20)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        label = tk.Label(upper_frame, text='You are in Person mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        name_label = tk.Label(upper_frame, text='Please enter your name:', fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        self._full_name = tk.Text(upper_frame, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        movement_label = tk.Label(upper_frame, text='Movement speed in seconds:', fg='black', font=LABEL)
        movement_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        self._movement_speed = tk.Text(upper_frame, height=2, width=15, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._movement_speed.pack(side=tk.TOP)

        submit_button = tkmac.Button(upper_frame, text='Submit',
                                     command=lambda: self._submit(self._full_name.get('1.0', 'end-1c'),
                                                                  self._movement_speed.get('1.0', 'end-1c')))
        submit_button.pack(side=tk.TOP, anchor='center')

    def _submit(self, person_id: str, speed: str):
        self._full_name.delete('1.0', 'end-1c')
        self._movement_speed.delete('1.0', 'end-1c')
        person = Person(personId=person_id, movement_speed=speed)
        person.run()
