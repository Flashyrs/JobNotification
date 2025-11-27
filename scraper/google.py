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
        loc = job.get("locations", [])
        if not any(is_india(l) for l in loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": job.get("id"),
                "title": title,
                "company": "Google",
                "url": f"https://careers.google.com/jobs/results/{job.get('id')}"
            })
    return jobs
