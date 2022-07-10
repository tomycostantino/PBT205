import threading
from database import Database
from threading import Thread
from message_broker import MessageBroker


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._positionBroker = MessageBroker(endpoint)
        self._queryBroker = MessageBroker(endpoint)
        self._queryPublisher = MessageBroker(endpoint)

    # Subscribe to the channels
    # Use a thread to run the function in parallel
    # I created two brokers because they are subscribted to different channels
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

        if position_message:
            self._update_database(position_message)

        elif query_message:
            for query in query_message:
                self._respond_query(query)

    # When a person sends location, update the database
    def _update_database(self, messages):
        db = Database()
        for message in messages:
            db.insert_value(message['personId'], message['position'], message['date'], message['time'])
            print(message)
        db.close()
        del db

    def _respond_query(self, query):
        name = query['person']
        db = Database()
        db_result = db.get_query(name)
        db.close()
        del db

        if db_result:
            results = dict()
            count = 1
            for row in db_result:
                results[count] = {'personId': row[0], 'position': row[1], 'date': row[2], 'time': row[3]}
                count += 1
            print(results)
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query', results)

        else:
            errorMessage = {'error': 'No results found'}
            self._queryPublisher.JSON_publish('sent_from_tracker', 'query', errorMessage)
            print(errorMessage)

    def run(self):
        # The functions will be run in parallel so the UI can keep working
        t1 = Thread(target=self._subscribe)
        t2 = Thread(target=self._read_messages)

        t1.start()
        t2.start()
