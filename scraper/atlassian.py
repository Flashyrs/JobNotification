import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://boards-api.greenhouse.io/v1/boards/atlassian/jobs?content=true"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        
        # Get location from the job object
        location_obj = job.get("location", {})
        if isinstance(location_obj, dict):
            location = location_obj.get("name", "")
        else:
            location = str(location_obj) if location_obj else ""
        
        # Add India location filter
        if not is_india(location):
            continue
        
        if any(k in title.lower() for k in KEYWORDS):
            job_id = job.get("id", "")
            apply_url = job.get("absolute_url", "")
            
            # Fallback URL construction if absolute_url is missing
            if not apply_url and job_id:
                apply_url = f"https://jobs.lever.co/atlassian/{job_id}"
            
            if apply_url:  # Only add if we have a valid URL
                jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": "Atlassian",
                    "url": apply_url,
                    "location": location
                })

    return jobs
