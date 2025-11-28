import os
import threading
import datetime
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

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

    # Run the scraper in a thread pool to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        new_jobs = await loop.run_in_executor(executor, run_scraper)
    
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
        try:
            new_jobs = run_scraper()
            count = len(new_jobs) if new_jobs else 0
            last_scrape_time = datetime.datetime.now()
            last_scrape_count = count
            print(f"✅ Scraper completed: {count} new jobs found")
        except Exception as e:
            print(f"❌ Scraper error: {e}")
        
        time.sleep(15 * 60)


def main():
    # Start the scraper loop in a background thread
    threading.Thread(target=scraper_loop, daemon=True).start()

    # Build the application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("fetch", fetch))
    app.add_handler(CommandHandler("status", status))

    print("🤖 Telegram bot is running...")
    
    # Run the bot - this handles the event loop internally
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
