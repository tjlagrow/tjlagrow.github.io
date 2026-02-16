import requests
from bs4 import BeautifulSoup
import yaml
import datetime
import os
import re
import time
from difflib import SequenceMatcher

# Configuration
SCHOLAR_ID = "KO7oYeAAAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&pagesize=100"
SCHOLAR_DATA_FILE = "../_data/scholar.yml"
PUBS_DATA_FILE = "../_data/research.yml"

def get_scholar_stats():
    """Scrapes Google Scholar for total citation metrics."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Fetching profile stats from: {SCHOLAR_URL}")
        response = requests.get(SCHOLAR_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Total Citations Table
        table = soup.find('table', id='gsc_rsb_st')
        if not table:
            print("Error: Could not find stats table.")
            return None, None

        rows = table.find_all('tr')
        citations = int(rows[1].find_all('td')[1].text)
        hindex = int(rows[2].find_all('td')[1].text)
        i10index = int(rows[3].find_all('td')[1].text)
        
        stats = {
            "citations": citations,
            "hindex": hindex,
            "i10index": i10index,
            "updated": datetime.date.today().strftime("%Y-%m-%d")
        }

        # Parse individual papers from the profile page
        papers = []
        # The main list of papers is usually in a table id='gsc_a_t'
        pub_table = soup.find('table', id='gsc_a_t')
        if pub_table:
            for row in pub_table.find_all('tr', class_='gsc_a_tr'):
                title_link = row.find('a', class_='gsc_a_at')
                if title_link:
                    title = title_link.text.strip()
                    # Citation count is in a cell with class 'gsc_a_c' -> 'a' class 'gsc_a_ac'
                    cite_cell = row.find('td', class_='gsc_a_c')
                    cite_link = cite_cell.find('a', class_='gsc_a_ac') if cite_cell else None
                    
                    cite_count = 0
                    if cite_link and cite_link.text.strip():
                        cite_count = int(cite_link.text.strip())
                    
                    papers.append({'title': title, 'citations': cite_count})
        
        print(f"Found {len(papers)} papers on Scholar profile.")
        return stats, papers
        
    except Exception as e:
        print(f"Error fetching Scholar data: {e}")
        return None, None

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def update_files(stats, scholar_papers):
    """Updates both scholar.yml and research.yml."""
    base_dir = os.path.dirname(__file__)
    
    # 1. Update scholar.yml
    if stats:
        scholar_path = os.path.join(base_dir, SCHOLAR_DATA_FILE)
        try:
            with open(scholar_path, 'w') as f:
                yaml.dump(stats, f, default_flow_style=False, sort_keys=False)
            print(f"Updated {scholar_path}")
        except Exception as e:
            print(f"Error updating scholar.yml: {e}")

    # 2. Update research.yml
    if scholar_papers:
        pubs_path = os.path.join(base_dir, PUBS_DATA_FILE)
        try:
            with open(pubs_path, 'r') as f:
                local_pubs = yaml.safe_load(f)
            
            updated_count = 0
            for pub in local_pubs:
                # Initialize matching logic
                best_match = None
                best_score = 0.0
                
                # Try to find matching paper in scholar_papers
                for sp in scholar_papers:
                    score = similar(pub['title'], sp['title'])
                    if score > 0.85: # Threshold for fuzzy match
                        if score > best_score:
                            best_score = score
                            best_match = sp
                
                if best_match:
                    pub['citations'] = best_match['citations']
                    updated_count += 1
                elif 'citations' not in pub:
                     pub['citations'] = 0 # Initialize if no match found

            with open(pubs_path, 'w') as f:
                yaml.dump(local_pubs, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"Updated {pubs_path}: matched {updated_count} papers.")
            
        except Exception as e:
            print(f"Error updating research.yml: {e}")

if __name__ == "__main__":
    print("Starting Google Scholar update...")
    stats, papers = get_scholar_stats()
    
    if stats:
        update_files(stats, papers)
    else:
        print("Update failed.")
