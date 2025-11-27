import requests
import os
from dotenv import load_dotenv
from utils.subscribers import load_subscribers

load_dotenv()  # load TELEGRAM_TOKEN

def send(message: str):
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        print("Missing Telegram TOKEN")
        return

    subscribers = load_subscribers()
    if not subscribers:
        print("No subscribers to send messages to.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for chat_id in subscribers:
        try:
            requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                },
                timeout=10
            )
        except Exception as e:
            print(f"Telegram error for {chat_id}: {e}")
