# Tomas Costantino - A00042881
import logging
import typing
import threading
from threading import Thread
from database.database import Database
from message_broker import MessageBroker
from modules.twilio.twilio_messaging import Messaging

logger = logging.getLogger()


class Tracker:
    def __init__(self):

        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'

        self._positionBroker = MessageBroker(endpoint)  # Broker to read position queue
        self._userDataBroker = MessageBroker(endpoint)  # Broker to read user_data_get queue

        self._publisher = MessageBroker(endpoint)  # Broker to publish when required

        self._messaging = Messaging()

        self._running = False

    def _add_log(self, msg: str):
        '''
        Add a log to the log file
        :param msg:
        :return:
        '''
        logger.info('%s', msg)

    '''
    Broker functions
    '''

    def _subscribe(self):
        '''
        Subscribe to the queues
        :return:
        '''

        '''
        Create queues the tracker reads from and subscribe to them
        Use a thread to run the function in parallel so it does not get stuck in the receiving loop
        '''

        self._publisher.exchange_declare('sent_to_tracker', 'topic')
        self._publisher.exchange_declare('sent_from_tracker', 'topic')

        self._positionBroker.queue_declare('position_queue')
        self._positionBroker.queue_bind('sent_to_tracker', 'position_queue')

        self._userDataBroker.queue_declare('user_data_get')
        self._userDataBroker.queue_bind('sent_to_tracker', 'user_data_get')

        Thread(target=self._positionBroker.subscribe, args=('sent_to_tracker', 'position_queue'), daemon=True).start()
        Thread(target=self._userDataBroker.subscribe, args=('sent_to_tracker', 'user_data_get'), daemon=True).start()

    def _read_messages(self):
        '''
        Read messages from the queues
        :return:
        '''

        '''
        Read messages from both queues every 0.1 second
        '''
        threading.Timer(0.1, self._read_messages).start()

        position_message = self._positionBroker.get_messages()
        user_data_message = self._userDataBroker.get_messages()

        # Check if the incoming messages are not empty
        self._handle_position_messages(position_message) if position_message else None
        self._handle_user_data_get_messages(user_data_message) if user_data_message else None

    def _handle_position_messages(self, messages: list):
        '''
        Update database with positions received
        :param messages:
        :return:
        '''

        Thread(target=self._update_database, args=(messages,), daemon=True).start()

    def _handle_user_data_get_messages(self, messages: list):
        '''
        Handle user_data_get messages in queue
        :param messages:
        :return:
        '''

        for message in messages:
            if message['from'] == 'query':
                Thread(target=self._handle_message, args=(message,), daemon=True).start()

            elif message['from'] == 'grid':
                Thread(target=self._handle_message, args=(message,), daemon=True).start()

            elif message['from'] == 'add_infected':
                Thread(target=self._handle_message, args=(message,), daemon=True).start()

    def _handle_message(self, message: dict):
        '''
        Handle messages in queue that can be either names or positions
        :param message:
        :return:
        '''

        if message['type'] == 'names':
            result = self._retrieve_all_names()

            if result:
                response = self._create_names_response(result)
            else:
                response = {'error': 'No names found'}

            self._publish_on_queue(message['reply_on'], response)

        elif message['type'] == 'positions':
            db_result = self._retrieve_all_positions(message['about'])

            if db_result:
                response = self._create_positions_response(db_result)
            else:
                response = {'error': 'No results found'}

            self._publish_on_queue(message['reply_on'], response)

        elif message['type'] == 'close_contacts':
            db_result = self._retrieve_all_close_contacts(message['about'])

            if db_result:
                response = self._create_close_contacts_response(db_result)
            else:
                response = {'error': 'No results found'}

            self._publish_on_queue(message['reply_on'], response)

        elif message['type'] == 'close_contacts_names':
            db_result = self._retrieve_close_contacts_names()

            if db_result:
                response = self._create_close_contacts_names_response(db_result)
            else:
                response = {'error': 'No results found'}

            self._publish_on_queue(message['reply_on'], response)

        elif message['type'] == 'new_infection':
            self._add_infected_person(message['about'], message['date'])

    def _publish_on_queue(self, queue_name: str, message):
        '''
        Publish on a queue
        :param queue_name:
        :param message:
        :return:
        '''

        self._publisher.JSON_publish('sent_from_tracker', queue_name, message)

    def _create_close_contacts_response(self, database_rows: list) -> typing.List[dict]:
        '''
        Create a response for the grid
        :param result:
        :return:
        '''

        close_contacts = []
        for row in database_rows:
            value = {'infected': row[0], 'contact': row[1], 'position': row[2], 'date': row[3]}
            close_contacts.append(value)

        return close_contacts

    def _create_names_response(self, database_rows: list) -> typing.List[str]:
        '''
        Create a response for the names queue
        :param database_rows:
        :return:
        '''

        names = []
        for name in database_rows:
            if name[0] not in names:
                names.append(name[0])

        return names

    def _create_positions_response(self, database_rows: list) -> typing.List[dict]:
        '''
        Create a response for the positions queue
        :param database_rows:
        :return:
        '''

        positions = []

        for row in database_rows:
            positions.append({'personId': row[0], 'position': row[2], 'date': row[3]})

        return positions

    def _create_close_contacts_names_response(self, database_rows: list) -> typing.List[str]:
        '''
        Create a response for the close contacts names queue
        :param database_rows:
        :return:
        '''

        names = []
        for name in database_rows:
            if name[0] not in names:
                names.append(name[0])

            if name[1] not in names:
                names.append(name[1])

        return names

    '''
    Database functions
    '''

    def _update_database(self, messages: list):
        '''
        Update the database with positions received
        :param messages:
        :return:
        '''

        '''
        I create database here and then delete because it can only be used in the thread that it is created in
        '''
        db = Database()
        [db.insert_position_data(message['personId'].lower(), message['contact'], message['position'], message['date'],
                                 message['time']) for message in messages]

        self._check_close_contact(db, messages)

        db.close()
        del db

    def _check_close_contact(self, db: Database, messages: list):
        for message in messages:
            contact = db.check_for_close_contact(message['personId'].lower(), message['contact'], message['position'],
                                                 message['date'])
            self._messaging.send_message(message['contact'].lower(), self._generate_close_contact_message(message))\
                if contact else None

    def _generate_close_contact_message(self, message: dict) -> str:
        '''
        Generate a message for the user
        :param message:
        :return:
        '''

        return f'You have been in close contact with {message["personId"]} at {message["position"]} on {message["date"]}'

    def _retrieve_all_positions(self, personId: str) -> typing.List[dict]:
        '''
        Retrieve the position of a person from the database
        :param personId:
        :return:
        '''

        db = Database()
        db_result = db.retrieve_position_data(personId.lower())
        db.close()
        del db

        return db_result

    def _retrieve_all_names(self) -> typing.List[dict]:
        '''
        Retrieve all the names from the database
        :return:
        '''

        db = Database()
        db_result = db.retrieve_all_names()
        db.close()
        del db

        return db_result

    def _retrieve_all_close_contacts(self, personId: str) -> typing.List[dict]:
        '''
        Get the close contact of a person
        :param personId:
        :return:
        '''

        db = Database()
        db_result = db.retrieve_all_close_contacts(personId.lower())
        db.close()
        del db

        return db_result

    def _retrieve_close_contacts_names(self) -> typing.List[dict]:
        '''
        Retrieve all the names from the database
        :return:
        '''

        db = Database()
        db_result = db.retrieve_close_contacts_names()
        db.close()
        del db

        return db_result


    def check_if_person_exists(self, table: str, personId: str) -> bool:
        '''
        Check if a person exists in the database
        :param table:
        :param personId:
        :return:
        '''

        db = Database()
        db_result = db.check_if_person_exists(table.lower(), personId.lower())
        db.close()
        del db

        return True if db_result else False

    def _add_infected_person(self, personId: str, date: str):
        '''
        Add a person to the infected table
        :param personId:
        :param date:
        :return:
        '''
        db = Database()
        db.add_infected_person(personId.lower(), date)
        db.close()
        del db

    def _get_close_contacts_table(self):
        # Get all history of close contacts and print out the result
        # It will later be used to be displayed in the UI
        db = Database()
        db_result = db.retrieve_close_contacts_table()
        db.close()
        del db

        return [row for row in db_result]

    def _check_for_recovery(self):
        '''
        Check if a person has recovered
        :return:
        '''

        threading.Timer(10, self._check_for_recovery).start()
        db = Database()
        db.check_for_recovered_persons()
        db.close()
        del db

    def is_running(self):
        '''
        Check if the tracker is running so do not allow for another tracker to run at the same time
        :return:
        '''

        return self._running

    # Run the tracker after it is created
    def run(self):
        '''
        Run the tracker
        :return:
        '''
        # The functions will be run in parallel so the UI can keep working
        # Dies when main thread (only non-daemon thread) exits.
        Thread(target=self._subscribe, daemon=True).start()
        Thread(target=self._read_messages, daemon=True).start()
        Thread(target=self._check_for_recovery, daemon=True).start()
        self._running = True
