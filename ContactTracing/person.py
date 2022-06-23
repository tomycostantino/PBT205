

class Person:
    def __init__(self, mw_endpoint: str = '', personId: str = '', movement_speed: str = ''):
        self._mw_endpoint = mw_endpoint
        self._personId = personId
        self.movement_speed = movement_speed
        self._actual_position = tuple()

    def send_location(self):
        self._actual_position = self._generate_position()
        # Do stuff here to send it to middleware

    def _generate_position(self) -> tuple:
        new_position = tuple()
        # Do stuff here
        return new_position
