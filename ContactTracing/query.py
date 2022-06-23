

class Query:
    def __init__(self, mw_endpoint: str = '', personId: str = ''):
        self._mw_endpoint = mw_endpoint
        self._personId = personId

    def publish_identifier(self):
        pass

    def get_query(self):
        pass
