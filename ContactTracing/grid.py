
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
        '''
        Returns the id of the current object.
        :return:
        '''

        return id(self)

    def _get_query(self, consumer):
        '''
        Try to receive the query
        :param consumer:
        :return:
        '''

        Thread(target=self._read_messages, args=(consumer,), daemon=True).start()

    def _read_messages(self, consumer):
        '''
        Reads messages from the grid response channel
        :param consumer:
        :return:
        '''

        timer = threading.Timer(0.1, self._read_messages, args=(consumer,))
        timer.start()

        messages = consumer.get_messages()

        if messages is not None:
            for message in messages[0]:
                self._message_queue.append(message)

            del consumer
            self._publisher.queue_unbind('sent_from_tracker', self._id)
            self._publisher.queue_delete(self._id)
            timer.cancel()

    def _subscribe(self, consumer):
        '''
        Subscribes to the response channel
        :param consumer:
        :return:
        '''

        consumer.subscribe('sent_from_tracker', self._id)

    def publish_query(self, message):
        '''
        Publishes a query to the tracker.
        :param message:
        :return:
        '''

        # Create consumer first
        consumer = MessageBroker(self._endpoint)
        consumer.queue_declare(self._id)

        message = {'from': 'grid',
                   'type': 'names' if message == 'names' else 'close_contacts',
                   'about': message if message != 'names' else 'all',
                   'reply_on': self._id}

        self._publisher.JSON_publish('sent_to_tracker', 'user_data_get', message)

        Thread(target=self._subscribe, args=(consumer,), daemon=True).start()
        Thread(target=self._get_query, args=(consumer,), daemon=True).start()

    def retrieve_messages(self):
        '''
        Returns the messages in the message queue and clears it
        :return:
        '''

        messages = self._message_queue
        self._message_queue = []
        return messages

