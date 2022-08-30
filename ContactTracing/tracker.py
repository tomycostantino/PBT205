# Tomas Costantino - A00042881
import threading
from database import Database
from threading import Thread
from message_broker import MessageBroker


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'

        self._positionBroker = MessageBroker(endpoint)  # Broker to read position queue
        self._userDataBroker = MessageBroker(endpoint)  # Broker to read user_data_get queue

        self._publisher = MessageBroker(endpoint)       # Broker to publish when required

        self._running = False

    def _subscribe(self):
        # Subscribe to the channels
        # Use a thread to run the function in parallel so it does not get stuck in the receiving loop
        # I created two brokers because they are subscribed to different channels
        self._positionBroker.exchange_declare('sent_to_tracker', 'topic')
        self._positionBroker.exchange_declare('sent_from_tracker', 'topic')

        self._positionBroker.queue_declare('position_queue')
        self._positionBroker.queue_bind('sent_to_tracker', 'position_queue')

        self._userDataBroker.queue_declare('user_data_get')
        self._userDataBroker.queue_bind('sent_to_tracker', 'user_data_get')

        Thread(target=self._positionBroker.subscribe, args=('sent_to_tracker', 'position_queue'), daemon=True).start()
        Thread(target=self._userDataBroker.subscribe, args=('sent_to_tracker', 'user_data_get'), daemon=True).start()

    def _read_messages(self):
        # Read messages from both queues every second
        threading.Timer(1, self._read_messages).start()

        position_message = self._positionBroker.get_messages()
        user_data_message = self._userDataBroker.get_messages()

        # Check if the incoming messages are not empty
        self._handle_position_messages(position_message) if position_message else None
        self._handle_user_data_get_messages(user_data_message) if user_data_message else None

    def _handle_position_messages(self, messages):
        # Update the database with positions received
        self._update_database(messages)

    def _handle_user_data_get_messages(self, messages):
        for message in messages:
            if message['from'] == 'query':
                Thread(target=self._handle_query, args=(message,), daemon=True).start()

            elif message['from'] == 'grid':
                if message['type'] == 'names':
                    response = self._retrieve_all_names()
                    self._publish_on_queue(message['reply_on'], response)

                elif message['type'] == 'positions':
                    response = self._retrieve_position(message['about'])
                    self._publish_on_queue(message['reply_on'], response)

            elif message['from'] == 'add_infected':
                if message['type'] == 'names':
                    response = self._retrieve_all_names()
                    self._publish_on_queue(message['reply_on'], response)

                elif message['type'] == 'add_infected':
                    self.add_infected_person(message['about'], message['date'])

    def _publish_on_queue(self, queue_name, message):
        # Publish a message on a queue
        self._publisher.JSON_publish('sent_from_tracker', queue_name, message)

    def _update_database(self, messages):
        # When a person sends location, update the database
        # I create database here and then delete because it can only be used
        # in the thread that it is created in
        print(messages)
        db = Database()
        [db.insert_position_data(message['personId'].lower(), message['position'], message['date'], message['time']) for message in messages]
        db.close()
        del db

    def _handle_query(self, message):

        if message['type'] == 'names':
            response = self._retrieve_all_names()
            self._publish_on_queue(message['reply_on'], response)

        elif message['type'] == 'positions':
            db_result = self._retrieve_position(message['about'])
            response = ''
            if db_result:
                response = self._create_query_response(db_result)
            else:
                response = {'error': 'No results found'}
            self._publish_on_queue(message['reply_on'], response)

    def _retrieve_position(self, personId: str):
        # Publish what is retrieved from database
        db = Database()
        db_result = db.retrieve_position_data(personId.lower())
        db.close()
        del db

        return db_result

    def _retrieve_all_names(self):
        # Get all names from the database
        db = Database()
        db_result = db.retrieve_all_names()
        db.close()
        del db

        return [row for row in db_result]

    def _create_query_response(self, database_rows):
        # Create a big dictionary of dictionaries to send over the broker
        results = dict()
        idx = 1
        for row in database_rows:
            results[idx] = {'personId': row[0], 'position': row[1], 'date': row[2], 'time': row[3]}
            idx += 1
        return results

    def check_if_person_exists(self, table: str, personId: str) -> bool:
        # Check if a person exists in the database
        db = Database()
        db_result = db.check_if_person_exists(table.lower(), personId.lower())
        db.close()
        del db

        return True if db_result else False

    def add_infected_person(self, personId: str, date: str):
        # This function will make an attempt to add a person to the infected list
        db = Database()
        db.add_infected_person(personId.lower(), date)
        db.close()
        del db

    def get_close_contact(self, personId: str):
        # Get the close contact of a person and print out the result
        # It will later be used to be displayed in the UI
        db = Database()
        db_result = db.retrieve_close_contact(personId.lower())
        db.close()
        del db

        return [row for row in db_result]

    def get_all_close_contacts(self):
        # Get all history of close contacts and print out the result
        # It will later be used to be displayed in the UI
        db = Database()
        db_result = db.retrieve_all_close_contact()
        db.close()
        del db

        return [row for row in db_result]

    def _check_for_recovery(self):
        threading.Timer(10, self._check_for_recovery).start()
        db = Database()
        db.check_for_recovered_persons()
        db.close()
        del db

    def is_running(self):
        # Don't allow for another tracker to run at the same time
        return self._running

    # Run the tracker after it is created
    def run(self):
        # The functions will be run in parallel so the UI can keep working
        # Dies when main thread (only non-daemon thread) exits.
        Thread(target=self._subscribe, daemon=True).start()
        Thread(target=self._read_messages, daemon=True).start()
        Thread(target=self._check_for_recovery, daemon=True).start()
        self._running = True
