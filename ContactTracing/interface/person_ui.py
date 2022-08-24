# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from person import Person
from interface.styling import *
from interface.geometry import *


class PersonUI(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        '''
        Initialize the window
        :param args:
        :param kwargs:
        '''

        super().__init__(*args, **kwargs)
        self.geometry(PERSON_WINDOW)
        '''
        Main frame for UI
        It is further divided into child frames that live in the main frame
        '''
        main_frame = tk.Frame(self)
        main_frame.pack(side=tk.TOP, expand=True, fill='both')

        '''
        Welcoming message
        '''
        welcome_label = tk.Label(main_frame, text='Welcome!', fg='black', font=HEADER)
        welcome_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        '''
        Check in frame to display location to check in at
        '''
        checkin_frame = tk.Frame(main_frame)
        checkin_frame.pack(side=tk.TOP, expand=True)

        checkin_label = tk.Label(checkin_frame, text='Check in at:', fg='black', font=SUBHEADER)
        checkin_label.pack(side=tk.LEFT, expand=True, anchor='center')

        location_label = tk.Label(checkin_frame, text='6, 8', fg='black', font=SUBHEADER)
        location_label.pack(side=tk.LEFT, expand=True, anchor='center')

        '''
        Person details
        '''
        person_details_frame = tk.Frame(main_frame)
        person_details_frame.pack(side=tk.TOP, expand=True)

        # Name items
        name_label = tk.Label(person_details_frame, text='Full name:', fg='black', font=LABEL, anchor='w')
        name_label.pack(side=tk.TOP, expand=True, fill='both')

        full_name = tk.Text(person_details_frame, height=1, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG, font=TEXTBOX)
        full_name.pack(side=tk.TOP)

        contact_label = tk.Label(person_details_frame, text='Contact number:', fg='black', font=LABEL, anchor='w')
        contact_label.pack(side=tk.TOP, expand=True, fill='both')

        contact_number = tk.Text(person_details_frame, height=1, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG, font=TEXTBOX)
        contact_number.pack(side=tk.TOP)

        '''
        Send data button
        '''
        checkin_button = tkmac.Button(main_frame, text='Check in', width=130,
                                     command=lambda: self._submit_data(full_name, contact_number))
        checkin_button.pack(side=tk.TOP, anchor='center')

        '''
        Return home
        '''
        return_button = tkmac.Button(main_frame, text='Return home', width=130, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center', pady=30)

    def _submit_data(self, full_name: tk.Text, phone_number: tk.Text):

        person_id = full_name.get('1.0', 'end-1c')
        person_id = person_id[:-1] if person_id.endswith(' ') else person_id

        contact_number = phone_number.get('1.0', 'end-1c')

        '''
        Clear text boxes
        '''
        full_name.delete('1.0', 'end-1c')
        phone_number.delete('1.0', 'end-1c')

        # Create a tuple for the grid size
        grid_size = (10, 10)

        # Create a person object and run it
        person = Person(personId=person_id, movement_speed='5', grid_size=grid_size)
        person.run()

        '''
        Popup window
        '''
        tkinter.messagebox.showinfo("Contact Tracing", "Checked in!")

    def _back_to_mainmenu(self):
        '''
        Bring back master window and destroy this one
        '''
        self.master.deiconify()
        self.destroy()



