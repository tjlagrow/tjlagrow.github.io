import requests
from bs4 import BeautifulSoup
import yaml
import os
from difflib import SequenceMatcher

# Configuration
SCHOLAR_ID = "KO7oYeAAAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&pagesize=100&sortby=pubdate"
PUBS_DATA_FILE = "../_data/research.yml"

def get_scholar_papers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Fetching profile from: {SCHOLAR_URL}")
    try:
        response = requests.get(SCHOLAR_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        papers = []
        pub_table = soup.find('table', id='gsc_a_t')
        if pub_table:
            for row in pub_table.find_all('tr', class_='gsc_a_tr'):
                title_link = row.find('a', class_='gsc_a_at')
                if title_link:
                    title = title_link.text.strip()
                    # authors are usually in the first div under the td class gsc_a_t
                    details_cell = row.find('td', class_='gsc_a_t')
                    divs = details_cell.find_all('div')
                    authors = divs[0].text.strip() if len(divs) > 0 else ""
                    venue = divs[1].text.strip() if len(divs) > 1 else ""
                    
                    # year is in gsc_a_y
                    year_cell = row.find('td', class_='gsc_a_y')
                    year = year_cell.text.strip() if year_cell else ""
                    
                    papers.append({
                        'title': title,
                        'authors': authors,
                        'venue': venue,
                        'year': year
                    })
        return papers
    except Exception as e:
        print(f"Error: {e}")
        return []

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_missing():
    base_dir = os.path.dirname(__file__)
    pubs_path = os.path.join(base_dir, PUBS_DATA_FILE)
    
    with open(pubs_path, 'r') as f:
        local_pubs = yaml.safe_load(f)
    
    scholar_papers = get_scholar_papers()
    
    print(f"\nScanning {len(scholar_papers)} papers from Scholar against {len(local_pubs)} local papers...\n")
    
    missing_papers = []
    
    for sp in scholar_papers:
        is_found = False
        for lp in local_pubs:
            if similar(sp['title'], lp['title']) > 0.85:
                is_found = True
                break
        
        if not is_found:
            missing_papers.append(sp)
            print(f"MISSING: [{sp['year']}] {sp['title']}")
            print(f"          Authors: {sp['authors']}")
            print(f"          Venue:   {sp['venue']}")
            print("-" * 50)

if __name__ == "__main__":
    find_missing()
