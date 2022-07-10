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

        self._actual_position = dict()
        self._actual_position['personId'] = self._personId

    def run(self):
        self._send_location()

    # Send new location to the broker so the tracker updates
    def _send_location(self):

        # Kick off the thread to send the location continuosly
        threading.Timer(self._movement_speed, self._send_location).start()

        # Generate new position
        self._generate_position()

        # Get current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dt = dt_string.split(' ')
        self._actual_position['date'] = dt[0]
        self._actual_position['time'] = dt[1]

        self._msgBroker.JSON_publish('send_to_tracker', 'position', self._actual_position)

    # Will generate a new position to be sent to the broker
    def _generate_position(self):
        x = random.randint(0, self._grid_size[0])
        y = random.randint(0, self._grid_size[1])
        new_position = str(x) + ',' + str(y)
        self._actual_position['position'] = new_position
