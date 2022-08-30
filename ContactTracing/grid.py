
import threading
from threading import Thread
from message_broker import MessageBroker


class Grid:
    def __init__(self):

        self._endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._publisher = MessageBroker(self._endpoint)
        self._id = str(self._get_id())

        self._message_queue = []

    def _get_id(self):
        return id(self)

    def publish_query(self, message):
        # Create consumer first
        consumer = MessageBroker(self._endpoint)
        consumer.queue_declare(self._id)
        # consumer.queue_bind('sent_from_tracker', self._id)

        message = {'from': 'grid',
                   'type': 'names' if message == 'names' else 'close_contacts',
                   'about': message if message != 'names' else 'all',
                   'reply_on': self._id}

        self._publisher.JSON_publish('sent_to_tracker', 'user_data_get', message)

        Thread(target=self._subscribe, args=(consumer,), daemon=True).start()
        Thread(target=self.get_query, args=(consumer,), daemon=True).start()

    def get_query(self, consumer):
        # Try to receive the query
        Thread(target=self._read_messages, args=(consumer,), daemon=True).start()

    def _read_messages(self, consumer):
        threading.Timer(0.1, self._read_messages, args=(consumer,)).start()

        messages = consumer.get_messages()
        idx = 0
        if messages is not None:
            for message in messages[0][idx].items():
                self._message_queue.append(message)
                idx += 1
            del consumer
            self._publisher.queue_unbind('sent_from_tracker', self._id)
            self._publisher.queue_delete(self._id)

    def get_messages(self):
        return self._message_queue

    def _subscribe(self, consumer):
        # Subscribes to the query response channel
        consumer.subscribe('sent_from_tracker', self._id)

