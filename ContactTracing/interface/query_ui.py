# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox
from threading import Thread
from query import Query
from interface.styling import *
from interface.geometry import *
from ttkwidgets.autocomplete import AutocompleteCombobox


class QueryUI(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(QUERY_WINDOW)

        self._query = Query()

        Thread(target=self._get_all_names, daemon=True).start()

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

        self._name_box = AutocompleteCombobox(
            upper_frame,
            width=30,
            foreground=TEXTBOX_FG,
            justify=tk.CENTER,
            background=TEXTBOX_BG,
            font=TEXTBOX,
        )
        self._name_box.pack(side=tk.TOP)

        # When the button is pressed it will send the data to the tracker and wait for a response
        submit_button = tkmac.Button(lower_frame, text='Submit', command=self._submit)
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _submit(self):
        tkinter.messagebox.showinfo("Contact Tracing", "Query successfully created")
        Thread(target=self._query.publish_query, args=(self._name_box.get().lower())).start()
        self._name_box.delete(0, 'end')

    def _back_to_mainmenu(self):
        del self._query
        self.master.deiconify()
        self.destroy()

    def _get_all_names(self):
        names = self._query.get_all_names()
        self._name_box.set_completion_list(names)
