import threading
from time import sleep
from threading import Thread
from message_broker import MessageBroker


class Query:
    def __init__(self, personId: str = ''):
        self._personId = personId

        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._queryPublisher = MessageBroker(endpoint)
        self._queryConsumer = MessageBroker(endpoint)

    # Publishes the identifier of the person asked for
    def publish_query(self):
        message = {'person': self._personId}
        self._queryPublisher.JSON_publish('send_to_tracker', 'query', message)
        query_thread = Thread(target=self.get_query)
        query_thread.start()

    # Gets the query from the tracker and prints it out to the screen
    def get_query(self):
        thread = Thread(target=self._subscribe)
        thread.start()

        query = None
        counter = 0
        while query is None and counter < 10:
            query = self._queryConsumer.get_messages()
            counter += 1
            sleep(1)

        print(query)

    def _subscribe(self):
        self._queryConsumer.subscribe('sent_from_tracker', 'query')
    