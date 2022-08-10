# Tomas Costantino - A00042881
import pika, os, sys
import json
'''
This class manages the broker interaction required in person, query and tracker components
'''


class MessageBroker:
    def __init__(self, url: str):

        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # It will store the messages received and will clear when asked by the tracker
        self._messageQueue = []

    def queue_declare(self, queue_name: str):
        # Create a new queue in the broker when we are senders
        self.channel.queue_declare(queue=queue_name)

    def basic_publish(self, exchange: str, routing_key: str, message: str):
        # Publish a new message on the queue
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    def JSON_publish(self, exchange: str, routing_key: str, message: dict):
        # Publish a JSON message on the queue, makes it easier when working with that type of data
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message))

    def _handle_messages(self, ch, method, properties, body):
        # Handle incoming messages
        # And add them to queue to then get picked up by tracker
        new_message = json.loads(body)
        print(new_message)
        self._messageQueue.append(new_message)

    def get_messages(self):
        # This function will add return the message queue it has to the tracker when
        # the tracker asks for it
        if self._messageQueue:
            messages = self._messageQueue
            self._messageQueue = []
            return messages

    def subscribe(self, exchange: str, queue_name: str):
        # Subscribe to queue
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self._handle_messages, auto_ack=True)
        self.channel.start_consuming()

