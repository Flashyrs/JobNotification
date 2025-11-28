import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://www.uber.com/api/loadSearchJobsResults"
    try:
        # Uber uses a different API endpoint
        response = requests.post(
            url,
            json={"params": {"location": [], "department": []}},
            headers={"Content-Type": "application/json"},
            timeout=20
        )
        data = response.json()
    except:
        return []

    jobs = []

    for j in data.get("data", {}).get("results", []):
        title = j.get("title", "")
        loc = j.get("location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            job_id = j.get("id", "")
            # Construct URL with fallback
            apply_url = j.get("apply_url") or j.get("url")
            if not apply_url and job_id:
                apply_url = f"https://www.uber.com/global/en/careers/list/{job_id}"
            
            if apply_url:  # Only add if we have a valid URL
                jobs.append({
                    "id": job_id or apply_url,
                    "title": title,
                    "company": "Uber",
                    "url": apply_url
                })
    return jobs
