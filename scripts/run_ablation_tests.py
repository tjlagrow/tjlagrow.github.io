import os
import re
import json
import time
import math
import collections
import numpy as np
import yaml
import html
import matplotlib.pyplot as plt
import torch

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES_DIR = os.path.join(PROJECT_ROOT, "_pages")
POSTS_DIR = os.path.join(PROJECT_ROOT, "_posts")
NEWSLETTERS_DIR = os.path.join(PROJECT_ROOT, "_newsletters")
DATA_DIR = os.path.join(PROJECT_ROOT, "_data")
EMBEDDINGS_FILE = os.path.join(PROJECT_ROOT, "assets", "json", "embeddings.json")
QUERIES_FILE = os.path.join(PROJECT_ROOT, "scripts", "ablation_queries.json")
CHECKPOINT_FILE = os.path.join(PROJECT_ROOT, "scripts", "ablation_checkpoint.json")
RESULTS_FILE = os.path.join(PROJECT_ROOT, "artifacts", "ablation_results.json")
IMAGE_OUT_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "ablation")

# Ensure directories exist
os.makedirs(IMAGE_OUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

# Load Persona Examples from persona_examples.json for Persona Testing
PERSONA_EXAMPLES_FILE = os.path.join(PROJECT_ROOT, "scripts", "persona_examples.json")
if os.path.exists(PERSONA_EXAMPLES_FILE):
    with open(PERSONA_EXAMPLES_FILE, "r", encoding="utf-8") as f:
        PERSONA_EXAMPLES = json.load(f)
else:
    PERSONA_EXAMPLES = []

VISUAL_ASSETS = [
    {
        "title": "Alzheimer's Disease Brain Connectivity Header",
        "url": "/assets/images/alzheimers_header.png",
        "text": "Alzheimer's Disease analysis and brain network connectivity map. Shows functional connectivity graph decomposition and Solenoidal and Curl decomposition regimes of resting-state fMRI activity. Details Helmholtz-Hodge decomposition pipelines.",
        "type": "visual_asset"
    },
    {
        "title": "Cross-Species Brain Graph Topology Header",
        "url": "/assets/images/cross_species_header.png",
        "text": "Cross-species comparative brain graph topology and alignment mappings. Visualizes resting-state functional MRI alignment protocols between different mammalian cohorts and evolutionary conservation metrics.",
        "type": "visual_asset"
    },
    {
        "title": "Backward Design Education Paradigm Header",
        "url": "/assets/images/education_header.png",
        "text": "Backward Design educational paradigm diagram. Illustrates backward design mapping: starting from learning outcomes and assessments, then aligning learning activities and curriculum rubrics, grounding teaching in evidence-based learning science.",
        "type": "visual_asset"
    },
    {
        "title": "Ramon y Cajal Brain Tissue Sketch",
        "url": "/assets/images/ramon_y_cajal.png",
        "text": "Santiago Ramon y Cajal historical illustration of brain tissue neural structures, historical brain slice neurons, pyramidal cells, and cortical layers. Classic neurobiology sketch.",
        "type": "visual_asset"
    },
    {
        "title": "Ramon y Cajal Histology Retinal Drawing",
        "url": "/assets/images/ramon_y_cajal_3.png",
        "text": "Santiago Ramon y Cajal neuroanatomy histology drawing of retinal cell connections, rods, cones, bipolar cells, and optic nerve synapses. Historical neuroscience cell architecture.",
        "type": "visual_asset"
    },
    {
        "title": "Static and Dynamic Web Assembly Optimizations Header",
        "url": "/assets/images/static_dynamic_header.png",
        "text": "Static hosting and browser-side WebAssembly execution optimization overview. Visualizes single-threaded WASM fallback, dynamic CDN weight retrieval, and HTTP persistent caching storage pipelines.",
        "type": "visual_asset"
    },
    {
        "title": "Waddles AI Avatar Truffle Pig Mascot",
        "url": "/assets/images/waddles_ai_avatar.png",
        "text": "Waddles RAG search assistant avatar, truffle pig minimalist flat-vector mascot illustration. Pulses and tilts with dynamic mouse-move orbital interactive tech rings.",
        "type": "visual_asset"
    }
]

# Simple BM25 Indexer
class SimpleBM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(docs)
        self.avg_doc_len = 0.0
        self.doc_freqs = []
        self.doc_lens = []
        self.idf = {}
        
        def tokenize(text):
            return re.findall(r'\w+', text.lower())

        total_words = 0
        for doc in docs:
            words = tokenize(doc)
            self.doc_lens.append(len(words))
            total_words += len(words)
            freqs = collections.Counter(words)
            self.doc_freqs.append(freqs)
            
            for word in freqs:
                self.idf[word] = self.idf.get(word, 0) + 1
                
        self.avg_doc_len = total_words / max(self.corpus_size, 1)
        for word, count in self.idf.items():
            self.idf[word] = math.log((self.corpus_size - count + 0.5) / (count + 0.5) + 1.0)
            
    def get_scores(self, query):
        def tokenize(text):
            return re.findall(r'\w+', text.lower())
        query_words = tokenize(query)
        scores = np.zeros(self.corpus_size)
        for idx in range(self.corpus_size):
            doc_len = self.doc_lens[idx]
            freqs = self.doc_freqs[idx]
            score = 0.0
            for word in query_words:
                if word in freqs:
                    f = freqs[word]
                    word_idf = self.idf.get(word, 0.0)
                    numerator = f * (self.k1 + 1)
                    denominator = f + self.k1 * (1 - self.b + self.b * doc_len / max(self.avg_doc_len, 1))
                    score += word_idf * (numerator / denominator)
            scores[idx] = score
        return scores


# Word-based longest common subsequence (LCS) for ROUGE-L
def compute_lcs(x, y):
    n, m = len(x), len(y)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[n][m]


def calculate_rouge_l_recall(candidate, reference):
    c_words = re.findall(r'\w+', candidate.lower())
    r_words = re.findall(r'\w+', reference.lower())
    if not r_words:
        return 0.0
    lcs_len = compute_lcs(c_words, r_words)
    return lcs_len / len(r_words)


def calculate_ttr(answer):
    words = re.findall(r'\b\w+\b', answer.lower())
    if not words:
        return 1.0
    return len(set(words)) / len(words)


def calculate_groundedness(answer, context):
    stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "by", "for", "with", "about", "that", "this", "these", "those"}
    ans_words = set(re.findall(r'\b\w{3,}\b', answer.lower()))
    ctx_words = set(re.findall(r'\b\w{3,}\b', context.lower()))
    ans_content_words = ans_words - stopwords
    if not ans_content_words:
        return 1.0
    overlap = ans_content_words.intersection(ctx_words)
    return len(overlap) / len(ans_content_words)


def calculate_citation_fidelity(answer, context):
    ans_urls = set(re.findall(r'https?://[^\s"\'}]+', answer))
    if not ans_urls:
        return 1.0
    ctx_urls = set(re.findall(r'https?://[^\s"\'}]+', context))
    overlap = ans_urls.intersection(ctx_urls)
    return len(overlap) / len(ans_urls)


