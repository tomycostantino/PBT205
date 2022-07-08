import pika, os, sys

'''
This class manages the broker interaction required in person, query and tracker components
'''


class MessageBroker:
    def __init__(self, url: str):
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    # Create a new queue in the broker when we are senders
    def queue_declare(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name)

    # Publish a new message on the queue
    def basic_publish(self, routing_key: str, message: str):
        self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)

    # Handle incoming messages
    def _handle_messages(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    # Subscribe to queues
    def subscribe(self, queue_name: str):
        self.channel.basic_consume(queue=queue_name, on_message_callback=self._handle_messages, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

