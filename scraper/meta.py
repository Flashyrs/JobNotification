import requests
from scraper.common import KEYWORDS, is_india
from datetime import datetime

def scrape():
    url = "https://www.metacareers.com/api/v1/jobs?q=software"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for job in data.get("data", []):
        title = job.get("title", "")
        loc = job.get("formatted_location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            # Extract date posted
            date_posted = job.get("posted_date", "") or job.get("created_time", "")
            if date_posted:
                try:
                    # Convert to readable format
                    dt = datetime.fromisoformat(date_posted.replace("Z", "+00:00"))
                    date_posted = dt.strftime("%b %d, %Y")
                except:
                    pass
            
            jobs.append({
                "id": job.get("id"),
                "title": title,
                "company": "Meta",
                "url": job.get("canonical_url"),
                "location": loc,
                "date_posted": date_posted or "Recently"
            })
    return jobs
