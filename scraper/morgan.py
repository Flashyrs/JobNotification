import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    # Morgan Stanley uses Taleo API
    url = "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-1e4a7e8a5213/candidate/so/pm/1/pl/1/opp/16471-2025-Technology-Full-time-Analyst-Program-Mumbai/en-GB"
    
    # Try to use their API endpoint
    api_url = "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-2/candidate/jobboard/vacancy/1/offset/0"
    
    try:
        response = requests.get(api_url, timeout=20)
        data = response.json()
        
        jobs = []
        
        for job in data.get("requisitionList", []):
            title = job.get("column", [{}])[0].get("value", "") if job.get("column") else ""
            location = job.get("column", [{}])[1].get("value", "") if len(job.get("column", [])) > 1 else ""
            job_id = job.get("jobId", "")
            
            if not is_india(location):
                continue
            
            if any(k in title.lower() for k in KEYWORDS):
                # Construct proper Morgan Stanley careers URL
                apply_url = f"https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/candidate/so/pm/1/pl/1/opp/{job_id}/en-GB"
                
                jobs.append({
                    "id": job_id,
                    "title": title,
                    "company": "Morgan Stanley",
                    "url": apply_url,
                    "location": location
                })
        
        return jobs
    except:
        return []
