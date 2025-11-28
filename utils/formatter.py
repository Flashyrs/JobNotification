"""
Utility functions for formatting job data for Telegram messages
"""
from datetime import datetime

def format_job_message(job, scraper_name=None):
    """
    Format a single job into a Telegram message with Markdown formatting.
    
    Args:
        job (dict): Job dictionary with keys: title, company, url, location, date_posted (optional)
        scraper_name (str, optional): Name of the scraper that found this job
    
    Returns:
        str: Formatted message string
    """
    # Extract job details
    title = job.get("title", "Unknown Role")
    company = job.get("company", "Unknown Company")
    url = job.get("url", "")
    location = job.get("location", "")
    date_posted = job.get("date_posted", "")
    
    # Build the message
    message = f"🎯 *New Job Alert!*\n\n"
    message += f"*Role:* {title}\n"
    message += f"*Company:* {company}\n"
    
    if location:
        message += f"*Location:* {location}\n"
    
    if date_posted:
        message += f"*Posted:* {date_posted}\n"
    
    if scraper_name:
        message += f"*Source:* {scraper_name.title()}\n"
    
    if url:
        message += f"\n🔗 [Apply Here]({url})\n"
    
    return message


def format_relative_date(date_str):
    """
    Convert date string to relative format (e.g., "2 days ago", "Today").
    
    Args:
        date_str: ISO format date string or human-readable date
    
    Returns:
        str: Relative date string
    """
    if not date_str:
        return ""
    
    try:
        # Try to parse ISO format
        if "T" in date_str or "-" in date_str:
            job_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            # Already human-readable
            return date_str
        
        now = datetime.now()
        diff = now - job_date
        
        if diff.days == 0:
            if diff.seconds < 3600:
                return f"{diff.seconds // 60} minutes ago"
            else:
                return f"{diff.seconds // 3600} hours ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            return f"{diff.days // 7} weeks ago"
        else:
            return job_date.strftime("%b %d, %Y")
    except:
        return date_str


def format_job_summary(jobs):
    """
    Format a summary of multiple jobs.
    
    Args:
        jobs (list): List of job dictionaries
    
    Returns:
        str: Formatted summary message
    """
    if not jobs:
        return "No new jobs found."
    
    count = len(jobs)
    companies = set(job.get("company", "Unknown") for job in jobs)
    
    message = f"✨ *Found {count} new job{'s' if count != 1 else ''}!*\n\n"
    message += f"Companies: {', '.join(sorted(companies))}\n"
    
    return message


def format_jobs_list(jobs, max_jobs=10):
    """
    Format a list of jobs into a compact message.
    
    Args:
        jobs (list): List of job dictionaries
        max_jobs (int): Maximum number of jobs to include in one message
    
    Returns:
        list: List of formatted message strings (split if too many jobs)
    """
    if not jobs:
        return ["No jobs to display."]
    
    messages = []
    current_message = f"📋 *Job Listings ({len(jobs)} total)*\n\n"
    
    for i, job in enumerate(jobs[:max_jobs], 1):
        title = job.get("title", "Unknown Role")
        company = job.get("company", "Unknown Company")
        url = job.get("url", "")
        date_posted = job.get("date_posted", "")
        
        job_text = f"{i}. *{company}* - {title}\n"
        if date_posted:
            job_text += f"   📅 {date_posted}\n"
        if url:
            job_text += f"   🔗 [Apply]({url})\n"
        job_text += "\n"
        
        # Telegram has a 4096 character limit per message
        if len(current_message) + len(job_text) > 4000:
            messages.append(current_message)
            current_message = f"📋 *Job Listings (continued)*\n\n{job_text}"
        else:
            current_message += job_text
    
    messages.append(current_message)
    
    if len(jobs) > max_jobs:
        messages.append(f"... and {len(jobs) - max_jobs} more jobs!")
    
    return messages
