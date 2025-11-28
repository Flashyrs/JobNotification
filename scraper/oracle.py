import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    # Oracle uses Taleo system
    url = "https://oracle.taleo.net/careersection/2/jobsearch.ftl?lang=en"
    
    # Try alternative API endpoint
    api_url = "https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/11.13.18.05/recruitingCEJobRequisitions"
    
    try:
        # Try the REST API first
        response = requests.get(
            api_url,
            params={
                "onlyData": "true",
                "expand": "requisitionList.secondaryLocations,flexFieldsFacet.values",
                "finder": "findReqs;siteNumber=CX,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,offset=0"
            },
            timeout=20
        )
        data = response.json()
        
        jobs = []
        for item in data.get("items", []):
            title = item.get("Title", "")
            locations = item.get("PrimaryLocation", "")
            
            if not is_india(locations):
                continue
            
            if any(k in title.lower() for k in KEYWORDS):
                req_id = item.get("Id", "")
                # Construct proper Oracle careers URL
                apply_url = f"https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/{req_id}"
                
                jobs.append({
                    "id": req_id,
                    "title": title,
                    "company": "Oracle",
                    "url": apply_url,
                    "location": locations
                })
        
        return jobs
    except:
        return []
