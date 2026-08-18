import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        requests.post(
            url,
            data={
                "chat_id": self.chat_id,
                "text": text,
            },
            timeout=30,
        )
