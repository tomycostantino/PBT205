# Tomas Costantino - A00042881
import sqlite3


class Database:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.row_factory = sqlite3.Row  # Makes the data retrieved from the database accessible by their column name
        self._cursor = self._conn.cursor()
        self._create_tables()

    # Create tables in database when initialised
    def _create_tables(self):
        self._cursor.execute("CREATE TABLE IF NOT EXISTS positions (name TEXT, position TEXT, date TEXT, time TEXT)")
        self._conn.commit()  # Saves the changes

    # Insert new person into database
    def insert_value(self, personId: str, position: str, date: str, time: str):
        self._cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", (personId, position, date, time))
        self._conn.commit()

    # Query the database for a person
    def get_query(self, personId: str):
        self._cursor.execute("SELECT * FROM positions WHERE name = ?", (personId,))
        positions = self._cursor.fetchall()

        positions_list = [row for row in positions]
        return positions_list

    # Close connection before delete it
    def close(self):
        self._conn.close()
