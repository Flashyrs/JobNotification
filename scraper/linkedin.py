import requests
from bs4 import BeautifulSoup
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://www.linkedin.com/jobs/search?keywords=software&location=India"
    try:
        html = requests.get(url, timeout=20).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    cards = soup.select("div.base-card")

    for card in cards:
        title_tag = card.select_one("h3.base-search-card__title")
        company_tag = card.select_one("h4.base-search-card__subtitle")
        link_tag = card.select_one("a.base-card__full-link")

        if not (title_tag and company_tag and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        company = company_tag.get_text(strip=True)
        link = link_tag.get("href", "")

        if not is_india(card.get_text()):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": link,
                "title": title,
                "company": company,
                "url": link
            })

    return jobs
