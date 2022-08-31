import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox
from add_infected import AddInfected
from interface.styling import *
from interface.geometry import *
from datetime import datetime


class AddInfectedUI(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wm_title("Add infected person")
        self.geometry(ADD_INFECTED_WINDOW)

        self._add_infected = AddInfected()

        label = tk.Label(self, text='Please enter name of the person\n you want to mark as infected:',
                         fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._full_name = tk.Text(self, height=3, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        label = tk.Label(self, text='Insert the infected date dd/mm/yyyy \n'
                                    'Leave in blank for today', fg='black', font=LABEL)
        label.pack(side=tk.TOP, expand=False, anchor='center')

        self._infected_date = tk.Text(self, height=3, width=20, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._infected_date.pack(side=tk.TOP)

        submit_button = tkmac.Button(self, text='Submit',
                                     command=lambda: self._submit_infected_person(self._full_name.get('1.0', 'end-1c')))
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(self, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _submit_infected_person(self, personId: str):
        if len(personId) == 0:
            tkinter.messagebox.showinfo("Contact Tracing", "Please enter a name")
            return

        else:
            if self._infected_date.get('1.0', 'end-1c') == '':
                # Get current time
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                # Split date and time to have them separated
                dt = dt_string.split(' ')
                self._add_infected.publish_query(personId, dt[0])

            tkinter.messagebox.showinfo("Contact Tracing", "Person successfully added")
            self._full_name.delete('1.0', 'end-1c')
            self._infected_date.delete('1.0', 'end-1c')

    def _back_to_mainmenu(self):
        del self._add_infected
        self.master.deiconify()
        self.destroy()
