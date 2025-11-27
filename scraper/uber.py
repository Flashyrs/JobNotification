import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://www.uber.com/api/jobs/search?query=software"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for j in data.get("jobs", []):
        title = j.get("title", "")
        loc = j.get("location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": j.get("job_id"),
                "title": title,
                "company": "Uber",
                "url": j.get("apply_url")
            })
    return jobs
