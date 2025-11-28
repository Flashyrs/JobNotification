"""
Utility functions for formatting job data for Telegram messages
"""

def format_job_message(job, scraper_name=None):
    """
    Format a single job into a Telegram message with Markdown formatting.
    
    Args:
        job (dict): Job dictionary with keys: title, company, url, location (optional)
        scraper_name (str, optional): Name of the scraper that found this job
    
    Returns:
        str: Formatted message string
    """
    # Extract job details
    title = job.get("title", "Unknown Role")
    company = job.get("company", "Unknown Company")
    url = job.get("url", "")
    location = job.get("location", "")
    
    # Build the message
    message = f"🎯 *New Job Alert!*\n\n"
    message += f"*Role:* {title}\n"
    message += f"*Company:* {company}\n"
    
    if location:
        message += f"*Location:* {location}\n"
    
    if scraper_name:
        message += f"*Source:* {scraper_name.title()}\n"
    
    if url:
        message += f"\n🔗 [Apply Here]({url})\n"
    
    return message


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
        
        job_text = f"{i}. *{company}* - {title}\n"
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
