import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox
from add_infected import AddInfected
from interface.styling import *
from interface.geometry import *
from datetime import datetime
from threading import Thread
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkcalendar import Calendar


class AddInfectedUI(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wm_title("Add infected person")
        self.geometry(ADD_INFECTED_WINDOW)

        self._add_infected = AddInfected()

        Thread(target=self._get_all_names, daemon=True).start()

        label = tk.Label(self, text='Please enter name of the person\n you want to mark as infected:',
                         fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._name_box = AutocompleteCombobox(
            self,
            width=30,
            foreground=TEXTBOX_FG,
            justify=tk.CENTER,
            background=TEXTBOX_BG,
            font=TEXTBOX,
        )
        self._name_box.pack(side=tk.TOP)

        label = tk.Label(self, text='Infected date:', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        # creating a calendar object
        self._calendar = Calendar(self, selectmode="day", font=CALENDAR, foreground=TEXTBOX_FG, showweeknumbers=False,
                                  maxdate=datetime.today(), date_pattern="dd/mm/yyyy")
        # display on main window
        self._calendar.pack(side=tk.TOP, pady=20)

        submit_button = tkmac.Button(self, text='Mark as infected',
                                     command=self._submit_infected_person)
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(self, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center', pady=15)

    def _submit_infected_person(self):
        if self._name_box == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            return

        else:
            self._add_infected.publish_query(self._name_box.get(), self._calendar.get_date())

            tkinter.messagebox.showinfo("Contact Tracing", "Person successfully added")
            self._name_box.delete(0, 'end')

    def _back_to_mainmenu(self):
        del self._add_infected
        self.master.deiconify()
        self.destroy()

    def _get_all_names(self):
        names = self._add_infected.get_all_names()
        self._name_box.set_completion_list(names)
