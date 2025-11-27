import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://www.amazon.jobs/en/search.json?category=student-programs"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for j in data.get("jobs", []):
        title = j.get("title", "")
        loc = j.get("normalized_location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": j.get("job_id"),
                "title": title,
                "company": "Amazon",
                "url": "https://www.amazon.jobs" + j.get("job_path", "")
            })
    return jobs
