from __future__ import print_function

from twilio.rest import Client
import api_keys


class Messaging:
    def __init__(self):
        # Configure HTTP basic authorization: BasicAuth
        account_sid = api_keys.account_sid
        auth_token = api_keys.auth_token
        self._client = Client(account_sid, auth_token)

    def send_message(self, to: str, body: str):

        message = self._client.messages \
            .create(
                body=body,
                from_='+16188275096',
                to='+610414967328'
            )
        print(message.sid)
