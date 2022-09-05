from __future__ import print_function

import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from sms_database import SmsDatabase


class Messaging:
    def __init__(self):
        # Configure HTTP basic authorization: BasicAuth
        configuration = clicksend_client.Configuration()
        configuration.username = ''
        configuration.password = ''

        self._api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

    def send_message(self, to: str, body: str):

        sms = SmsMessage(source="php",
                         body=body,
                         to=to,
                         schedule=1436874701)

        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms])

        try:
            api_response = self._api_instance.sms_send_post(sms_messages)
            if api_response.data is not None:
                SmsDatabase().insert_sms_data(to, body)
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
