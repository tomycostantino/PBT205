# Tomas Costantino - A00042881
import sqlite3
import typing
from datetime import datetime, date, timedelta


class Database:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.row_factory = sqlite3.Row  # Makes the data retrieved from the database accessible by their column name
        self._cursor = self._conn.cursor()
        self._create_tables()

    def _create_tables(self):
        '''
        Create the tables in the database
        :return:
        '''
        self._cursor.execute("CREATE TABLE IF NOT EXISTS positions (name TEXT, contact TEXT, position TEXT, date TEXT, time TEXT)")
        self._conn.commit()  # Saves the changes
        self._cursor.execute("CREATE TABLE IF NOT EXISTS close_contacts (infected_person TEXT, contact TEXT, position TEXT, date TEXT)")
        self._conn.commit()  # Saves the changes
        self._cursor.execute("CREATE TABLE IF NOT EXISTS currently_infected_people (name TEXT, date_infected TEXT, date_recovered TEXT)")
        self._conn.commit()  # Saves the changes

    def check_if_person_exists(self, table: str, personId: str) -> bool:
        '''
        Check if a person exists in the database
        :param table:
        :param personId:
        :return:
        '''
        self._cursor.execute('SELECT * FROM ' + table + ' WHERE name = ?', (personId,))
        result = self._cursor.fetchall()
        return True if result else False

    def retrieve_all_names(self) -> typing.List[dict]:
        '''
        Retrieve all names from the database
        :return:
        '''

        self._cursor.execute('SELECT name FROM positions')
        names = self._cursor.fetchall()
        return [row for row in names]

    def insert_position_data(self, personId: str, contact: str, position: str, date: str, time: str):
        '''
        Insert a new position data into the database
        :param personId:
        :param position:
        :param date:
        :param time:
        :return:
        '''

        self._cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?)", (personId, contact, position, date, time))
        self._conn.commit()

    def check_for_close_contact(self, personId: str, contact: str, position: str, date: str):
        '''
        Check if a person is a close contact with someone in the database
        :param personId:
        :param position:
        :param date:
        :return:
        '''

        if self.check_if_person_exists('currently_infected_people', personId):
            self._cursor.execute('SELECT name FROM positions WHERE name != ? AND contact != ? AND position = ? '
                                 'AND date = ?', (personId, contact, position, date))
            contacts = self._cursor.fetchall()
            if contacts:
                [self._add_close_contact(personId, contact[0], position, date) for contact in contacts]
                return True
            else:
                return False

        # The person is not infected, so now retrieve the name of currently infected people and check on the system
        else:
            self._cursor.execute('SELECT name FROM currently_infected_people')
            infected_people = self._cursor.fetchall()

            for infected_person in infected_people:
                self._cursor.execute('SELECT name FROM positions WHERE name = ? AND position = ? AND date = ?',
                                     (str(infected_person), position, date))
                contacts = self._cursor.fetchall()
                if contacts:
                    self._add_close_contact(infected_person[0], contacts[0], position, date)
                    return True
                else:
                    return False

    def _add_close_contact(self, infected_person: str, contact: str, position: str, date: str):
        '''
        Add a close contact to the database
        :param infected_person:
        :param contact:
        :param position:
        :param date:
        :return:
        '''

        self._cursor.execute('SELECT * FROM close_contacts WHERE infected_person = ? AND contact = ? AND position = ? AND date = ?',
                             (infected_person, contact, position, date))
        result = self._cursor.fetchall()
        if not result:
            self._cursor.execute('INSERT INTO close_contacts VALUES (?, ?, ?, ?)', (infected_person, contact, position, date))
            self._conn.commit()

    def retrieve_position_data(self, personId: str) -> typing.List[dict]:
        '''
        Retrieve the position data of a person
        :param personId:
        :return:
        '''

        self._cursor.execute("SELECT * FROM positions WHERE name = ?", (personId,))
        positions = self._cursor.fetchall()
        return [row for row in positions]

    def retrieve_all_close_contacts(self, personId: str) -> typing.List[dict]:
        '''
        Retrieve all close contacts of a person
        :param personId:
        :return:
        '''

        self._cursor.execute('SELECT * FROM close_contacts WHERE infected_person = ? OR contact = ?', (personId, personId))
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def retrieve_close_contacts_table(self) -> typing.List[dict]:
        '''
        Retrieve the close contacts table
        :return:
        '''

        self._cursor.execute('SELECT * FROM close_contacts')
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def add_infected_person(self, personId: str, date_infected: str):
        '''
        Add an infected person to the database
        :param personId:
        :param date_infected:
        :return:
        '''

        date_infected = datetime.strptime(date_infected, '%d/%m/%Y')
        date_recovered = date_infected + timedelta(weeks=2)

        date_infected = date_infected.strftime('%d/%m/%Y')
        date_recovered = date_recovered.strftime('%d/%m/%Y')

        self._cursor.execute("INSERT INTO currently_infected_people VALUES (?, ?, ?)", (personId, date_infected, date_recovered))
        self._conn.commit()

    def check_for_recovered_persons(self):
        '''
        Check if there are any recovered persons in the database
        :return:
        '''
        today = datetime.now()
        today = today.strftime('%d/%m/%Y %H:%M:%S')
        today = today.split(' ')[0]
        self._cursor.execute('SELECT name FROM currently_infected_people WHERE date_recovered = ?', (today,))
        result = self._cursor.fetchall()

        [self._remove_infected_person(str(person[0])) for person in result] if result else None

    def _remove_infected_person(self, personId: str):
        '''
        Remove an infected person from the database
        :param personId:
        :return:
        '''
        self._cursor.execute("DELETE FROM currently_infected_people WHERE name = ?", (personId,))
        self._conn.commit()

    def retrieve_close_contacts_names(self) -> typing.List[dict]:
        '''
        Retrieve the names of the close contacts
        :return:
        '''
        self._cursor.execute('SELECT infected_person, contact FROM close_contacts')
        close_contacts = self._cursor.fetchall()
        return [row for row in close_contacts]

    def close(self):
        '''
        Close the connection to the database
        :return:
        '''
        self._conn.close()
