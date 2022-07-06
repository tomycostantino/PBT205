import random
import threading
from message_broker import MessageBroker


class Person:
    def __init__(self, mw_endpoint: str = '', personId: str = '', movement_speed: str = '', grid_size: tuple = (10, 10)):
        self._mw_endpoint = mw_endpoint
        self._personId = personId
        self._movement_speed = float(movement_speed)
        self._grid_size = grid_size
        #self._msgBroker = MessageBroker()

    def run(self):
        self._send_location()

    # Send new location to the broker so the tracker updates
    def _send_location(self):
        threading.Timer(self._movement_speed, self._send_location).start()
        self._generate_position()
        print(self._personId)
        print(self._actual_position)

        # Do stuff here to send it to middleware it would be something like:
        # self._msgBroker.basic_publish(self._actual_position, self._personId)

    # Will generate a new position to be sent to the broker
    def _generate_position(self):
        x = random.randint(0, self._grid_size[0])
        y = random.randint(0, self._grid_size[1])
        self._actual_position = (x, y)
