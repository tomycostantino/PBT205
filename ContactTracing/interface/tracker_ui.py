import tkinter as tk
import tkmacosx as tkmac


class TrackerUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = tk.Label(self, text='Tracker', fg='black', font=("Calibri", 14, "bold"))
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

