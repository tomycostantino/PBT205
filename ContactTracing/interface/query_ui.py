# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox
from threading import Thread
from query import Query
from interface.scrollable_frame import ScrollableFrame
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
        label = tk.Label(upper_frame, text='Database search mode', fg='black', font=HEADER)
        label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        # Person widgets
        name_label = tk.Label(upper_frame, text='Please enter name of the \n'
                                                'person you want to query:', fg='black', font=SUBHEADER)
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
        submit_button = tkmac.Button(lower_frame, text='Get data', width=150, command=self._submit)
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.BOTTOM, anchor='center', pady=10)

    def _submit(self):
        tkinter.messagebox.showinfo("Contact Tracing", "Query successfully created")
        self._query.publish_query(self._name_box.get().lower())
        self._name_box.delete(0, 'end')
        Thread(target=self._receive_data, daemon=True).start()

    def _back_to_mainmenu(self):
        del self._query
        self.master.deiconify()
        self.destroy()

    def _get_all_names(self):
        names = self._query.get_all_names()
        self._name_box.set_completion_list(names)

    def _receive_data(self):
        while True:
            data = self._query.retrieve_messages()
            if data:
                print(data)
                self._display_data(data)
                break

    def _display_data(self, data: list):
        popup = tk.Toplevel()
        popup.wm_title('Positions')
        popup.geometry(QUERY_SPREADSHEET)

        upper_frame = tk.Frame(popup)
        upper_frame.pack(side=tk.TOP, anchor='w')

        tk.Label(upper_frame, text='Name', fg='black', font=LABEL, borderwidth=1, border=1).grid(row=0, column=0)
        tk.Label(upper_frame, text='Position', fg='black', font=LABEL, borderwidth=1, border=1).grid(row=0, column=1)
        tk.Label(upper_frame, text='Date', fg='black', font=LABEL, borderwidth=1, border=1).grid(row=0, column=2)

        lower_frame = ScrollableFrame(popup, width=230)
        lower_frame.pack(side=tk.TOP, expand=True)

        row = 1

        for datapoint in data:
            tk.Label(lower_frame.sub_frame, text=datapoint['personId'], fg='black', font=SUBHEADER).grid(row=row, column=0)
            tk.Label(lower_frame.sub_frame, text=datapoint['position'], fg='black', font=SUBHEADER).grid(row=row, column=1)
            tk.Label(lower_frame.sub_frame, text=datapoint['date'], fg='black', font=SUBHEADER).grid(row=row, column=2)
            row += 1



