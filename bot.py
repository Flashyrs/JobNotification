import requests
import time
import os
from dotenv import load_dotenv
from utils.subscribers import load_subscribers, save_subscribers

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"
print("BOT STARTED... POLLING NOW")

def listen():
    offset = 0
    subscribers = load_subscribers()

    while True:
        try:
            resp = requests.get(f"{API}/getUpdates?offset={offset}", timeout=15).json()
        except:
            time.sleep(2)
            continue

        for upd in resp.get("result", []):
            offset = upd["update_id"] + 1

            if "message" not in upd:
                continue

            msg = upd["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")

            if text == "/start":
                subscribers.add(chat_id)
                save_subscribers(subscribers)

                requests.post(
                    f"{API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "🎉 You are now subscribed to job alerts!"
                    }
                )

        time.sleep(1)


if __name__ == "__main__":
    listen()
