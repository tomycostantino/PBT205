# Tomas Costantino - A00042881
import threading
from database import Database
from threading import Thread
from message_broker import MessageBroker
from time import sleep


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._positionBroker = MessageBroker(endpoint)  # Broker to read position
        self._queryBroker = MessageBroker(endpoint)  # Broker to read query
        self._queryPublisher = MessageBroker(endpoint)  # Broker to publish query

    # Subscribe to the channels
    # Use a thread to run the function in parallel so it does not get stuck in the receiving loop
    # I created two brokers because they are subscribed to different channels
    def _subscribe(self):
        t1 = Thread(target=self._positionBroker.subscribe, args=('send_to_tracker', 'position'))
        t2 = Thread(target=self._queryBroker.subscribe, args=('send_to_tracker', 'query'))
        t1.start()
        t2.start()

    # Read messages from both queues every second
    def _read_messages(self):
        threading.Timer(1, self._read_messages).start()
        position_message = self._positionBroker.get_messages()
        query_message = self._queryBroker.get_messages()

        # Check if the incoming messages are not empty
        if position_message:
            self._update_database(position_message)

        elif query_message:
            for query in query_message:
                self._respond_query(query)

    # When a person sends location, update the database
    def _update_database(self, messages):
        # I create database here and then delete because it can only be used
        # in the thread that it is created in
        db = Database()
        for message in messages:
            db.insert_value(message['personId'].lower(), message['position'], message['date'], message['time'])
            print(message)
        db.close()
        del db

    # Publish what is retrieved from database
    def _respond_query(self, query):
        db = Database()
        # I had an error with the key of the dict so this was my only way to get rid of it
        personId = list(query.items())
        db_result = db.get_query(str(personId[0][1]))

        db.close()
        del db

        # See if what retrieved is empty
        # If we know the person we give all info
        if db_result:
            # Create a big dictionary of dictionaries to send over the broker
            results = dict()
            count = 1
            for row in db_result:
                results[count] = {'personId': row[0], 'position': row[1], 'date': row[2], 'time': row[3]}
                count += 1
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query_response', results)

        # If person not found, send a message saying so
        else:
            errorMessage = {'error': 'No results found'}
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query_response', errorMessage)

    # Run the tracker after it is created
    def run(self):
        # The functions will be run in parallel so the UI can keep working
        t1 = Thread(target=self._subscribe)
        t2 = Thread(target=self._read_messages)

        t1.start()
        t2.start()
