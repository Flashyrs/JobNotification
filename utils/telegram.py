import requests
import os
import time
from dotenv import load_dotenv
from utils.storage import load_subscribers, get_unseen_jobs_for_user, mark_job_seen

load_dotenv()  # load TELEGRAM_TOKEN

def send(message: str):
    """
    Legacy function - sends same message to all subscribers.
    Use send_jobs() for per-subscriber job notifications.
    """
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        print("Missing Telegram TOKEN")
        return

    subscribers = load_subscribers()
    if not subscribers:
        print("No subscribers to send messages to.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for i, chat_id in enumerate(subscribers):
        try:
            requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                },
                timeout=10
            )
            # Small delay between messages to avoid rate limiting
            if i < len(subscribers) - 1:
                time.sleep(0.5)
        except Exception as e:
            print(f"Telegram error for {chat_id}: {e}")


def send_jobs(all_jobs, format_job_func):
    """
    Send jobs to subscribers, but only jobs they haven't seen.
    
    Args:
        all_jobs: List of job dictionaries
        format_job_func: Function to format job into message (job, scraper_name) -> str
    
    Returns:
        dict: Statistics {chat_id: jobs_sent_count}
    """
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        print("Missing Telegram TOKEN")
        return {}
    
    subscribers = load_subscribers()
    if not subscribers:
        print("No subscribers to send messages to.")
        return {}
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    stats = {}
    
    print(f"\n📤 Sending job notifications to {len(subscribers)} subscriber(s)...")
    
    for chat_id in subscribers:
        # Get jobs this user hasn't seen
        unseen_jobs = get_unseen_jobs_for_user(chat_id, all_jobs)
        
        if not unseen_jobs:
            print(f"  📭 No new jobs for subscriber {chat_id}")
            stats[chat_id] = 0
            continue
        
        print(f"  📬 Sending {len(unseen_jobs)} job(s) to subscriber {chat_id}")
        sent_count = 0
        
        for job in unseen_jobs:
            try:
                # Format the job message
                scraper_name = job.get("scraper", "unknown")
                message = format_job_func(job, scraper_name)
                
                # Send the message
                response = requests.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": "Markdown",
                        "disable_web_page_preview": True
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    # Mark as seen for this user
                    mark_job_seen(chat_id, job.get("id"), job)
                    sent_count += 1
                    print(f"    ✅ Sent: {job.get('company')} - {job.get('title')}")
                else:
                    print(f"    ❌ Failed to send: {response.status_code}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ❌ Error sending job: {e}")
        
        stats[chat_id] = sent_count
    
    return stats


def send_to_user(chat_id, message):
    """
    Send a message to a specific user.
    Used for /fetch command responses.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        print("Missing Telegram TOKEN")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to {chat_id}: {e}")
        return False