def calculate_hallucination_ratio(answer, context, query):
    stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "by", "for", "with", "about", "that", "this", "these", "those"}
    ans_words = set(re.findall(r'\b\w{3,}\b', answer.lower())) - stopwords
    ctx_words = set(re.findall(r'\b\w{3,}\b', context.lower()))
    q_words = set(re.findall(r'\b\w{3,}\b', query.lower()))
    if not ans_words:
        return 0.0
    extraneous = ans_words - ctx_words - q_words
    return len(extraneous) / len(ans_words)


def calculate_verbosity_ratio(answer, reference):
    if not reference:
        return 1.0
    return len(answer) / len(reference)


def calculate_structure_fidelity(ans_text):
    txt = ans_text.strip()
    if not (txt.startswith('{') and txt.endswith('}')):
        return 0.0
    try:
        parsed = json.loads(txt)
        if isinstance(parsed, dict) and "answer" in parsed:
            if len(parsed) == 1:
                return 1.0
            return 0.5
        return 0.0
    except Exception:
        return 0.0




# Query Normalization Helpers
def preprocess_query(query, synonyms_enabled=True, length_filter_enabled=True):
    clean = query.strip()
    if not clean:
        return ""
    clean = clean.replace("??", "?").replace("!!", "!")
    clean = re.sub(r'\s+', ' ', clean)
    if length_filter_enabled:
        words = clean.split()
        if len(words) > 20:
            sentences = re.split(r'(?<=[.!?])\s+', clean)
            if len(sentences) >= 2:
                clean = sentences[0] + " " + sentences[-1]
    if synonyms_enabled:
        mappings = {
            r"\bml\b": "CS 7641 Machine Learning",
            r"\brl\b": "CS 7642 Reinforcement Learning",
            r"\bqpps?\b": "Quasi-Periodic Patterns",
            r"\bfmri\b": "resting-state fMRI",
            r"\bmind lab\b": "Keilholz MIND Lab",
            r"\bclasses\b": "courses",
            r"\bemail\b": "contact details"
        }
        for pattern, replacement in mappings.items():
            clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
    return clean


def doc_passes_intent(doc, intent):
    effective_type = doc.get("original_type") or doc.get("type")
    url = doc.get("url", "")
    if intent == "Teaching":
        return "/teaching" in url or effective_type in ["milestone", "omscs7641_post", "omscs7641_page"]
    elif intent == "Research":
        return effective_type in ["publication", "talk"]
    else:
        is_teaching = "/teaching" in url or effective_type in ["milestone", "omscs7641_post", "omscs7641_page"]
        is_research = effective_type in ["publication", "talk"]
        return not (is_teaching or is_research)


# Evaluation Metrics Calculators
def calculate_retrieval_metrics(retrieved_titles, ground_truth_titles, top_k=5):
    hit_at_3 = 0
    hit_at_5 = 0
    mrr = 0.0
    dcg = 0.0
    for rank, title in enumerate(retrieved_titles[:top_k]):
        if title in ground_truth_titles:
            hit_at_5 = 1
            if rank < 3:
                hit_at_3 = 1
            if mrr == 0.0:
                mrr = 1.0 / (rank + 1)
            dcg += 1.0 / math.log2(rank + 2)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(min(top_k, len(ground_truth_titles))))
    ndcg = (dcg / idcg) if idcg > 0 else 0.0
    return hit_at_3, hit_at_5, mrr, ndcg


