import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    # Goldman Sachs uses their own API
    url = "https://goldmansachs.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-0/candidate/jobboard/vacancy/1/offset/0"
    
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        
        jobs = []
        
        for job in data.get("requisitionList", []):
            columns = job.get("column", [])
            
            # Extract title and location from columns
            title = columns[0].get("value", "") if len(columns) > 0 else ""
            location = columns[1].get("value", "") if len(columns) > 1 else ""
            job_id = job.get("jobId", "")
            
            if not is_india(location):
                continue
            
            if any(k in title.lower() for k in KEYWORDS):
                # Construct proper Goldman Sachs careers URL
                apply_url = f"https://goldmansachs.tal.net/vx/lang-en-GB/mobile-0/brand-0/candidate/so/pm/1/pl/1/opp/{job_id}/en-GB"
                
                jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": "Goldman Sachs",
                    "url": apply_url,
                    "location": location
                })
        
        return jobs
    except:
        return []
