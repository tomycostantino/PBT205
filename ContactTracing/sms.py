from __future__ import print_function
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException


# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = 'tomas.160201@gmail.com'
configuration.password = 'CC1563A2-D22B-9441-8288-3895583F671C'

# create an instance of the API class
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

# If you want to explictly set from, add the key _from to the message.
sms_message = SmsMessage(source="php",
                        body="Putito",
                        to="+61414967328",
                        schedule=1436874701)

sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

try:
    # Send sms message(s)
    api_response = api_instance.sms_send_post(sms_messages)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
