# Tomas Costantino - A00042881
import threading
from database import Database
from threading import Thread
from message_broker import MessageBroker


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._positionBroker = MessageBroker(endpoint)  # Broker to read position
        self._queryBroker = MessageBroker(endpoint)     # Broker to read query
        self._queryPublisher = MessageBroker(endpoint)  # Broker to publish query

        self._running = False

    def _subscribe(self):
        # Subscribe to the channels
        # Use a thread to run the function in parallel so it does not get stuck in the receiving loop
        # I created two brokers because they are subscribed to different channels
        Thread(target=self._positionBroker.subscribe, args=('send_to_tracker', 'position'), daemon=True).start()
        Thread(target=self._queryBroker.subscribe, args=('send_to_tracker', 'query'), daemon=True).start()

    def _read_messages(self):
        # Read messages from both queues every second
        threading.Timer(1, self._read_messages).start()
        position_message = self._positionBroker.get_messages()
        query_message = self._queryBroker.get_messages()

        # Check if the incoming messages are not empty
        if position_message:
            self._update_database(position_message)

        elif query_message:
            self._respond_query(query_message)

    def _update_database(self, messages):
        # When a person sends location, update the database
        # I create database here and then delete because it can only be used
        # in the thread that it is created in
        print(messages)
        db = Database()
        [db.insert_position_data(message['personId'].lower(), message['position'], message['date'], message['time']) for message in messages]
        db.close()
        del db

    def _retrieve_position(self, personId: str):
        # Publish what is retrieved from database
        db = Database()
        db_result = db.retrieve_position_data(personId)
        db.close()
        del db
        return db_result

    def _create_query_response(self, database_rows):
        # Create a big dictionary of dictionaries to send over the broker
        results = dict()
        for idx, row in database_rows:
            results[idx] = {'personId': row[0], 'position': row[1], 'date': row[2], 'time': row[3]}

        return results

    def _respond_query(self, query):
        print(query)
        personId = str(list(query.items())[0][1])
        db_result = self._retrieve_position(personId)

        # See if what retrieved is empty
        # If we know the person we give all info
        if db_result:
            results = self._create_query_response(db_result)
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query_response', results)

        # If person not found, send a message saying so
        else:
            errorMessage = {'error': 'No results found'}
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query_response', errorMessage)

    def check_if_person_exists(self, table: str, personId: str) -> bool:
        # Check if a person exists in the database
        db = Database()
        db_result = db.check_if_person_exists(table, personId)
        db.close()
        del db

        return True if db_result else False

    def add_infected_person(self, personId: str, date: str):
        # This function will make an attempt to add a person to the infected list
        db = Database()
        db.add_infected_person(personId, date)
        db.close()
        del db

    def get_close_contact(self, personId: str):
        # Get the close contact of a person and print out the result
        # It will later be used to be displayed in the UI
        db = Database()
        db_result = db.retrieve_close_contact(personId)
        db.close()
        del db

        [print(row) for row in db_result]

    def get_all_close_contacts(self):
        # Get all history of close contacts and print out the result
        # It will later be used to be displayed in the UI
        db = Database()
        db_result = db.retrieve_all_close_contact()
        db.close()
        del db

        [print(row) for row in db_result]

    def is_running(self):
        # Don't allow for another tracker to run at the same time
        return self._running

    # Run the tracker after it is created
    def run(self):
        # The functions will be run in parallel so the UI can keep working
        # Dies when main thread (only non-daemon thread) exits.
        Thread(target=self._subscribe, daemon=True).start()
        Thread(target=self._read_messages, daemon=True).start()

        self._running = True
