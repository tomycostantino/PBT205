from message_broker import MessageBroker


class Person:
    def __init__(self, mw_endpoint: str = '', personId: str = '', movement_speed: str = ''):
        self._mw_endpoint = mw_endpoint
        self._personId = personId
        self.movement_speed = movement_speed
        self._actual_position = tuple()
        self._msgBroker = MessageBroker()

    # Send new location to the broker so the tracker updates
    def send_location(self):
        self._actual_position = self._generate_position()
        # Do stuff here to send it to middleware

    # Will generate a new position to be sent to the broker
    def _generate_position(self) -> tuple:
        new_position = tuple()
        # Generate the new random position for the tracker
        return new_position
