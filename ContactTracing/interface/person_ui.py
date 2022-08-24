# Tomas Costantino - A00042881
import tkinter as tk
import tkmacosx as tkmac
import tkinter.messagebox

from person import Person
from interface.styling import *


class PersonUI(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create frames to split UI
        upper_frame = tk.Frame(self, width=250, height=120)
        upper_frame.pack(side=tk.TOP, expand=True, fill='both')

        lower_frame = tk.Frame(self, width=200, height=20)
        lower_frame.pack(side=tk.BOTTOM, expand=True, fill='both')

        # Title
        welcome_label = tk.Label(upper_frame, text='Welcome', fg='black', font=HEADER)
        welcome_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        '''
        Check in frame to display location to check in at
        '''
        checkin_frame = tk.Frame(upper_frame)
        checkin_frame.pack(side=tk.TOP, expand=True)

        checkin_label = tk.Label(checkin_frame, text='Check in at:', fg='black', font=SUBHEADER)
        checkin_label.pack(side=tk.LEFT, expand=False, anchor='center')

        location_label = tk.Label(checkin_frame, text='6, 8', fg='black', font=SUBHEADER)
        location_label.pack(side=tk.LEFT, expand=False, anchor='center')

        # Grid items
        grid_size = tk.Label(upper_frame, text='Grid size:', fg='black', font=LABEL)
        grid_size.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        self._x = tk.Text(upper_frame, height=2, width=5, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._x.pack(side=tk.TOP)
        self._x.insert('1.0', '10')
        self._x.config(state=tk.DISABLED)

        self._y = tk.Text(upper_frame, height=2, width=5, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._y.pack(side=tk.TOP)
        self._y.insert('1.0', '10')
        self._y.config(state=tk.DISABLED)

        '''
        Person details frame
        '''
        person_details_frame = tk.Frame(upper_frame)
        person_details_frame.pack(side=tk.TOP, expand=True)

        # Name items
        name_label = tk.Label(person_details_frame, text='Full name:', fg='black', font=LABEL, anchor='w')
        name_label.pack(side=tk.TOP, expand=True, fill='both')

        self._full_name = tk.Text(person_details_frame, height=1, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._full_name.pack(side=tk.TOP)

        contact_label = tk.Label(person_details_frame, text='Contact number:', fg='black', font=LABEL, anchor='w')
        contact_label.pack(side=tk.TOP, expand=True, fill='both')

        self._contact_number = tk.Text(person_details_frame, height=1, width=30, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._contact_number.pack(side=tk.TOP)

        # Movement speed items
        movement_label = tk.Label(person_details_frame, text='Movement speed in seconds:', fg='black', font=LABEL)
        movement_label.pack(side=tk.TOP, expand=True, anchor='center', fill='both')

        self._movement_speed = tk.Text(person_details_frame, height=2, width=15, bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self._movement_speed.pack(side=tk.TOP)

        # When the button is pressed it will try to start sending the data to the tracker
        submit_button = tkmac.Button(upper_frame, text='Check in',
                                     command=lambda: self._submit(self._full_name.get('1.0', 'end-1c'),
                                                                  self._movement_speed.get('1.0', 'end-1c')))
        submit_button.pack(side=tk.TOP, anchor='center')

        return_button = tkmac.Button(lower_frame, text='Return home', width=150, command=self._back_to_mainmenu)
        return_button.pack(side=tk.TOP, anchor='center')

    def _submit(self, person_id: str, speed: str):
        # Check for valid entries

        # See iuf name not empty or shorter tgan 3 characters
        if len(self._full_name.get('1.0', 'end-1c')) < 3:
            tkinter.messagebox.showerror("Contact Tracing",  "Insert a name")
            return

        # See if speed is a number
        elif not self._movement_speed.get('1.0', 'end-1c').isnumeric() or \
                len(self._movement_speed.get('1.0', 'end-1c')) == 0:
            self._movement_speed.delete('1.0', 'end-1c')
            tkinter.messagebox.showerror("Contact Tracing",  "Insert a valid movement speed")
            return

        # See if grid size is a number
        elif not self._x.get('1.0', 'end-1c').isnumeric() or \
                len(self._x.get('1.0', 'end-1c')) == 0 or \
                not self._y.get('1.0', 'end-1c').isnumeric() or \
                len(self._y.get('1.0', 'end-1c')) == 0:

            self._x.delete('1.0', 'end-1c')
            self._y.delete('1.0', 'end-1c')
            tkinter.messagebox.showerror("Contact Tracing", "Insert valid grid size")
            return

        # Check grid size range
        if int(self._x.get('1.0', 'end-1c')) < 10 or int(self._x.get('1.0', 'end-1c')) > 1000 or \
                int(self._y.get('1.0', 'end-1c')) < 10 or int(self._y.get('1.0', 'end-1c')) > 1000:
            tkinter.messagebox.showerror("Contact Tracing", "Grid size has to be between 10x10 and 1000x1000")
            return

        # Clear text boxes
        self._full_name.delete('1.0', 'end-1c')
        self._movement_speed.delete('1.0', 'end-1c')

        # Create a tuple for the grid size
        grid_size = (int(self._x.get('1.0', 'end-1c')), int(self._y.get('1.0', 'end-1c')))

        # Create a person object and run it
        person = Person(personId=person_id, movement_speed=speed, grid_size=grid_size)
        person.run()

        # Display popup window
        tkinter.messagebox.showinfo("Contact Tracing", "Person successfully created")

    def _back_to_mainmenu(self):
        self.master.deiconify()
        self.destroy()



