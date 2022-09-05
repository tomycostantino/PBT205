import sqlite3
import typing
from datetime import datetime


class SmsDatabase:
    def __init__(self):
        self._conn = sqlite3.connect('sms_database.db')
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._create_tables()

    def _create_tables(self):
        '''
        Create tables in database when initialised
        :return:
        '''

        self._cursor.execute("CREATE TABLE IF NOT EXISTS sms_sent (phone_number TEXT, message TEXT, date TEXT)")
        self._conn.commit()

    def insert_sms_data(self, phone_number: str, message: str):
        '''
        Insert new sms into database
        :param phone_number:
        :param message:
        :return:
        '''

        today = datetime.now()
        today = today.strftime('%d/%m/%Y %H:%M:%S')
        today = today.split(' ')[0]
        self._cursor.execute("INSERT INTO sms_sent VALUES (?, ?, ?)", (phone_number, message, today))
        self._conn.commit()
