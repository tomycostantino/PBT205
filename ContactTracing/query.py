from message_broker import MessageBroker


class Query:
    def __init__(self, mw_endpoint: str = '', personId: str = ''):
        self._mw_endpoint = mw_endpoint
        self._personId = personId

        endpoint = 'amqps://rozfefzx:LCBohEjCaUgnWVrHTroExcQS1vp2CmGU@vulture.rmq.cloudamqp.com/rozfefzx'
        self._msgBroker = MessageBroker(endpoint)

    # Publishes the identifier of the person asked for
    def publish_identifier(self):
        pass

    # Gets the query from the tracker and prints it out to the screen
    def get_query(self):
        pass
    