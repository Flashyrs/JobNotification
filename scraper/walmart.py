import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    # Walmart uses a different API structure
    url = "https://careers.walmart.com/api/jobs"
    
    try:
        response = requests.get(
            url,
            params={
                "q": "software",
                "page": "1",
                "sort": "rank",
                "expand": "department,brand,type,rate"
            },
            timeout=20
        )
        data = response.json()
    except:
        return []

    jobs = []
    
    for job in data.get("jobs", []):
        title = job.get("title", "")
        location = job.get("location", "")
        
        # Add India location filter
        if not is_india(location):
            continue
        
        if any(k in title.lower() for k in KEYWORDS):
            job_id = job.get("id", "")
            req_id = job.get("reqId", "") or job_id
            
            # Construct URL with fallback
            apply_url = job.get("applyUrl") or job.get("url")
            if not apply_url and req_id:
                apply_url = f"https://careers.walmart.com/us/jobs/{req_id}"
            
            if apply_url:  # Only add if we have a valid URL
                jobs.append({
                    "id": job_id or req_id,
                    "title": title,
                    "company": "Walmart",
                    "url": apply_url,
                    "location": location
                })

    return jobs
