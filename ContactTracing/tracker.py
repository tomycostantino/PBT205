from message_broker import MessageBroker


class Tracker:
    def __init__(self):
        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._msgBroker = MessageBroker(endpoint)

    def _subscribe(self, topic: str):
        if topic == 'position':
            self._msgBroker.subscribe('position')

        elif topic == 'query':
            self._msgBroker.subscribe('query')

    def run(self):
        self._subscribe('position')
        self._subscribe('query')
