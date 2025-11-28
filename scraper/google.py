import requests
from scraper.common import KEYWORDS, is_india

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
            
            jobs.append({
                "id": job.get("id"),
                "title": title,
                "company": "Google",
                "url": f"https://careers.google.com/jobs/results/{job.get('id')}",
                "location": india_location
            })
    return jobs
