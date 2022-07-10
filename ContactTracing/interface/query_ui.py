# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from query import Query
from interface.styling import *


class QueryUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create frames to split UI
        upper_frame = tk.Frame(self, width=200, height=75)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self, width=200, height=75)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        # Title
        label = tk.Label(upper_frame, text='You are in Query mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        # Person widgets
        name_label = tk.Label(upper_frame, text='Please enter name of the \n'
                                                'person you want to query:', fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        self._full_name = tk.Text(upper_frame, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        # When the button is pressed it will send the data to the tracker and wait for a response
        submit_button = tkmac.Button(upper_frame, text='Submit', command=self._submit)
        submit_button.pack(side=tk.TOP, anchor='center')

    def _submit(self):
        tkinter.messagebox.showinfo("Contact Tracing", "Query successfully created")
        query = Query(self._full_name.get('1.0', 'end-1c'))
        query.publish_query()
        self._full_name.delete('1.0', 'end-1c')
