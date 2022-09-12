# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC2f741f65a1d60acbbc8029778fe1beb2'
auth_token = '4ad347ac5f469e06cdfd0a7667805ce9'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is Tomas trying here',
         from_='+16188275096',
         to='+610414967328'
     )

print(message.sid)
