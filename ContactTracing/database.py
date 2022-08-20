# Tomas Costantino - A00042881
import sqlite3
from datetime import datetime, date, timedelta


class Database:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.row_factory = sqlite3.Row  # Makes the data retrieved from the database accessible by their column name
        self._cursor = self._conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create tables in database when initialised
        self._cursor.execute("CREATE TABLE IF NOT EXISTS positions (name TEXT, position TEXT, date TEXT, time TEXT)")
        self._conn.commit()  # Saves the changes
        self._cursor.execute("CREATE TABLE IF NOT EXISTS close_contacts (infected_person TEXT, contact TEXT, position TEXT, date TEXT)")
        self._conn.commit()  # Saves the changes
        self._cursor.execute("CREATE TABLE IF NOT EXISTS currently_infected_people (name TEXT, date_infected TEXT, date_recovered TEXT)")
        self._conn.commit()  # Saves the changes

    def check_if_person_exists(self, table: str, personId: str) -> bool:
        # Check if a person exists in the database
        self._cursor.execute('SELECT * FROM ' + table + ' WHERE name = ?', (personId,))
        result = self._cursor.fetchall()
        return True if result else False

    def insert_position_data(self, personId: str, position: str, date: str, time: str):
        # Insert new person into database
        self._cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", (personId, position, date, time))
        self._conn.commit()

        # See if the new entry is a close contact with someone in the database
        self._check_for_close_contact(personId, position, date)

    def _check_for_close_contact(self, personId: str, position: str, date: str):
        # Check if there is a close contact after entering a new position to the database
        if self.check_if_person_exists('currently_infected_people', personId):
            self._cursor.execute('SELECT name FROM positions WHERE name != ? AND position = ? AND date = ?', (personId, position, date))
            contacts = self._cursor.fetchall()
            [self._add_close_contact(personId, contact[0], position, date) for contact in contacts] if contacts else None

        # The person is not infected, so now retrieve the name of currently infected people and check on the system
        else:
            self._cursor.execute('SELECT name FROM currently_infected_people')
            infected_people = self._cursor.fetchall()

            for infected_person in infected_people:
                self._cursor.execute('SELECT name FROM positions WHERE name = ? AND position = ? AND date = ?', (str(infected_person), position, date))
                contacts = self._cursor.fetchall()
                self._add_close_contact(infected_person[0], contacts[0], position, date) if contacts else None

    def _add_close_contact(self, infected_person: str, contact: str, position: str, date: str):
        # Add a close contact to the database
        self._cursor.execute('SELECT * FROM close_contacts WHERE infected_person = ? AND contact = ? AND position = ? AND date = ?',
                             (infected_person, contact, position, date))
        result = self._cursor.fetchall()
        if not result:
            self._cursor.execute('INSERT INTO close_contacts VALUES (?, ?, ?, ?)', (infected_person, contact, position, date))
            self._conn.commit()

    def retrieve_position_data(self, personId: str):
        # Query the database for a person's historical position data
        self._cursor.execute("SELECT * FROM positions WHERE name = ?", (personId,))
        positions = self._cursor.fetchall()
        return [row for row in positions]

    def retrieve_close_contact(self, personId: str):
        # Retrieve close contacts by person name
        self._cursor.execute('SELECT * FROM close_contacts WHERE infected_person = ? OR contact = ?', (personId, personId))
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def retrieve_all_close_contact(self):
        # Retrieve the whole table of close_contacts
        self._cursor.execute('SELECT * FROM close_contacts')
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def add_infected_person(self, personId: str, date_infected: str):
        # Add a person to the currently infected people table
        date_infected = datetime.strptime(date_infected, '%d/%m/%Y')
        date_recovered = date_infected + timedelta(weeks=2)

        date_infected = date_infected.strftime('%d/%m/%Y')
        date_recovered = date_recovered.strftime('%d/%m/%Y')

        self._cursor.execute("INSERT INTO currently_infected_people VALUES (?, ?, ?)", (personId, date_infected, date_recovered))
        self._conn.commit()

    def check_for_recovered_persons(self):
        # Check if a person has recovered
        today = datetime.now()
        today = today.strftime('%d/%m/%Y %H:%M:%S')
        today = today.split(' ')[0]
        self._cursor.execute('SELECT name FROM currently_infected_people WHERE date_recovered = ?', (today,))
        result = self._cursor.fetchall()

        [self._remove_infected_person(str(person[0])) for person in result] if result else None

    def _remove_infected_person(self, personId: str):
        # Remove a person from the currently infected people table
        self._cursor.execute("DELETE FROM currently_infected_people WHERE name = ?", (personId,))
        self._conn.commit()

    def close(self):
        # Close connection before delete it
        self._conn.close()
