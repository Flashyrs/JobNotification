import os
import asyncio
import threading
import datetime
import time

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from utils.storage import add_subscriber, remove_subscriber
from main import main as run_scraper

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

last_scrape_time = None
last_scrape_count = 0


async def start(update, context):
    add_subscriber(update.effective_chat.id)
    await update.effective_chat.send_message("✅ You are now subscribed!")


async def stop(update, context):
    remove_subscriber(update.effective_chat.id)
    await update.effective_chat.send_message("❎ You are unsubscribed.")


async def fetch(update, context):
    global last_scrape_time, last_scrape_count

    await update.effective_chat.send_message("🔍 Running scraper...")

    new_jobs = run_scraper()
    count = len(new_jobs) if new_jobs else 0
    last_scrape_time = datetime.datetime.now()
    last_scrape_count = count

    await update.effective_chat.send_message(f"✅ Found {count} new jobs.")


async def status(update, context):
    if last_scrape_time:
        msg = f"""
📊 *Status*
Last Run: {last_scrape_time}
Jobs Found: {last_scrape_count}
"""
    else:
        msg = "⚠ No scrapes yet."

    await update.effective_chat.send_message(msg, parse_mode="Markdown")


def scraper_loop():
    global last_scrape_time, last_scrape_count

    while True:
        print("🔄 Running scheduled scraper...")
        new_jobs = run_scraper()
        count = len(new_jobs) if new_jobs else 0
        last_scrape_time = datetime.datetime.now()
        last_scrape_count = count
        time.sleep(15 * 60)


async def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("fetch", fetch))
    app.add_handler(CommandHandler("status", status))

    print("🤖 Telegram bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    threading.Thread(target=scraper_loop, daemon=True).start()

    asyncio.run(run_bot())
