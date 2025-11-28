import requests
from scraper.common import KEYWORDS, is_india
from datetime import datetime

def scrape():
    url = "https://careers.google.com/api/v3/search/?q=software"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        locations = job.get("locations", [])
        
        # Check if any location is in India
        if not any(is_india(l) for l in locations):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            # Get the first India location
            india_location = next((l for l in locations if is_india(l)), "")
            
            # Extract date posted
            date_posted = job.get("posted_date", "") or job.get("publish_date", "")
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
                "company": "Google",
                "url": f"https://careers.google.com/jobs/results/{job.get('id')}",
                "location": india_location,
                "date_posted": date_posted or "Recently"
            })
    return jobs
