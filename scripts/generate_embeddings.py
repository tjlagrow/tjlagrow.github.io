import os
import re
import json
import yaml
import html

# Root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Directories
PAGES_DIR = os.path.join(PROJECT_ROOT, "_pages")
POSTS_DIR = os.path.join(PROJECT_ROOT, "_posts")
NEWSLETTERS_DIR = os.path.join(PROJECT_ROOT, "_newsletters")
DATA_DIR = os.path.join(PROJECT_ROOT, "_data")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "assets", "json", "embeddings.json")

def clean_content(content):
    """Strips YAML front matter, Liquid tags, HTML, and Markdown syntax."""
    # Decode HTML entities
    content = html.unescape(content)
    
    # Remove YAML front matter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
            
    # Remove Liquid tags {% ... %} and {{ ... }}
    content = re.sub(r'\{%.*?%\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\{\{.*?\}\}', '', content, flags=re.DOTALL)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove HTML tags (keep text)
    content = re.sub(r'<[^>]+>', ' ', content)
    
    # Clean markdown links [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    
    # Clean headings, lists, bold, italics, code blocks
    content = re.sub(r'#+\s+', '', content)
    content = re.sub(r'[*_`~]', '', content)
    content = re.sub(r'-\s+', '', content)
    
    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def chunk_text(text, max_words=120):
    """Splits text into chunks of ~120 words to preserve context bounds."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        if not words:
            continue
        word_count = len(words)
        
        if current_word_count + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
            
        current_chunk.append(sentence)
        current_word_count += word_count
        
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

def parse_front_matter(file_path):
    """Extracts front matter and content from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    title = os.path.basename(file_path)
    url = None
    layout = "page"
    
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                if meta:
                    title = meta.get("title", title)
                    url = meta.get("permalink", url)
                    layout = meta.get("layout", layout)
            except Exception as e:
                print(f"Error parsing YAML front matter for {file_path}: {e}")
                
    return title, url, layout, raw

def get_post_url(filename, front_matter_categories):
    """Generates the pretty URL for a blog post based on filename and categories."""
    # Filename format: YYYY-MM-DD-title.md
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|html)$', filename)
    if not m:
        return f"/posts/{filename}"
        
    year, month, day, slug = m.groups()[:4]
    
    # categories: could be space separated string or list
    cats = []
    if front_matter_categories:
        if isinstance(front_matter_categories, list):
            cats = front_matter_categories
        elif isinstance(front_matter_categories, str):
            cats = front_matter_categories.split()
            
    cat_path = "/".join(cats)
    if cat_path:
        return f"/{cat_path}/{year}/{month}/{day}/{slug}/"
    else:
        return f"/{year}/{month}/{day}/{slug}/"

