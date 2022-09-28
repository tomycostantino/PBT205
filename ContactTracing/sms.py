# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from api_keys import *

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = account_sid
auth_token = auth_token
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is Tomas trying here',
         from_='+16188275096',
         to='+610414967328'
     )

print(message.sid)
