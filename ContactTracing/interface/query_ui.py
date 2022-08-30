# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from query import Query
from interface.styling import *
from interface.geometry import *


class QueryUI(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(QUERY_WINDOW)

        self._query = Query()

        # Create frames to split UI
        upper_frame = tk.Frame(self)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self)
        lower_frame.pack(side=tk.TOP, expand=True, fill='both')

        # Title
        label = tk.Label(upper_frame, text='You are in Query mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        # Person widgets
        name_label = tk.Label(upper_frame, text='Please enter name of the \n'
                                                'person you want to query:', fg='black', font=LABEL)
        name_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        full_name = tk.Text(upper_frame, height=1, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        full_name.pack(side=tk.TOP)

        # When the button is pressed it will send the data to the tracker and wait for a response
        submit_button = tkmac.Button(upper_frame, text='Submit', command=lambda: self._submit(full_name))
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _submit(self, textbox: tk.Text):
        tkinter.messagebox.showinfo("Contact Tracing", "Query successfully created")
        self._query.publish_query(textbox.get('1.0', 'end-1c'))
        textbox.delete('1.0', 'end-1c')

    def _back_to_mainmenu(self):
        del self._query
        self.master.deiconify()
        self.destroy()