def extract_chunks():
    """Compiles all text chunks across pages, posts, newsletters, and YAML databases."""
    chunks = []
    
    # 1. Parse Pages
    if os.path.isdir(PAGES_DIR):
        for root, _, files in os.walk(PAGES_DIR):
            for file in files:
                if file.endswith((".html", ".md")):
                    path = os.path.join(root, file)
                    title, url, layout, raw = parse_front_matter(path)
                    
                    # Skip search index json, 404, feed, etc.
                    if "waddles" in file.lower() or "search.json" in file.lower() or "feed.xml" in file.lower():
                        continue
                        
                    clean_txt = clean_content(raw)
                    if not clean_txt:
                        continue
                        
                    # Fallback URL
                    if not url:
                        url_name = os.path.splitext(file)[0]
                        url = f"/{url_name}/"
                        
                    for text_chunk in chunk_text(clean_txt):
                        chunks.append({
                            "title": title,
                            "url": url,
                            "text": text_chunk,
                            "type": "page"
                        })
                        
    # 2. Parse Posts
    if os.path.isdir(POSTS_DIR):
        for file in os.listdir(POSTS_DIR):
            if file.endswith((".md", ".html")):
                path = os.path.join(POSTS_DIR, file)
                title, url, layout, raw = parse_front_matter(path)
                clean_txt = clean_content(raw)
                if not clean_txt:
                    continue
                
                # Get categories from front matter to build permalink
                categories = None
                if raw.startswith("---"):
                    parts = raw.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            meta = yaml.safe_load(parts[1])
                            if meta:
                                categories = meta.get("categories")
                        except Exception:
                            pass
                            
                url = get_post_url(file, categories)
                for text_chunk in chunk_text(clean_txt):
                    chunks.append({
                        "title": title,
                        "url": url,
                        "text": text_chunk,
                        "type": "post"
                    })
                    
    # 3. Parse Newsletters
    if os.path.isdir(NEWSLETTERS_DIR):
        for file in os.listdir(NEWSLETTERS_DIR):
            if file.endswith((".md", ".html")):
                path = os.path.join(NEWSLETTERS_DIR, file)
                title, url, layout, raw = parse_front_matter(path)
                clean_txt = clean_content(raw)
                if not clean_txt:
                    continue
                
                if not url:
                    name_slug = os.path.splitext(file)[0]
                    url = f"/newsletter/{name_slug}/"
                    
                for text_chunk in chunk_text(clean_txt):
                    chunks.append({
                        "title": title,
                        "url": url,
                        "text": text_chunk,
                        "type": "newsletter"
                    })

    # 4. Parse YAML Databases (Research, Talks, Defenses)
    # 4.1 Research publications
    research_path = os.path.join(DATA_DIR, "research.yml")
    if os.path.isfile(research_path):
        with open(research_path, "r", encoding="utf-8") as f:
            papers = yaml.safe_load(f) or []
        for paper in papers:
            title = paper.get("title", "Publication")
            authors = paper.get("authors", "")
            venue = paper.get("venue", "")
            date = paper.get("date", "")
            abstract = paper.get("abstract", "")
            keywords = ", ".join(paper.get("keywords", []))
            
            # Format text representation
            text = f"Research Publication: '{title}' published in {venue} ({date}) by {authors}."
            if abstract:
                text += f" Abstract: {abstract}"
            if keywords:
                text += f" Keywords: {keywords}"
                
            chunks.append({
                "title": title,
                "url": "/research/",
                "text": text,
                "type": "publication"
            })
            
    # 4.2 Talks
    talks_path = os.path.join(DATA_DIR, "talks.yml")
    if os.path.isfile(talks_path):
        with open(talks_path, "r", encoding="utf-8") as f:
            talks = yaml.safe_load(f) or []
        for talk in talks:
            title = talk.get("title", "Presentation")
            venue = talk.get("venue", "")
            date = talk.get("date", "")
            abstract = talk.get("abstract", "")
            
            text = f"Presentation/Talk: '{title}' presented at {venue} ({date})."
            if abstract:
                text += f" Abstract: {abstract}"
                
            chunks.append({
                "title": title,
                "url": "/research/",
                "text": text,
                "type": "talk"
            })
            
    # 4.3 Defenses
    defense_path = os.path.join(DATA_DIR, "defense.yml")
    if os.path.isfile(defense_path):
        with open(defense_path, "r", encoding="utf-8") as f:
            defenses = yaml.safe_load(f) or []
        for df in defenses:
            title = df.get("title", "Academic Milestone")
            venue = df.get("venue", "")
            date = df.get("date", "")
            abstract = df.get("abstract", "")
            
            text = f"PhD Academic Defense/Proposal: '{title}' presented at {venue} ({date})."
            if abstract:
                text += f" Abstract: {abstract}"
                
            chunks.append({
                "title": title,
                "url": "/research/",
                "text": text,
                "type": "milestone"
            })

    # 4.4 YouTube Transcripts
    youtube_path = os.path.join(DATA_DIR, "youtube_transcripts.json")
    if os.path.isfile(youtube_path):
        with open(youtube_path, "r", encoding="utf-8") as f:
            transcripts = json.load(f) or []
        for vt in transcripts:
            title = vt.get("title", "")
            url = vt.get("url", "")
            transcript_text = vt.get("transcript", "")
            original_type = vt.get("original_type", "")
            
            # Segment the transcript into chunks of ~120 words
            sub_chunks = chunk_text(transcript_text, max_words=120)
            for i, text_chunk in enumerate(sub_chunks):
                # The text is prefixed with context to help keyword matching and LLM understanding.
                chunk_text_representation = f"YouTube Video Transcript for '{title}': {text_chunk}"
                chunks.append({
                    "title": f"Transcript: {title} (Part {i+1})",
                    "url": url,
                    "text": chunk_text_representation,
                    "type": "youtube_transcript",
                    "original_type": original_type
                })

    # 4.5 Georgia Tech OMSCS Machine Learning (CS 7641) Course Content
    course_path = os.path.join(DATA_DIR, "omscs7641_content.json")
    if os.path.isfile(course_path):
        with open(course_path, "r", encoding="utf-8") as f:
            course_items = json.load(f) or []
        for item in course_items:
            title = item.get("title", "")
            url = item.get("url", "")
            content_html = item.get("content_html", "")
            author = item.get("author", "")
            date = item.get("date", "")
            item_type = item.get("type", "omscs7641_post")
            
            clean_txt = clean_content(content_html)
            if not clean_txt:
                continue
                
            formatted_date = date.split("T")[0] if "T" in date else date
            metadata_prefix = f"Georgia Tech OMSCS CS 7641 Machine Learning course site article: '{title}' written by {author} on {formatted_date}."
            
            sub_chunks = chunk_text(clean_txt, max_words=120)
            for text_chunk in sub_chunks:
                chunk_text_representation = f"{metadata_prefix} {text_chunk}"
                chunks.append({
                    "title": title,
                    "url": url,
                    "text": chunk_text_representation,
                    "type": item_type
                })

    print(f"Extracted {len(chunks)} total text chunks for embedding.")
    return chunks

def main():
    print("Step 1: Extracting text chunks from Jekyll markdown/html files and databases...")
    chunks = extract_chunks()
    
    if not chunks:
        print("No chunks found. Aborting.")
        return
        
    print("\nStep 2: Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
    # Import here to avoid slow loading if errors occur above
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("\nStep 3: Generating dense vector embeddings...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print("\nStep 4: Compiling and saving database...")
    embeddings_list = embeddings.tolist()
    
    output_data = []
    for chunk, emb in zip(chunks, embeddings_list):
        item = {
            "title": chunk["title"],
            "url": chunk["url"],
            "text": chunk["text"],
            "type": chunk["type"],
            "embedding": emb
        }
        if "original_type" in chunk:
            item["original_type"] = chunk["original_type"]
        output_data.append(item)
        
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"Success! Generated vector database file at: {OUTPUT_FILE}")
    print(f"Total file size: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
