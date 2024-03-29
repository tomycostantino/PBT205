# Tomas Costantino - A00042881
import random
import threading

from message_broker import MessageBroker
from datetime import datetime
from threading import Thread


class Person:
    def __init__(self, personId: str = '', contact: str = '', movement_speed: str = '', grid_size: tuple = (10, 10)):
        self._movement_speed = float(movement_speed)
        self._grid_size = grid_size

        endpoint = 'amqps://bueyyocn:Z4EAvfK6ZD5HTAlSPdrmrBfLcSzSX2Hb@vulture.rmq.cloudamqp.com/bueyyocn'
        self._msgBroker = MessageBroker(endpoint)

        self._actual_position = dict()
        self._actual_position['personId'] = personId
        self._actual_position['contact'] = contact

    def _send_location(self):
        # Send new location to the broker so the tracker updates

        # Kick off the thread to send the location continuously
        threading.Timer(self._movement_speed, self._send_location).start()

        # Generate new position
        self._generate_position()

        # Get current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # Split date and time to have them separated
        dt = dt_string.split(' ')
        self._actual_position['date'] = dt[0]
        self._actual_position['time'] = dt[1]

        self._msgBroker.JSON_publish('sent_to_tracker', 'position_queue', self._actual_position)

    def _generate_position(self):
        # Will generate a new position to be sent to the broker
        x = random.randint(0, self._grid_size[0])
        y = random.randint(0, self._grid_size[1])
        new_position = str(x) + ', ' + str(y)
        self._actual_position['position'] = new_position

    def run(self):
        Thread(target=self._send_location, daemon=True).start()
