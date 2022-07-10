import random
import threading

from message_broker import MessageBroker
from datetime import datetime


class Person:
    def __init__(self, personId: str = '', movement_speed: str = '', grid_size: tuple = (10, 10)):
        self._personId = personId
        self._movement_speed = float(movement_speed)
        self._grid_size = grid_size

        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._msgBroker = MessageBroker(endpoint)

    def run(self):
        self._send_location()

    # Send new location to the broker so the tracker updates
    def _send_location(self):
        threading.Timer(self._movement_speed, self._send_location).start()
        self._generate_position()

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dt = dt_string.split(' ')
        date = dt[0]
        time = dt[1]

        message = str(self._personId) + ', ' + str(self._actual_position) + ', ' + date + ', ' + time

        self._msgBroker.basic_publish('send_to_tracker', 'position', message)

    # Will generate a new position to be sent to the broker
    def _generate_position(self):
        x = random.randint(0, self._grid_size[0])
        y = random.randint(0, self._grid_size[1])
        self._actual_position = str(x) + ', ' + str(y)
