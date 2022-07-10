import sqlite3


class Database:
    def __init__(self):
        self._db = sqlite3.connect('database.db')
        self._cursor = self._db.cursor()

    def insert_value(self, personId: str, time: str, position: tuple):
        self._cursor.execute("INSERT INTO positions VALUES (?, ?)", (personId, position))
        self._db.commit()
