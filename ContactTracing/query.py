# Tomas Costantino - A00042881
from time import sleep
from threading import Thread
from message_broker import MessageBroker


class Query:
    def __init__(self, personId: str = ''):
        self._personId = personId

        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._queryPublisher = MessageBroker(endpoint)
        self._queryConsumer = MessageBroker(endpoint)

        self._subscribed = False

    def publish_query(self):
        # Publishes the identifier of the person asked for
        message = {'personId': self._personId}
        self._queryPublisher.JSON_publish('send_to_tracker', 'query', message)

        # Once query sent now kick off thread to receive if there is something
        self.get_query()

    def get_query(self):
        # Get the query from the tracker and prints it out to the screen

        # If we are not subscribed then subscribe to the query response channel
        if not self._subscribed:
            Thread(target=self._subscribe, daemon=True).start()

        # Try to receive the query
        Thread(target=self._try_to_receive_query, daemon=True).start()

    def _try_to_receive_query(self):
        query_result = None
        counter = 0
        # Try to retrieve the query ten times and if not possible leave the loop
        while query_result is None and counter < 10:
            query_result = self._queryConsumer.get_messages()
            counter += 1
            print('Waiting for query')
            sleep(1)

        # Check if the query is not empty
        if query_result:
            for query in query_result[0].items():
                print(query)

        else:
            print('No query received')

    def _subscribe(self):
        # Subscribes to the query response channel
        self._subscribed = True
        self._queryConsumer.subscribe('sent_from_tracker', 'query_response')
    