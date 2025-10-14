# This class is responsible for sending WhatsApp notifications with the deal flight details.

# first try just print().

# and then add Twilio to send WhatsApp messages with price, IATA codes, dates.

import os
from twilio.rest import Client

class NotificationManager:

    def __init__(self):
        self.client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    def send_whatsapp(self, message_body):
        try:
            message = self.client.messages.create(
                from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}",
                body=message_body,
                to=f"whatsapp:{os.getenv('TWILIO_MY_WHATSAPP')}"
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
