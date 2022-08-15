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

    def insert_position_data(self, personId: str, position: str, date: str, time: str):
        # Insert new person into database
        self._cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", (personId, position, date, time))
        self._conn.commit()

        self._check_for_close_contact(personId, position, date)

    def retrieve_position_data(self, personId: str):
        # Query the database for a person
        self._cursor.execute("SELECT * FROM positions WHERE name = ?", (personId,))
        positions = self._cursor.fetchall()
        return [row for row in positions]

    def _check_for_close_contact(self, personId: str, position: str, date: str):
        self._cursor.execute('SELECT * FROM positions WHERE name != ? AND position = ? AND date = ?', (personId, position, date))
        close_contacts = self._cursor.fetchall()
        close_contacts = [row for row in close_contacts]
        print(close_contacts)

        if close_contacts:
            [self._add_close_contact(personId, contact[0], position, date) for contact in close_contacts]

    def retrieve_close_contact(self, personId: str):
        self._cursor.execute('SELECT * FROM close_contacts WHERE name_1 = ? OR name_2 = ?', (personId, personId))
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def retrieve_all_close_contact(self):
        self._cursor.execute('SELECT * FROM close_contacts')
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def _add_close_contact(self, name_1: str, name_2: str, position: str, date: str):
        self._cursor.execute('INSERT INTO close_contacts VALUES (?, ?, ?, ?)', (name_1, name_2, position, date))
        self._conn.commit()

    def close(self):
        # Close connection before delete it
        self._conn.close()
