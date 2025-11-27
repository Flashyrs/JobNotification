import threading
import time
import os
import datetime
from utils.storage import add_subscriber
from utils.storage import remove_subscriber

from main import main as run_scraper
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

last_scrape_time = None
last_scrape_count = 0


# ========== BOT COMMANDS ==========

async def start(update, context):
    from utils.storage import add_subscriber
    add_subscriber(update.effective_chat.id)

    await update.effective_chat.send_message(
        "✅ You are now subscribed to job alerts!"
    )


async def stop(update, context):
    from utils.storage import remove_subscriber
    remove_subscriber(update.effective_chat.id)

    await update.effective_chat.send_message(
        "❎ You have been unsubscribed."
    )


async def fetch(update, context):
    global last_scrape_time, last_scrape_count

    await update.effective_chat.send_message("🔍 Running scraper now...")

    count = run_scraper()
    last_scrape_time = datetime.datetime.now()
    last_scrape_count = count

    await update.effective_chat.send_message(
        f"✅ Scrape finished! Found {count} new jobs."
    )


async def status(update, context):
    global last_scrape_time, last_scrape_count

    if last_scrape_time:
        msg = f"""
📊 *Scraper Status*
Last Run: {last_scrape_time.strftime('%Y-%m-%d %H:%M:%S')}
Jobs Found: {last_scrape_count}
"""
    else:
        msg = "⚠ No scrapes have run yet."

    await update.effective_chat.send_message(msg, parse_mode="Markdown")


# ========== BACKGROUND SCHEDULER ==========

def scraper_loop():
    global last_scrape_time, last_scrape_count

    while True:
        print("🔄 Running scheduled scraper...")
        count = run_scraper()
        last_scrape_time = datetime.datetime.now()
        last_scrape_count = count

        time.sleep(15 * 60)  # Run every 15 minutes


# ========== MAIN STARTER ==========

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("fetch", fetch))
    app.add_handler(CommandHandler("status", status))

    print("🤖 Telegram bot is now running...")
    app.run_polling()


if __name__ == "__main__":
    # Start scraper loop in a background thread
    threading.Thread(target=scraper_loop, daemon=True).start()

    # Start telegram bot (blocking)
    start_bot()