# Text Extraction Pipeline helpers
def clean_content(content):
    content = html.unescape(content)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
    content = re.sub(r'\{%.*?%\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\{\{.*?\}\}', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<script.*?>.*?</script>', ' ', content, flags=re.DOTALL)
    content = re.sub(r'<style.*?>.*?</style>', ' ', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    content = re.sub(r'#+\s+', '', content)
    content = re.sub(r'[*_`~]', '', content)
    content = re.sub(r'-\s+', '', content)
    return re.sub(r'\s+', ' ', content).strip()


def chunk_text(text, max_words=120):
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
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    title = os.path.basename(file_path)
    url, layout = None, "page"
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                if meta:
                    title = meta.get("title", title)
                    url = meta.get("permalink", url)
                    layout = meta.get("layout", layout)
            except Exception:
                pass
    return title, url, layout, raw


def get_post_url(filename, categories):
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|html)$', filename)
    if not m:
        return f"/posts/{filename}"
    year, month, day, slug = m.groups()[:4]
    cats = []
    if categories:
        if isinstance(categories, list):
            cats = categories
        elif isinstance(categories, str):
            cats = categories.split()
    cat_path = "/".join(cats)
    return f"/{cat_path}/{year}/{month}/{day}/{slug}/" if cat_path else f"/{year}/{month}/{day}/{slug}/"


def extract_parent_child_chunks(clean_txt, max_words_parent, max_words_child, metadata_prefix=""):
    parents = chunk_text(clean_txt, max_words=max_words_parent)
    sub_chunks = []
    for parent in parents:
        children = chunk_text(parent, max_words=max_words_child)
        for child in children:
            child_text = f"{metadata_prefix} {child}".strip() if metadata_prefix else child.strip()
            parent_text = f"{metadata_prefix} {parent}".strip() if metadata_prefix else parent.strip()
            sub_chunks.append({"text": child_text, "parent_text": parent_text})
    return sub_chunks


def run_dynamic_rechunking(max_parent, max_child, embed_model):
    """Re-chunks the site markdown files on the fly and generates new embeddings."""
    cache_file = os.path.join(PROJECT_ROOT, "scripts", f"embeddings_cache_{max_child}_{max_parent}.json")
    if os.path.exists(cache_file):
        print(f"Loading re-chunking cache from {cache_file}...")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
            
    print(f"Re-chunking documents on-the-fly (Child: {max_child} words, Parent: {max_parent} words)...")
    chunks = []
    
    # 1. Parse Pages
    if os.path.isdir(PAGES_DIR):
        for root, _, files in os.walk(PAGES_DIR):
            for file in files:
                if file.endswith((".html", ".md")):
                    path = os.path.join(root, file)
                    title, url, layout, raw = parse_front_matter(path)
                    if "waddles" in file.lower() or "search.json" in file.lower() or "feed.xml" in file.lower():
                        continue
                    clean_txt = clean_content(raw)
                    if not clean_txt: continue
                    if not url:
                        url = f"/{os.path.splitext(file)[0]}/"
                    for item in extract_parent_child_chunks(clean_txt, max_parent, max_child):
                        chunks.append({
                            "title": title, "url": url, "text": item["text"],
                            "parent_text": item["parent_text"], "type": "page"
                        })
                        
    # 2. Parse Posts
    if os.path.isdir(POSTS_DIR):
        for file in os.listdir(POSTS_DIR):
            if file.endswith((".md", ".html")):
                path = os.path.join(POSTS_DIR, file)
                title, url, layout, raw = parse_front_matter(path)
                clean_txt = clean_content(raw)
                if not clean_txt: continue
                categories = None
                if raw.startswith("---"):
                    parts = raw.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            meta = yaml.safe_load(parts[1])
                            if meta: categories = meta.get("categories")
                        except Exception: pass
                url = get_post_url(file, categories)
                for item in extract_parent_child_chunks(clean_txt, max_parent, max_child):
                    chunks.append({
                        "title": title, "url": url, "text": item["text"],
                        "parent_text": item["parent_text"], "type": "post"
                    })

    # 3. Parse Newsletters
    if os.path.isdir(NEWSLETTERS_DIR):
        for file in os.listdir(NEWSLETTERS_DIR):
            if file.endswith((".md", ".html")):
                path = os.path.join(NEWSLETTERS_DIR, file)
                title, url, layout, raw = parse_front_matter(path)
                clean_txt = clean_content(raw)
                if not clean_txt: continue
                if not url:
                    url = f"/newsletter/{os.path.splitext(file)[0]}/"
                for item in extract_parent_child_chunks(clean_txt, max_parent, max_child):
                    chunks.append({
                        "title": title, "url": url, "text": item["text"],
                        "parent_text": item["parent_text"], "type": "newsletter"
                    })

    # 4. Parse YAML Databases
    research_path = os.path.join(DATA_DIR, "research.yml")
    if os.path.isfile(research_path):
        with open(research_path, "r", encoding="utf-8") as f:
            papers = yaml.safe_load(f) or []
        for paper in papers:
            title = paper.get("title", "Publication")
            authors, venue, date = paper.get("authors", ""), paper.get("venue", ""), paper.get("date", "")
            abstract, keywords = paper.get("abstract", ""), ", ".join(paper.get("keywords", []))
            text = f"Research Publication: '{title}' published in {venue} ({date}) by {authors}."
            if abstract: text += f" Abstract: {abstract}"
            if keywords: text += f" Keywords: {keywords}"
            chunks.append({"title": title, "url": "/research/", "text": text, "parent_text": text, "type": "publication"})
            
    # Talks
    talks_path = os.path.join(DATA_DIR, "talks.yml")
    if os.path.isfile(talks_path):
        with open(talks_path, "r", encoding="utf-8") as f:
            talks = yaml.safe_load(f) or []
        for talk in talks:
            title, venue, date, abstract = talk.get("title", "Presentation"), talk.get("venue", ""), talk.get("date", ""), talk.get("abstract", "")
            text = f"Presentation/Talk: '{title}' presented at {venue} ({date})."
            if abstract: text += f" Abstract: {abstract}"
            chunks.append({"title": title, "url": "/research/", "text": text, "parent_text": text, "type": "talk"})

    # Defenses
    defense_path = os.path.join(DATA_DIR, "defense.yml")
    if os.path.isfile(defense_path):
        with open(defense_path, "r", encoding="utf-8") as f:
            defenses = yaml.safe_load(f) or []
        for df in defenses:
            title, venue, date, abstract = df.get("title", "Academic Milestone"), df.get("venue", ""), df.get("date", ""), df.get("abstract", "")
            text = f"PhD Academic Defense/Proposal: '{title}' presented at {venue} ({date})."
            if abstract: text += f" Abstract: {abstract}"
            chunks.append({"title": title, "url": "/research/", "text": text, "parent_text": text, "type": "milestone"})

    # Youtube Transcripts
    youtube_path = os.path.join(DATA_DIR, "youtube_transcripts.json")
    if os.path.isfile(youtube_path):
        with open(youtube_path, "r", encoding="utf-8") as f:
            transcripts = json.load(f) or []
        for vt in transcripts:
            title, url, transcript_text, original_type = vt.get("title", ""), vt.get("url", ""), vt.get("transcript", ""), vt.get("original_type", "")
            child_items = extract_parent_child_chunks(transcript_text, max_parent, max_child, metadata_prefix=f"YouTube Video Transcript for '{title}':")
            for i, item in enumerate(child_items):
                chunks.append({
                    "title": f"Transcript: {title} (Part {i+1})", "url": url, "text": item["text"],
                    "parent_text": item["parent_text"], "type": "youtube_transcript", "original_type": original_type
                })

    # Georgia Tech OMSCS Course Content
    course_path = os.path.join(DATA_DIR, "omscs7641_content.json")
    if os.path.isfile(course_path):
        with open(course_path, "r", encoding="utf-8") as f:
            course_items = json.load(f) or []
        for item in course_items:
            title, url, content_html = item.get("title", ""), item.get("url", ""), item.get("content_html", "")
            author, date, item_type = item.get("author", ""), item.get("date", ""), item.get("type", "omscs7641_post")
            clean_txt = clean_content(content_html)
            if not clean_txt: continue
            formatted_date = date.split("T")[0] if "T" in date else date
            metadata_prefix = f"Georgia Tech OMSCS CS 7641 Machine Learning course site article: '{title}' written by {author} on {formatted_date}."
            child_items = extract_parent_child_chunks(clean_txt, max_parent, max_child, metadata_prefix=metadata_prefix)
            for item in child_items:
                chunks.append({
                    "title": title, "url": url, "text": item["text"],
                    "parent_text": item["parent_text"], "type": item_type
                })

    # Visual Assets
    for asset in VISUAL_ASSETS:
        chunks.append({
            "title": asset["title"], "url": asset["url"], "text": asset["text"],
            "parent_text": asset["text"], "type": asset["type"]
        })

    # Compute dense embeddings in batch
    texts = [c["text"] for c in chunks]
    embeddings = embed_model.encode(texts, show_progress_bar=False).tolist()
    
    for i, emb in enumerate(embeddings):
        chunks[i]["embedding"] = emb
        
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
        
    return chunks


# Quantization Simulators
def run_quantization_sim(emb, method="int8"):
    v = np.array(emb)
    if method == "int8":
        # Scale to [-127, 127]
        max_val = np.max(np.abs(v))
        if max_val == 0:
            return v.astype(np.int8).tolist()
        scaled = v * (127.0 / max_val)
        return np.round(scaled).astype(np.int8).tolist()
    elif method == "binary":
        # Sign projection
        return np.sign(v).astype(np.int8).tolist()
    return emb


# Model Loader Helper (with robust fallbacks)
def load_hf_generator(model_id, fallback_id=None):
    import torch
    from transformers import pipeline
    
    use_auth = "meta-llama" in model_id and "unsloth" not in model_id
    token = os.environ.get("HF_TOKEN")
    
    print(f"Attempting to load pipeline for: {model_id}")
    try:
        if use_auth and not token:
            raise ValueError("Missing HF_TOKEN environment variable required for Llama models.")
        
        is_large = any(x in model_id.lower() for x in ["7b", "8b", "70b"])
        
        kwargs = {
            "token": token if use_auth else None
        }
        if torch.cuda.is_available() and not is_large:
            kwargs["torch_dtype"] = torch.float16
            kwargs["device_map"] = "auto"
        else:
            kwargs["device"] = -1
            kwargs["torch_dtype"] = torch.float32  # CPU is more efficient and standard with float32
            
        pipe = pipeline(
            "text-generation",
            model=model_id,
            **kwargs
        )
        return pipe
    except Exception as e:
        print(f"Hugging Face load failed for {model_id}: {e}")
        if fallback_id:
            print(f"Trying fallback model: {fallback_id}")
            try:
                is_large_fb = any(x in fallback_id.lower() for x in ["7b", "8b", "70b"])
                fallback_kwargs = {
                    "token": token if use_auth else None
                }
                if torch.cuda.is_available() and not is_large_fb:
                    fallback_kwargs["torch_dtype"] = torch.float16
                    fallback_kwargs["device_map"] = "auto"
                else:
                    fallback_kwargs["device"] = -1
                    fallback_kwargs["torch_dtype"] = torch.float32
                pipe = pipeline(
                    "text-generation",
                    model=fallback_id,
                    **fallback_kwargs
                )
                return pipe
            except Exception as fe:
                print(f"Fallback model failed to load: {fe}")
        return None


def main():
    print(f"Loading query database from {QUERIES_FILE}...")
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        queries_data = json.load(f)
        
    print("Initializing local embedding and re-ranking models...")
    from sentence_transformers import SentenceTransformer, CrossEncoder
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    reranker_model = CrossEncoder("ms-marco-MiniLM-L-6-v2")
    
    # Load or generate baseline (Ratio B) database
    db_items = run_dynamic_rechunking(200, 50, embed_model)
    doc_embeddings = np.array([item["embedding"] for item in db_items])
    corpus = [item["text"] for item in db_items]
    bm25 = SimpleBM25(corpus)
    
    # Initialize results
    ablation_results = {}
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                ablation_results = json.load(f)
            print(f"Resumed checkpoint. Loaded results for {len(ablation_results)} categories.")
        except Exception:
            pass

    # ABLATION PHASE 1: Retrieval Parameters
    if "Phase 1: Retrieval Parameters" not in ablation_results:
        print("\n--- Running Phase 1: Retrieval Parameters Ablation ---")
        phase1_results = {}
        
        # 1. Chunking Ratios
        ratios = {
            "Ratio A (Child 30 / Parent 150)": (150, 30),
            "Ratio B (Child 50 / Parent 200)": (200, 50),
            "Ratio C (Child 100 / Parent 500)": (500, 100)
        }
        for name, (p_words, c_words) in ratios.items():
            run_db = run_dynamic_rechunking(p_words, c_words, embed_model)
            run_corpus = [node["text"] for node in run_db]
            run_bm25 = SimpleBM25(run_corpus)
            run_embs = np.array([node["embedding"] for node in run_db])
            
            mrr_sum = 0.0
            hit3_sum = 0.0
            for q_idx, q_item in enumerate(queries_data):
                q = q_item["query"]
                gt = q_item["ground_truth_document_titles"]
                
                # Hybrid RRF (k=60)
                q_vec = embed_model.encode(q, show_progress_bar=False)
                dense_dots = np.dot(run_embs / np.linalg.norm(run_embs, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                sparse_scores = run_bm25.get_scores(q)
                
                dense_ranks = np.argsort(-dense_dots)
                sparse_ranks = np.argsort(-sparse_scores)
                
                dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                
                rrf_scores = {}
                for idx in range(len(run_db)):
                    rrf_scores[idx] = 1.0 / (60 + dense_rank_map[idx]) + 1.0 / (60 + sparse_rank_map[idx])
                
                sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                retrieved_titles = [run_db[idx]["title"] for idx, score in sorted_rrf[:5]]
                _, h3, mrr, _ = calculate_retrieval_metrics(retrieved_titles, gt, top_k=5)
                mrr_sum += mrr
                hit3_sum += h3
                
                print(f"    [Ratio {name}] Query {q_idx + 1}/{len(queries_data)}: '{q[:40]}...' | Hit@3: {h3}, MRR: {mrr:.4f} | Retrieved: {retrieved_titles} | Ground Truth: {gt}")
                
            phase1_results[f"chunk_{name}"] = {
                "hit_at_3": hit3_sum / len(queries_data),
                "mrr": mrr_sum / len(queries_data)
            }
            print(f"  {name} - Hit@3: {phase1_results[f'chunk_{name}']['hit_at_3']:.2%}, MRR: {phase1_results[f'chunk_{name}']['mrr']:.4f}")
            
        # 2. Retrieve Count (K)
        for K in [2, 3, 5, 8]:
            mrr_sum = 0.0
            hit3_sum = 0.0
            for q_idx, q_item in enumerate(queries_data):
                q = q_item["query"]
                gt = q_item["ground_truth_document_titles"]
                
                q_vec = embed_model.encode(q, show_progress_bar=False)
                dense_dots = np.dot(doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                sparse_scores = bm25.get_scores(q)
                
                dense_ranks = np.argsort(-dense_dots)
                sparse_ranks = np.argsort(-sparse_scores)
                dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                
                rrf_scores = {}
                for idx in range(len(db_items)):
                    rrf_scores[idx] = 1.0 / (60 + dense_rank_map[idx]) + 1.0 / (60 + sparse_rank_map[idx])
                
                sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                retrieved_titles = [db_items[idx]["title"] for idx, score in sorted_rrf[:K]]
                _, h3, mrr, _ = calculate_retrieval_metrics(retrieved_titles, gt, top_k=K)
                mrr_sum += mrr
                hit3_sum += h3
                
                print(f"    [K={K}] Query {q_idx + 1}/{len(queries_data)}: '{q[:40]}...' | Hit@3: {h3}, MRR: {mrr:.4f} | Retrieved: {retrieved_titles} | Ground Truth: {gt}")
                
            phase1_results[f"ret_K_{K}"] = {
                "hit_at_3": hit3_sum / len(queries_data),
                "mrr": mrr_sum / len(queries_data)
            }
            print(f"  K={K} - Hit@3: {phase1_results[f'ret_K_{K}']['hit_at_3']:.2%}, MRR: {phase1_results[f'ret_K_{K}']['mrr']:.4f}")

        # 3. Weighted Fusion
        weights = [0.2, 0.5, 0.8]
        for w in weights:
            mrr_sum = 0.0
            hit3_sum = 0.0
            for q_idx, q_item in enumerate(queries_data):
                q = q_item["query"]
                gt = q_item["ground_truth_document_titles"]
                
                q_vec = embed_model.encode(q, show_progress_bar=False)
                dense_dots = np.dot(doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                sparse_scores = bm25.get_scores(q)
                
                dense_ranks = np.argsort(-dense_dots)
                sparse_ranks = np.argsort(-sparse_scores)
                dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                
                rrf_scores = {}
                for idx in range(len(db_items)):
                    rrf_scores[idx] = w * (1.0 / (60 + dense_rank_map[idx])) + (1.0 - w) * (1.0 / (60 + sparse_rank_map[idx]))
                
                sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                retrieved_titles = [db_items[idx]["title"] for idx, score in sorted_rrf[:3]]
                _, h3, mrr, _ = calculate_retrieval_metrics(retrieved_titles, gt, top_k=3)
                mrr_sum += mrr
                hit3_sum += h3
                
                print(f"    [W_dense={w:.1f}] Query {q_idx + 1}/{len(queries_data)}: '{q[:40]}...' | Hit@3: {h3}, MRR: {mrr:.4f} | Retrieved: {retrieved_titles} | Ground Truth: {gt}")
                
            phase1_results[f"weight_dense_{w:.1f}"] = {
                "hit_at_3": hit3_sum / len(queries_data),
                "mrr": mrr_sum / len(queries_data)
            }
            print(f"  W_dense={w:.1f} - Hit@3: {phase1_results[f'weight_dense_{w:.1f}']['hit_at_3']:.2%}, MRR: {phase1_results[f'weight_dense_{w:.1f}']['mrr']:.4f}")

        # 4. Quantization
        quants = ["float32", "int8", "binary"]
        for q_type in quants:
            mrr_sum = 0.0
            hit3_sum = 0.0
            
            # Simulate database quantization
            quant_embs = []
            for item in db_items:
                quant_embs.append(run_quantization_sim(item["embedding"], q_type))
            quant_embs = np.array(quant_embs)
            
            for q_idx, q_item in enumerate(queries_data):
                q = q_item["query"]
                gt = q_item["ground_truth_document_titles"]
                
                # Quantize query
                raw_q_vec = embed_model.encode(q, show_progress_bar=False)
                q_vec = run_quantization_sim(raw_q_vec, q_type)
                
                # Retrieve dense
                if q_type == "binary":
                    # Dot product of binary vectors matches bitwise hamming equivalent
                    dense_dots = np.dot(quant_embs, q_vec)
                else:
                    dense_dots = np.dot(quant_embs / np.linalg.norm(quant_embs, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                    
                sparse_scores = bm25.get_scores(q)
                
                dense_ranks = np.argsort(-dense_dots)
                sparse_ranks = np.argsort(-sparse_scores)
                dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                
                rrf_scores = {}
                for idx in range(len(db_items)):
                    rrf_scores[idx] = 1.0 / (60 + dense_rank_map[idx]) + 1.0 / (60 + sparse_rank_map[idx])
                
                sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                retrieved_titles = [db_items[idx]["title"] for idx, score in sorted_rrf[:3]]
                _, h3, mrr, _ = calculate_retrieval_metrics(retrieved_titles, gt, top_k=3)
                mrr_sum += mrr
                hit3_sum += h3
                
                print(f"    [Quant={q_type}] Query {q_idx + 1}/{len(queries_data)}: '{q[:40]}...' | Hit@3: {h3}, MRR: {mrr:.4f} | Retrieved: {retrieved_titles} | Ground Truth: {gt}")
                
            phase1_results[f"quant_{q_type}"] = {
                "hit_at_3": hit3_sum / len(queries_data),
                "mrr": mrr_sum / len(queries_data)
            }
            print(f"  Quant: {q_type} - Hit@3: {phase1_results[f'quant_{q_type}']['hit_at_3']:.2%}, MRR: {phase1_results[f'quant_{q_type}']['mrr']:.4f}")

        ablation_results["Phase 1: Retrieval Parameters"] = phase1_results
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(ablation_results, f, indent=2)
        print("Phase 1 retrieval sweeps finished. Generating partial plots...")
        try:
            generate_expanded_plots(ablation_results)
        except Exception as pe:
            print(f"Failed to generate plots: {pe}")

    # Core subset of 5 queries for slow LLM benchmarks
    core_queries = [queries_data[0], queries_data[4], queries_data[8], queries_data[11], queries_data[13]]

    # ABLATION PHASE 2: Local Generator Comparison (Browser vs. Baselines)
    if "Phase 2: Generator Model Comparison" not in ablation_results:
        print("\n--- Running Phase 2: Generator Model Comparison ---")
        phase2_results = {}
        
        # Load baseline configurations using unsloth public models to avoid gating
        models_to_test = {
            "SmolLM-135M": ("HuggingFaceTB/SmolLM-135M-Instruct", None),
            "SmolLM2-360M": ("HuggingFaceTB/SmolLM2-360M-Instruct", None),
            "Qwen2.5-0.5B": ("Qwen/Qwen2.5-0.5B-Instruct", None),
            "Llama-3.2-1B": ("unsloth/Llama-3.2-1B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct"),
            "Llama-3.2-3B": ("unsloth/Llama-3.2-3B-Instruct", "Qwen/Qwen2.5-3B-Instruct"),
            "Llama-3-8B": ("unsloth/llama-3-8b-Instruct", "Qwen/Qwen2.5-7B-Instruct")
        }
        
        for name, (model_id, fallback_id) in models_to_test.items():
            print(f"\n[Phase 2] Loading model {name} ({model_id})...")
            t_load_start = time.perf_counter()
            pipe = load_hf_generator(model_id, fallback_id)
            t_load_end = time.perf_counter()
            if not pipe:
                print(f"Skipping model {name} (failed to load).")
                continue
            print(f"[Phase 2] Model {name} loaded successfully in {t_load_end - t_load_start:.2f}s.")
                
            rouge_sum = 0.0
            sem_sim_sum = 0.0
            char_len_sum = 0.0
            latency_sum = 0.0
            ttr_sum = 0.0
            groundedness_sum = 0.0
            citation_fidelity_sum = 0.0
            hallucination_sum = 0.0
            verbosity_sum = 0.0
            structure_sum = 0.0
            
            num_q = len(core_queries)
            for q_idx, q_item in enumerate(core_queries):
                query_str = q_item["query"]
                intent = q_item["intent"]
                ref_ans = q_item["ground_truth_answer"]
                
                print(f"  -> [Query {q_idx+1}/{num_q}] Running query: '{query_str}' (Intent: {intent})")
                print(f"       [RAG] Initiating retrieval flow...")
                
                # Fetch RAG Context (Ratio B, Hybrid RRF k=60, Pre-filtering, Rerank)
                t_rag_start = time.perf_counter()
                q_vec = embed_model.encode(query_str, show_progress_bar=False)
                
                # Apply intent pre-filtering
                valid_indices = [i for i, node in enumerate(db_items) if doc_passes_intent(node, intent)]
                if not valid_indices: valid_indices = list(range(len(db_items)))
                
                dense_dots = np.dot(doc_embeddings[valid_indices] / np.linalg.norm(doc_embeddings[valid_indices], axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                
                # BM25 scores
                doc_texts = [db_items[i]["text"] for i in valid_indices]
                v_bm25 = SimpleBM25(doc_texts)
                sparse_scores = v_bm25.get_scores(query_str)
                
                dense_ranks = np.argsort(-dense_dots)
                sparse_ranks = np.argsort(-sparse_scores)
                dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                
                rrf_scores = {}
                for idx in range(len(valid_indices)):
                    rrf_scores[idx] = 1.0 / (60 + dense_rank_map[idx]) + 1.0 / (60 + sparse_rank_map[idx])
                sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                retrieved_nodes = [db_items[valid_indices[idx]] for idx, score in sorted_rrf[:3]]
                print(f"       [RAG] RRF retrieved top chunks: {[node['title'] for node in retrieved_nodes]}")
                
                # Compress to sentences
                sentence_candidates = []
                for node in retrieved_nodes:
                    sentences = re.split(r'(?<=[.!?])\s+', node.get("parent_text", node["text"]))
                    for s in sentences:
                        s_clean = s.strip()
                        if len(s_clean.split()) > 3:
                            sentence_candidates.append({"text": s_clean})
                            
                # Batch embed sentences and select top 4
                s_texts = [s["text"] for s in sentence_candidates]
                s_embs = embed_model.encode(s_texts, show_progress_bar=False)
                s_dots = np.dot(s_embs / np.linalg.norm(s_embs, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                for idx, dot in enumerate(s_dots):
                    sentence_candidates[idx]["cosine"] = dot
                sentence_candidates.sort(key=lambda x: -x["cosine"])
                top_candidates = sentence_candidates[:8]
                
                # Rerank
                pairs = [[query_str, s["text"]] for s in top_candidates]
                ce_scores = reranker_model.predict(pairs)
                for idx, score in enumerate(ce_scores):
                    top_candidates[idx]["ce"] = float(score)
                top_candidates.sort(key=lambda x: -x["ce"])
                context = " ".join([s["text"] for s in top_candidates[:4]])
                t_rag_end = time.perf_counter()
                print(f"       [RAG] Cross-encoder reranked {len(top_candidates)} sentence candidates to select top 4. Context size: {len(context)} chars ({len(context.split())} words).")
                
                # Chat template construction
                messages = [
                    {"role": "system", "content": f"You are Waddles, Theodore J. LaGrow (TJ)'s personal chatbot assistant. Answer the user's question using ONLY this context:\n---\n{context}\n---\nYou MUST respond with a single valid JSON object holding an 'answer' property."},
                    {"role": "user", "content": query_str}
                ]
                
                # Model inference
                t_start = time.perf_counter()
                print(f"       [Inference] Querying generator model with custom system template...")
                outputs = pipe(messages, max_new_tokens=128, do_sample=False)
                t_end = time.perf_counter()
                
                ans_text = outputs[0]["generated_text"][-1]["content"]
                
                # Parse JSON answer
                clean_ans = ans_text
                try:
                    parsed = json.loads(ans_text)
                    clean_ans = parsed.get("answer", ans_text)
                except Exception:
                    # Parse fallback matching
                    m = re.search(r'"answer"\s*:\s*"([^"]+)"', ans_text)
                    if m: clean_ans = m.group(1)
                    
                if not isinstance(clean_ans, str):
                    if isinstance(clean_ans, (dict, list)):
                        clean_ans = json.dumps(clean_ans)
                    else:
                        clean_ans = str(clean_ans)
                    
                # Compute overlap metrics
                rouge_val = calculate_rouge_l_recall(clean_ans, ref_ans)
                
                # Compute semantic cosine similarity
                cand_vec = embed_model.encode(clean_ans, show_progress_bar=False)
                ref_vec = embed_model.encode(ref_ans, show_progress_bar=False)
                sem_sim = float(np.dot(cand_vec / np.linalg.norm(cand_vec), ref_vec / np.linalg.norm(ref_vec)))
                
                # Calculate new metrics
                ttr = calculate_ttr(clean_ans)
                groundedness = calculate_groundedness(clean_ans, context)
                citation_fidelity = calculate_citation_fidelity(clean_ans, context)
                hallucination_ratio = calculate_hallucination_ratio(clean_ans, context, query_str)
                verbosity_ratio = calculate_verbosity_ratio(clean_ans, ref_ans)
                structure_fidelity = calculate_structure_fidelity(ans_text)
                
                duration = t_end - t_start
                print(f"       [RAG Context retrieved in {t_rag_end - t_rag_start:.2f}s]")
                print(f"       [Inference completed in {duration:.2f}s]")
                print(f"       - Answer preview: {clean_ans[:100]}...")
                print(f"       - ROUGE-L Overlap: {rouge_val:.4f}, Semantic Cosine Similarity: {sem_sim:.4f}")
                print(f"       - Lexical Diversity (TTR): {ttr:.4f}, Groundedness: {groundedness:.4f}, Citation Fidelity: {citation_fidelity:.4f}")
                print(f"       - Hallucination Ratio: {hallucination_ratio:.4f}, Verbosity Ratio: {verbosity_ratio:.4f}, Structure Fidelity: {structure_fidelity:.4f}")
                
                rouge_sum += rouge_val
                sem_sim_sum += sem_sim
                char_len_sum += len(ans_text)
                latency_sum += duration
                ttr_sum += ttr
                groundedness_sum += groundedness
                citation_fidelity_sum += citation_fidelity
                hallucination_sum += hallucination_ratio
                verbosity_sum += verbosity_ratio
                structure_sum += structure_fidelity
                
            num_q = len(core_queries)
            phase2_results[name] = {
                "rouge_l": rouge_sum / num_q,
                "semantic_similarity": sem_sim_sum / num_q,
                "length": char_len_sum / num_q,
                "latency_sec": latency_sum / num_q,
                "lexical_diversity_ttr": ttr_sum / num_q,
                "groundedness": groundedness_sum / num_q,
                "citation_fidelity": citation_fidelity_sum / num_q,
                "hallucination_ratio": hallucination_sum / num_q,
                "verbosity_ratio": verbosity_sum / num_q,
                "structure_fidelity": structure_sum / num_q
            }
            print(f"\n>> {name} Summary - ROUGE-L: {phase2_results[name]['rouge_l']:.4f}, Cosine Sim: {phase2_results[name]['semantic_similarity']:.4f}, Avg Latency: {phase2_results[name]['latency_sec']:.2f}s")
            print(f"   TTR: {phase2_results[name]['lexical_diversity_ttr']:.4f}, Groundedness: {phase2_results[name]['groundedness']:.4f}, Citation Fidelity: {phase2_results[name]['citation_fidelity']:.4f}")
            print(f"   Hallucination: {phase2_results[name]['hallucination_ratio']:.4f}, Verbosity: {phase2_results[name]['verbosity_ratio']:.4f}, Structure: {phase2_results[name]['structure_fidelity']:.4f}")
            
            # Clean CUDA memory if applicable
            del pipe
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
        ablation_results["Phase 2: Generator Model Comparison"] = phase2_results
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(ablation_results, f, indent=2)
        print("Phase 2 generator sweeps finished. Generating updated plots...")
        try:
            generate_expanded_plots(ablation_results)
        except Exception as pe:
            print(f"Failed to generate plots: {pe}")

    # ABLATION PHASE 3: Persona Adherence & Few-Shot Anchoring
    if "Phase 3: Persona & Few-Shot Adherence" not in ablation_results:
        print("\n--- Running Phase 3: Persona & Few-Shot Adherence ---")
        phase3_results = {}
        
        # Load lightweight representative model Qwen2.5-0.5B for fast testing
        print("\n[Phase 3] Loading base model Qwen2.5-0.5B-Instruct...")
        pipe = load_hf_generator("Qwen/Qwen2.5-0.5B-Instruct")
        if not pipe:
            print("Skipping Phase 3 (generator failed to load).")
        else:
            print("[Phase 3] Base model loaded successfully.")
            personas = ["helpful", "sassy", "pirate", "cynical_redditor"]
            few_shots = [0, 1, 2, 3]
            
            for persona in personas:
                phase3_results[persona] = {}
                for shot in few_shots:
                    print(f"\n  Evaluating persona '{persona}' with {shot} few-shot examples...")
                    
                    json_conformance_sum = 0
                    style_density_sum = 0.0
                    
                    num_q = len(core_queries)
                    for q_idx, q_item in enumerate(core_queries):
                        query_str = q_item["query"]
                        intent = q_item["intent"]
                        
                        # Fetch RAG Context (Ratio B, Hybrid RRF k=60, Pre-filtering, Rerank)
                        q_vec = embed_model.encode(query_str, show_progress_bar=False)
                        valid_indices = [i for i, node in enumerate(db_items) if doc_passes_intent(node, intent)]
                        if not valid_indices: valid_indices = list(range(len(db_items)))
                        
                        dense_dots = np.dot(doc_embeddings[valid_indices] / np.linalg.norm(doc_embeddings[valid_indices], axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                        
                        doc_texts = [db_items[i]["text"] for i in valid_indices]
                        v_bm25 = SimpleBM25(doc_texts)
                        sparse_scores = v_bm25.get_scores(query_str)
                        
                        dense_ranks = np.argsort(-dense_dots)
                        sparse_ranks = np.argsort(-sparse_scores)
                        dense_rank_map = {idx: r for r, idx in enumerate(dense_ranks)}
                        sparse_rank_map = {idx: r for r, idx in enumerate(sparse_ranks)}
                        
                        rrf_scores = {}
                        for idx in range(len(valid_indices)):
                            rrf_scores[idx] = 1.0 / (60 + dense_rank_map[idx]) + 1.0 / (60 + sparse_rank_map[idx])
                        sorted_rrf = sorted(rrf_scores.items(), key=lambda x: -x[1])
                        retrieved_nodes = [db_items[valid_indices[idx]] for idx, score in sorted_rrf[:3]]
                        
                        # Compress to sentences
                        sentence_candidates = []
                        for node in retrieved_nodes:
                            sentences = re.split(r'(?<=[.!?])\s+', node.get("parent_text", node["text"]))
                            for s in sentences:
                                s_clean = s.strip()
                                if len(s_clean.split()) > 3:
                                    sentence_candidates.append({"text": s_clean})
                                    
                        # Batch embed and select top 4
                        s_texts = [s["text"] for s in sentence_candidates]
                        s_embs = embed_model.encode(s_texts, show_progress_bar=False)
                        s_dots = np.dot(s_embs / np.linalg.norm(s_embs, axis=1, keepdims=True), q_vec / np.linalg.norm(q_vec))
                        for idx, dot in enumerate(s_dots):
                            sentence_candidates[idx]["cosine"] = dot
                        sentence_candidates.sort(key=lambda x: -x["cosine"])
                        top_candidates = sentence_candidates[:8]
                        
                        # Rerank
                        pairs = [[query_str, s["text"]] for s in top_candidates]
                        ce_scores = reranker_model.predict(pairs)
                        for idx, score in enumerate(ce_scores):
                            top_candidates[idx]["ce"] = float(score)
                        top_candidates.sort(key=lambda x: -x["ce"])
                        context = " ".join([s["text"] for s in top_candidates[:4]])
                        
                        # Retrieve persona anchoring samples
                        examples = [ex for ex in PERSONA_EXAMPLES if ex["tone"] == persona]
                        
                        # Build messages sequence with system prompt
                        system_msg = f"You are Waddles, Theodore J. LaGrow (TJ)'s personal chatbot assistant."
                        if persona != "helpful":
                            system_msg += f" Respond strictly adopting a {persona} style persona."
                        system_msg += f"\nAnswer the user's question using ONLY this context:\n---\n{context}\n---\nYou MUST respond with a single valid JSON object holding an 'answer' property."
                        
                        messages = [{"role": "system", "content": system_msg}]
                        
                        # Inject few-shot instances
                        for i in range(min(shot, len(examples))):
                            messages.append({"role": "user", "content": examples[i]["query"]})
                            # Format response as JSON string
                            messages.append({"role": "assistant", "content": json.dumps({"answer": examples[i]["answer"]})})
                            
                        # Add final user query
                        messages.append({"role": "user", "content": query_str})
                        
                        # Inference
                        t_start = time.perf_counter()
                        outputs = pipe(messages, max_new_tokens=128, do_sample=False)
                        t_end = time.perf_counter()
                        ans_text = outputs[0]["generated_text"][-1]["content"]
                        
                        # Check JSON conformance
                        is_valid_json = 0
                        try:
                            parsed = json.loads(ans_text)
                            if "answer" in parsed:
                                is_valid_json = 1
                        except Exception:
                            pass
                        json_conformance_sum += is_valid_json
                        
                        # Check Persona Lexical Density
                        words = re.findall(r'\w+', ans_text.lower())
                        word_count = max(len(words), 1)
                        hits = 0
                        
                        if persona == "pirate":
                            pirate_keywords = ["ahoy", "ye", "matey", "harrr", "avast", "cap", "landlubber", "sea", "treasure", "ship"]
                            for w in words:
                                if any(pk in w for pk in pirate_keywords):
                                    hits += 1
                        elif persona == "sassy":
                            sassy_keywords = ["obviously", "if", "fascinating", "sarcastic", "look", "tolerance", "zero", "wait", "marvelous", "sarcasm"]
                            for w in words:
                                if any(sk in w for sk in sassy_keywords):
                                    hits += 1
                        elif persona == "cynical_redditor":
                            redditor_keywords = ["afaik", "gatekeep", "omscs", "reddit", "typical", "annoy", "tldr"]
                            for w in words:
                                if any(rk in w for rk in redditor_keywords):
                                    hits += 1
                            if "/s" in ans_text.lower():
                                hits += 1
                        else:
                            # helpful (measure standard corporate/polite vocabulary density as a proxy)
                            helpful_keywords = ["please", "contact", "details", "information", "assist", "published", "teach", "research", "available"]
                            for w in words:
                                if any(hk in w for hk in helpful_keywords):
                                    hits += 1
                                    
                        style_density = hits / word_count
                        style_density_sum += style_density
                        
                        duration = t_end - t_start
                        print(f"    - Query {q_idx+1}/{num_q} '{query_str[:40]}...' in {duration:.2f}s (JSON: {is_valid_json}, Style Density: {style_density:.2%})")
                        print(f"      [Phase 3 Detail] Generated Text: {ans_text.strip()}")
                        if persona == "pirate":
                            kw_list = pirate_keywords
                        elif persona == "sassy":
                            kw_list = sassy_keywords
                        elif persona == "cynical_redditor":
                            kw_list = redditor_keywords
                        else:
                            kw_list = helpful_keywords
                        matched_kws = [w for w in words if any(kw in w for kw in kw_list)]
                        print(f"      [Phase 3 Detail] Persona Words Checked: {word_count} | Matching hits: {hits} | Matches: {matched_kws}")
                        
                    phase3_results[persona][f"shot_{shot}"] = {
                        "json_conformance": json_conformance_sum / num_q,
                        "style_density": style_density_sum / num_q
                    }
                    print(f"    >> Shot {shot} Summary - JSON conformance: {phase3_results[persona][f'shot_{shot}']['json_conformance']:.1%}, Style Density: {phase3_results[persona][f'shot_{shot}']['style_density']:.2%}")
            
            ablation_results["Phase 3: Persona & Few-Shot Adherence"] = phase3_results
            with open(CHECKPOINT_FILE, "w") as f:
                json.dump(ablation_results, f, indent=2)
                
    # Save final results
    with open(RESULTS_FILE, "w") as f:
        json.dump(ablation_results, f, indent=2)
    print(f"\nFinal expanded results compiled and written to {RESULTS_FILE}")
    
    # Generate Plots
    generate_expanded_plots(ablation_results)


def generate_expanded_plots(results):
    print("\nCompiling Matplotlib benchmark charts...")
    
    # 1. Chunking Ratio Recall (Phase 1)
    p1 = results.get("Phase 1: Retrieval Parameters", {})
    ratios_keys = ["chunk_Ratio A (Child 30 / Parent 150)", "chunk_Ratio B (Child 50 / Parent 200)", "chunk_Ratio C (Child 100 / Parent 500)"]
    if all(k in p1 for k in ratios_keys):
        plt.figure(figsize=(7, 5))
        labels = ["A (30/150)", "B (50/200)", "C (100/500)"]
        hit3_vals = [p1[k]["hit_at_3"] for k in ratios_keys]
        mrr_vals = [p1[k]["mrr"] for k in ratios_keys]
        
        x = np.arange(len(labels))
        width = 0.35
        plt.bar(x - width/2, hit3_vals, width, label="Recall@3", color="#2dd4bf")
        plt.bar(x + width/2, mrr_vals, width, label="MRR", color="#a855f7")
        plt.ylabel("Score")
        plt.title("Jekyll Hierarchical Chunk Ratios Retrieval Performance")
        plt.xticks(x, labels)
        plt.ylim(0, 1.1)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "chunk_ratio_recall.png"), dpi=150)
        plt.close()
        
    # 2. Parameter Trade-offs (Phase 1 K and cutoffs)
    k_keys = [f"ret_K_{k}" for k in [2, 3, 5, 8]]
    if all(k in p1 for k in k_keys):
        plt.figure(figsize=(7, 5))
        labels = ["K=2", "K=3", "K=5", "K=8"]
        hit3_vals = [p1[k]["hit_at_3"] for k in k_keys]
        mrr_vals = [p1[k]["mrr"] for k in k_keys]
        
        plt.plot(labels, hit3_vals, marker='o', linewidth=2.5, color="#38bdf8", label="Recall@3")
        plt.plot(labels, mrr_vals, marker='s', linewidth=2.5, color="#eab308", label="MRR")
        plt.ylabel("Retrieval Score")
        plt.title("Impact of Retrieved Document Chunks (K) on Search Performance")
        plt.ylim(min(mrr_vals) * 0.95, 1.05)
        plt.legend()
        plt.grid(linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "parameter_tradeoffs.png"), dpi=150)
        plt.close()

    # 3. Quantization recall impact
    quant_keys = ["quant_float32", "quant_int8", "quant_binary"]
    if all(k in p1 for k in quant_keys):
        plt.figure(figsize=(7, 5))
        labels = ["float32", "int8", "binary"]
        hit3_vals = [p1[k]["hit_at_3"] for k in quant_keys]
        mrr_vals = [p1[k]["mrr"] for k in quant_keys]
        
        x = np.arange(len(labels))
        width = 0.35
        plt.bar(x - width/2, hit3_vals, width, label="Recall@3", color="#f43f5e")
        plt.bar(x + width/2, mrr_vals, width, label="MRR", color="#fb923c")
        plt.ylabel("Performance Score")
        plt.title("Impact of Vector Quantization on Search Quality")
        plt.xticks(x, labels)
        plt.ylim(0, 1.1)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "quantization_impact.png"), dpi=150)
        plt.close()

    # 4. Local Generator Comparison (Phase 2)
    p2 = results.get("Phase 2: Generator Model Comparison", {})
    if p2:
        plt.figure(figsize=(9, 5))
        models = list(p2.keys())
        rouge_vals = [p2[m]["rouge_l"] for m in models]
        sim_vals = [p2[m]["semantic_similarity"] for m in models]
        
        x = np.arange(len(models))
        width = 0.35
        plt.bar(x - width/2, rouge_vals, width, label="ROUGE-L (Overlap)", color="#2dd4bf")
        plt.bar(x + width/2, sim_vals, width, label="Semantic Similarity", color="#38bdf8")
        plt.ylabel("Performance Score")
        plt.title("Generator Quality Comparison: Browser-Friendly vs. Baselines")
        plt.xticks(x, models)
        plt.ylim(0, 1.1)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "generation_comparison.png"), dpi=150)
        plt.close()

        # 4b. Local Generator Integrity & Diversity Comparison
        if any("lexical_diversity_ttr" in p2[m] for m in models):
            plt.figure(figsize=(9, 5))
            ttr_vals = [p2[m].get("lexical_diversity_ttr", 0.0) for m in models]
            ground_vals = [p2[m].get("groundedness", 0.0) for m in models]
            
            plt.bar(x - width/2, ttr_vals, width, label="Lexical Diversity (TTR)", color="#ec4899")
            plt.bar(x + width/2, ground_vals, width, label="Groundedness (Context Overlap)", color="#eab308")
            plt.ylabel("Performance Score")
            plt.title("Generator Integrity & Diversity Comparison")
            plt.xticks(x, models)
            plt.ylim(0, 1.1)
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGE_OUT_DIR, "generation_integrity.png"), dpi=150)
            plt.close()


    # 5. Persona Adherence & Few-Shot Anchoring (Phase 3)
    p3 = results.get("Phase 3: Persona & Few-Shot Adherence", {})
    if p3:
        plt.figure(figsize=(10, 5))
        shots = [0, 1, 2, 3]
        x_ticks = ["0-shot", "1-shot", "2-shot", "3-shot"]
        
        for persona, color in [("helpful", "#2dd4bf"), ("sassy", "#f43f5e"), ("pirate", "#38bdf8"), ("cynical_redditor", "#a855f7")]:
            if persona in p3:
                conformance = [p3[persona][f"shot_{s}"]["json_conformance"] for s in shots]
                style_dens = [p3[persona][f"shot_{s}"]["style_density"] for s in shots]
                
                p_label = persona.replace("_", " ").title()
                plt.plot(x_ticks, conformance, linestyle="-", marker="o", color=color, label=f"{p_label} - JSON Conformance")
                plt.plot(x_ticks, style_dens, linestyle="--", marker="s", color=color, label=f"{p_label} - Style Density")
                
        plt.xlabel("Few-Shot Style Examples Injected")
        plt.ylabel("Score Rate")
        plt.title("Few-Shot Persona Styling Adherence and JSON Conformance Curve")
        plt.ylim(-0.05, 1.15)
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.grid(linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "persona_adherence.png"), dpi=150)
        plt.close()

    print("Matplotlib figure compilation complete. Saved plots in assets/images/ablation/.")


if __name__ == "__main__":
    main()
