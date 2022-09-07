import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox
from add_infected import AddInfected
from interface.styling import *
from interface.geometry import *
from datetime import datetime
from threading import Thread
from ttkwidgets.autocomplete import AutocompleteCombobox


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

        label = tk.Label(self, text='Insert the infected date dd/mm/yyyy \n'
                                    'Leave in blank for today', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._infected_date = tk.Text(self, height=3, width=20, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._infected_date.pack(side=tk.TOP)

        submit_button = tkmac.Button(self, text='Submit',
                                     command=self._submit_infected_person)
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(self, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _submit_infected_person(self):
        if self._name_box == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            return

        else:
            if self._infected_date.get('1.0', 'end-1c') == '':
                # Get current time
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                # Split date and time to have them separated
                dt = dt_string.split(' ')
                self._add_infected.publish_query(self._name_box.get(), dt[0])

            tkinter.messagebox.showinfo("Contact Tracing", "Person successfully added")
            self._name_box.delete(0, 'end')
            self._infected_date.delete('1.0', 'end-1c')

    def _back_to_mainmenu(self):
        del self._add_infected
        self.master.deiconify()
        self.destroy()

    def _get_all_names(self):
        names = self._add_infected.get_all_names()
        self._name_box.set_completion_list(names)
