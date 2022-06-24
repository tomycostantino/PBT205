from message_broker import MessageBroker


class Tracker:
    def __init__(self, mw_endpoint: str = ''):
        self._mw_endpoint = mw_endpoint
        self._msgBroker = MessageBroker()

    def subscribe(self, topic: str):
        if topic == 'position':
            # Do stuff here to read from middleware and update UI
            pass

        elif topic == 'query':
            # Do stuff here to read from middleware and update UI
            pass


