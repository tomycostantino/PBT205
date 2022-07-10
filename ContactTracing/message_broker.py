import pika, os, sys

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

    # Create a new queue in the broker when we are senders
    def queue_declare(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name)

    # Publish a new message on the queue
    def basic_publish(self, exchange: str, routing_key: str, message: str):
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    # Handle incoming messages
    # And add them to queue to then get picked up by tracker
    def _handle_messages(self, ch, method, properties, body):
        str_body = str(body, 'utf-8')
        segments = str_body.split(', ')
        name = segments[0]
        position = segments[1] + ', ' + segments[2]
        date = segments[3]
        time = segments[4]
        message = (name, position, date, time)
        self._messageQueue.append(message)

    # This function will add return the message queue it has to the tracker when
    # the tracker asks for it
    def get_messages(self):
        if self._messageQueue:
            messages = [m for m in self._messageQueue]
            self._messageQueue = []
            return messages

    # Subscribe to queues
    def subscribe(self, exchange: str, queue_name: str):
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self._handle_messages, auto_ack=True)
        self.channel.start_consuming()
