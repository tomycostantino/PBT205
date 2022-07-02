import tkinter as tk
import tkmacosx as tkmac

from person import Person


class PersonUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        upper_frame = tk.Frame(self, width=200, height=75)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self, width=200, height=75)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        label = tk.Label(upper_frame, text='You are in Person mode', fg='black', font=("Calibri", 14, "bold"))
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        name_label = tk.Label(upper_frame, text='Please enter your name:', fg='black', font=("Calibri", 14, "bold"))
        name_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        full_name = tk.Text(upper_frame, height=4, width=40)
        full_name.pack(side=tk.TOP)

        submit_button = tkmac.Button(upper_frame, text='Submit', command=self._submit)
        submit_button.pack(side=tk.TOP, anchor='center', fill='both')

    def _submit(self):
        print('Person created')
