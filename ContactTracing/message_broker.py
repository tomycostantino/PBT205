import pika, os, sys

'''
This class manages the broker interaction required in person, query and tracker components
'''


class MessageBroker:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    # Create a new queue in the broker when we are senders
    def queue_declare(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name)

    # Publish a new message on the queue
    def basic_publish(self, message: str, routing_key: str):
        self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)
