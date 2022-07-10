import threading
from threading import Thread
from message_broker import MessageBroker


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._positionBroker = MessageBroker(endpoint)
        self._queryBroker = MessageBroker(endpoint)

    def _subscribe(self):
        self._positionBroker.subscribe('send_to_tracker', 'position')
        self._queryBroker.subscribe('send_to_tracker', 'query')

    def _read_messages(self):
        threading.Timer(1, self._read_messages).start()
        position_message = self._positionBroker.get_messages()
        query_message = self._queryBroker.get_messages()

        if position_message:
            print(position_message)

        elif query_message:
            print(query_message)

    def run(self):
        # The functions will be run in parallel so the UI can keep working
        t1 = Thread(target=self._subscribe)
        t2 = Thread(target=self._read_messages)

        t1.start()
        t2.start()
