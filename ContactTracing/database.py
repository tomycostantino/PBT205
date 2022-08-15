# Tomas Costantino - A00042881
import sqlite3


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
        self._cursor.execute("CREATE TABLE IF NOT EXISTS close_contacts (name_1 TEXT, name_2 TEXT, position TEXT, date TEXT)")
        self._conn.commit()  # Saves the changes

    def check_if_exists(self, personId: str) -> bool:
        # Check if a person exists in the database
        self._cursor.execute('SELECT * FROM positions WHERE name = ?', (personId,))
        result = self._cursor.fetchall()
        return True if result else False

    def insert_position_data(self, personId: str, position: str, date: str, time: str):
        # Insert new person into database
        self._cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", (personId, position, date, time))
        self._conn.commit()

        # See if the new entry is a close contact with someone in the database
        self._check_for_close_contact(personId, position, date)

    def retrieve_position_data(self, personId: str):
        # Query the database for a person
        self._cursor.execute("SELECT * FROM positions WHERE name = ?", (personId,))
        positions = self._cursor.fetchall()
        return [row for row in positions]

    def _check_for_close_contact(self, personId: str, position: str, date: str):
        # Check if there is a close contact after entering a new position to the database
        self._cursor.execute('SELECT * FROM positions WHERE name != ? AND position = ? AND date = ?', (personId, position, date))
        close_contacts = self._cursor.fetchall()
        close_contacts = [row for row in close_contacts]

        # if there is any close contact, add it to the database
        if close_contacts:
            [self._add_close_contact(personId, contact[0], position, date) for contact in close_contacts]

    def retrieve_close_contact(self, personId: str):
        # Retrieve close contact by person name
        self._cursor.execute('SELECT * FROM close_contacts WHERE name_1 = ? OR name_2 = ?', (personId, personId))
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def retrieve_all_close_contact(self):
        # Retrieve the whole table of close_contacts
        self._cursor.execute('SELECT * FROM close_contacts')
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def add_infected_person(self, personId: str):
        pass

    def _add_close_contact(self, name_1: str, name_2: str, position: str, date: str):
        # Add a close contact to the database
        self._cursor.execute('INSERT INTO close_contacts VALUES (?, ?, ?, ?)', (name_1, name_2, position, date))
        self._conn.commit()

    def close(self):
        # Close connection before delete it
        self._conn.close()
