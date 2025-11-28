import os
import threading
import datetime
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from utils.storage import add_subscriber, remove_subscriber, get_unseen_jobs_for_user
from main import run_all_scrapers
from utils.formatter import format_job_message, format_jobs_list

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

last_scrape_time = None
last_scrape_count = 0
last_scraper_stats = {}


async def start(update, context):
    add_subscriber(update.effective_chat.id)
    await update.effective_chat.send_message("✅ You are now subscribed!")


async def stop(update, context):
    remove_subscriber(update.effective_chat.id)
    await update.effective_chat.send_message("❎ You are unsubscribed.")


async def fetch(update, context):
    """Fetch only NEW jobs (unseen by this user)"""
    global last_scrape_time, last_scrape_count, last_scraper_stats

    await update.effective_chat.send_message("🔍 Running scraper...")

    # Run the scraper in a thread pool to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, lambda: run_all_scrapers(return_stats=True))
    
    all_jobs, scraper_stats = result
    last_scraper_stats = scraper_stats
    
    # Filter to only jobs this user hasn't seen
    chat_id = update.effective_chat.id
    unseen_jobs = get_unseen_jobs_for_user(chat_id, all_jobs)
    
    count = len(unseen_jobs)
    total_count = len(all_jobs)
    last_scrape_time = datetime.datetime.now()
    last_scrape_count = count

    # Send scraper statistics
    stats_msg = "📊 *Scraper Results:*\n\n"
    for scraper_name, stats in scraper_stats.items():
        if stats["status"] == "success":
            emoji = "✅" if stats["count"] > 0 else "📭"
            stats_msg += f"{emoji} {scraper_name}: {stats['count']} jobs\n"
        else:
            stats_msg += f"❌ {scraper_name}: Error\n"
    
    stats_msg += f"\n*Total:* {total_count} jobs found"
    stats_msg += f"\n*New for you:* {count} unseen jobs"
    
    await update.effective_chat.send_message(stats_msg, parse_mode="Markdown")
    
    # Send detailed job information for unseen jobs
    if unseen_jobs:
        await update.effective_chat.send_message(
            f"📬 Sending {count} new job{'s' if count != 1 else ''} to you...",
            parse_mode="Markdown"
        )
        
        # Send each job as a separate message for better readability
        for i, job in enumerate(unseen_jobs[:10]):  # Limit to first 10 jobs to avoid spam
            try:
                scraper_name = job.get("scraper", "unknown")
                message = format_job_message(job, scraper_name)
                await update.effective_chat.send_message(
                    message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                # Small delay to avoid rate limiting (only if more messages to send)
                if i < min(len(unseen_jobs), 10) - 1:
                    await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error sending job message: {e}")
        
        # If there are more than 10 jobs, send a summary
        if count > 10:
            await update.effective_chat.send_message(
                f"📝 ... and {count - 10} more jobs! Subscribe with /start to get all notifications.",
                parse_mode="Markdown"
            )
    else:
        await update.effective_chat.send_message(
            "✨ No new jobs for you! You've seen all available jobs.",
            parse_mode="Markdown"
        )


async def fetchall(update, context):
    """Fetch ALL jobs from the last 1-2 days, regardless of seen status"""
    await update.effective_chat.send_message("🔍 Fetching all recent jobs (last 1-2 days)...")

    # Run the scraper in a thread pool to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, lambda: run_all_scrapers(return_stats=True))
    
    all_jobs, scraper_stats = result
    
    # Filter jobs from last 1-2 days based on date_posted
    recent_jobs = []
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=2)
    
    for job in all_jobs:
        # If job has date_posted, check if it's recent
        date_posted = job.get("date_posted", "")
        if date_posted and date_posted != "Recently":
            try:
                # Try to parse the date
                job_date = datetime.datetime.strptime(date_posted, "%b %d, %Y")
                if job_date >= cutoff_date:
                    recent_jobs.append(job)
                    continue
            except:
                pass
        
        # If no date or can't parse, include it (assume recent)
        recent_jobs.append(job)
    
    count = len(recent_jobs)
    total_count = len(all_jobs)

    # Send scraper statistics
    stats_msg = "📊 *Scraper Results (All Recent Jobs):*\n\n"
    for scraper_name, stats in scraper_stats.items():
        if stats["status"] == "success":
            emoji = "✅" if stats["count"] > 0 else "📭"
            stats_msg += f"{emoji} {scraper_name}: {stats['count']} jobs\n"
        else:
            stats_msg += f"❌ {scraper_name}: Error\n"
    
    stats_msg += f"\n*Total:* {total_count} jobs found"
    stats_msg += f"\n*Recent (1-2 days):* {count} jobs"
    
    await update.effective_chat.send_message(stats_msg, parse_mode="Markdown")
    
    # Send detailed job information
    if recent_jobs:
        await update.effective_chat.send_message(
            f"📬 Showing {min(count, 15)} recent job{'s' if count != 1 else ''}...",
            parse_mode="Markdown"
        )
        
        # Send each job as a separate message (limit to 15 to avoid spam)
        for i, job in enumerate(recent_jobs[:15]):
            try:
                scraper_name = job.get("scraper", "unknown")
                message = format_job_message(job, scraper_name)
                await update.effective_chat.send_message(
                    message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                # Small delay to avoid rate limiting
                if i < min(len(recent_jobs), 15) - 1:
                    await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error sending job message: {e}")
        
        # If there are more than 15 jobs, send a summary
        if count > 15:
            await update.effective_chat.send_message(
                f"📝 ... and {count - 15} more jobs! Use /fetch to see only new jobs for you.",
                parse_mode="Markdown"
            )
    else:
        await update.effective_chat.send_message(
            "📭 No recent jobs found in the last 1-2 days.",
            parse_mode="Markdown"
        )


async def status(update, context):
    """Show bot status and last scrape statistics"""
    if last_scrape_time:
        msg = f"📊 *Bot Status*\n\n"
        msg += f"*Last Run:* {last_scrape_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        msg += f"*Jobs Found:* {last_scrape_count}\n\n"
        
        if last_scraper_stats:
            msg += "*Last Scraper Results:*\n"
            for scraper_name, stats in last_scraper_stats.items():
                if stats["status"] == "success":
                    emoji = "✅" if stats["count"] > 0 else "📭"
                    msg += f"{emoji} {scraper_name}: {stats['count']}\n"
                else:
                    msg += f"❌ {scraper_name}: Error\n"
    else:
        msg = "⚠ No scrapes yet."

    await update.effective_chat.send_message(msg, parse_mode="Markdown")


async def help_command(update, context):
    """Show available commands"""
    help_text = """
🤖 *Available Commands:*

/start - Subscribe to job notifications
/stop - Unsubscribe from notifications
/fetch - Get new jobs (only unseen by you)
/fetchall - Get ALL recent jobs (last 1-2 days)
/status - Show bot status and scraper stats
/help - Show this help message

📊 *How it works:*
• /fetch shows only jobs you haven't seen
• /fetchall shows all jobs from last 1-2 days
• Both commands show which scrapers ran and how many jobs each found
• Subscribe with /start to get automatic notifications
"""
    await update.effective_chat.send_message(help_text, parse_mode="Markdown")


def scraper_loop():
    """Background scraper that runs every 15 minutes"""
    global last_scrape_time, last_scrape_count

    while True:
        print("🔄 Running scheduled scraper...")
        try:
            from main import main as run_main_scraper
            new_jobs = run_main_scraper()
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
    app.add_handler(CommandHandler("fetchall", fetchall))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_command))

    print("🤖 Telegram bot is running...")
    
    # Run the bot - this handles the event loop internally
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
