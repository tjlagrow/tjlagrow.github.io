import urllib.request
import json
import time
import os
import html

def fetch_all(endpoint):
    base_url = f"https://sites.gatech.edu/omscs7641/wp-json/wp/v2/{endpoint}"
    page = 1
    all_items = []
    
    while True:
        url = f"{base_url}?per_page=50&page={page}&_embed=1"
        try:
            print(f"Fetching {endpoint} page {page}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as r:
                items = json.loads(r.read().decode('utf-8'))
                if not items:
                    break
                all_items.extend(items)
                print(f"Retrieved {len(items)} items. Total so far: {len(all_items)}")
                page += 1
                time.sleep(0.5)
        except urllib.error.HTTPError as e:
            if e.code == 400: # Page out of range
                break
            else:
                print(f"HTTP Error: {e.code} for page {page}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return all_items

def get_author_name(item):
    try:
        embedded = item.get("_embedded", {})
        authors = embedded.get("author", [])
        if authors:
            return authors[0].get("name", "")
    except Exception:
        pass
    return ""

def main():
    posts = fetch_all("posts")
    pages = fetch_all("pages")
    
    print(f"\nFetched {len(posts)} posts and {len(pages)} pages in total.")
    
    processed_items = []
    
    # Process posts
    for p in posts:
        author = get_author_name(p)
        content_html = p.get("content", {}).get("rendered", "")
        title = p.get("title", {}).get("rendered", "")
        link = p.get("link", "")
        date = p.get("date", "")
        
        title = html.unescape(title)
        
        processed_items.append({
            "id": p.get("id"),
            "title": title,
            "url": link,
            "date": date,
            "author": author,
            "content_html": content_html,
            "type": "omscs7641_post"
        })
        
    # Process pages
    for pg in pages:
        author = get_author_name(pg)
        content_html = pg.get("content", {}).get("rendered", "")
        title = pg.get("title", {}).get("rendered", "")
        link = pg.get("link", "")
        date = pg.get("date", "")
        
        title = html.unescape(title)
        
        if not content_html.strip() or title.lower() in ["sample page"]:
            continue
            
        processed_items.append({
            "id": pg.get("id"),
            "title": title,
            "url": link,
            "date": date,
            "author": author,
            "content_html": content_html,
            "type": "omscs7641_page"
        })
        
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_path = os.path.join(project_root, "_data", "omscs7641_content.json")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_items, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(processed_items)} items to {output_path}")

if __name__ == "__main__":
    main()
