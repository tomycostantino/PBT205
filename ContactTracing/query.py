# Tomas Costantino - A00042881
import threading
from time import sleep
from threading import Thread
from message_broker import MessageBroker


class Query:
    def __init__(self):

        self._endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._publisher = MessageBroker(self._endpoint)
        self._id = str(self._get_id())

    def _get_id(self):
        return id(self)

    def publish_query(self, message):
        # Create consumer first
        consumer = MessageBroker(self._endpoint)
        consumer.queue_declare(self._id)
        # consumer.queue_bind('sent_from_tracker', self._id)

        message = {'from': 'query',
                   'type': 'names' if message == 'names' else 'positions',
                   'about': message if message != 'names' else 'all',
                   'reply_on': self._id}

        self._publisher.JSON_publish('sent_to_tracker', 'user_data_get', message)

        Thread(target=self._subscribe, args=(consumer,), daemon=True).start()
        Thread(target=self.get_query, args=(consumer,), daemon=True).start()

    def get_query(self, consumer):
        # Try to receive the query
        Thread(target=self.read_messages, args=(consumer,), daemon=True).start()

    def read_messages(self, consumer):
        threading.Timer(1, self.read_messages, args=(consumer,)).start()

        messages = consumer.get_messages()
        if messages is not None:
            for message in messages[0].items():
                print(message)
            del consumer
            self._publisher.queue_unbind('sent_from_tracker', self._id)
            self._publisher.queue_delete(self._id)

    def _subscribe(self, consumer):
        # Subscribes to the query response channel
        consumer.subscribe('sent_from_tracker', self._id)
    