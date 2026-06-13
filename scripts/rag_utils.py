import os
import re
import json
import time
import math
import collections
import html
import numpy as np
import yaml
import requests
import torch

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES_DIR = os.path.join(PROJECT_ROOT, "_pages")
POSTS_DIR = os.path.join(PROJECT_ROOT, "_posts")
NEWSLETTERS_DIR = os.path.join(PROJECT_ROOT, "_newsletters")
DATA_DIR = os.path.join(PROJECT_ROOT, "_data")
EMBEDDINGS_FILE = os.path.join(PROJECT_ROOT, "assets", "json", "embeddings.json")
QUERIES_FILE = os.path.join(PROJECT_ROOT, "scripts", "ablation_queries.json")
CACHE_DIR = os.path.join(PROJECT_ROOT, "scripts", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CHECKPOINT_FILE = os.path.join(CACHE_DIR, "ablation_checkpoint.json")
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
    cache_file = os.path.join(CACHE_DIR, f"embeddings_cache_{max_child}_{max_parent}.json")
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
        max_val = np.max(np.abs(v))
        if max_val == 0:
            return v.astype(np.int8).tolist()
        scaled = v * (127.0 / max_val)
        return np.round(scaled).astype(np.int8).tolist()
    elif method == "binary":
        return np.sign(v).astype(np.int8).tolist()
    return emb


class OllamaPipeline:
    def __init__(self, model_name):
        self.model_name = model_name
        
    def __call__(self, messages, max_new_tokens=128, do_sample=False, **kwargs):
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_new_tokens,
                "temperature": 0.0 if not do_sample else 0.7
            }
        }
        try:
            response = requests.post(url, json=payload, timeout=90)
            response.raise_for_status()
            res_json = response.json()
            assistant_content = res_json["message"]["content"]
            return [{"generated_text": messages + [{"role": "assistant", "content": assistant_content}]}]
        except Exception as e:
            print(f"Ollama API call failed: {e}")
            raise e


def get_system_specs():
    import platform
    import psutil
    
    specs = {
        "os": f"{platform.system()} {platform.release()}",
        "cpu": platform.processor() or "Unknown CPU",
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "gpu_available": torch.cuda.is_available(),
    }
    if specs["gpu_available"]:
        specs["gpu_name"] = torch.cuda.get_device_name(0)
        specs["gpu_vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
    else:
        specs["gpu_name"] = "N/A"
        specs["gpu_vram_gb"] = 0.0
    return specs


def llm_judge_evaluate(context, query, generated_answer):
    url = "http://localhost:11434/api/chat"
    
    def parse_judge_json(text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                return float(data.get("score", 0.5))
        except Exception:
            pass
        return 0.5

    faithfulness_prompt = (
        "You are an expert evaluator. Your task is to judge the FAITHFULNESS of a generated answer with respect to the provided context.\n"
        "An answer is faithful (score=1.0) if all claims made in the answer can be directly inferred from the context. "
        "It should not contain any information not present in the context, even if true. If the model correctly refuses to answer "
        "because the context is missing information (e.g. out-of-scope query), score it as 1.0.\n\n"
        f"[Context]:\n{context}\n\n"
        f"[Query]:\n{query}\n\n"
        f"[Generated Answer]:\n{generated_answer}\n\n"
        "Provide your evaluation in the following JSON format:\n"
        "{\n"
        '  "reasoning": "A brief explanation.",\n'
        '  "score": 1.0 or 0.0\n'
        "}\n"
        "Return ONLY the JSON object. Do not include any explanation outside the JSON."
    )
    
    payload_f = {
        "model": "llama3.1:8b-instruct-q4_K_M",
        "messages": [{"role": "user", "content": faithfulness_prompt}],
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 100}
    }
    
    relevance_prompt = (
        "You are an expert evaluator. Your task is to judge the RELEVANCE of a generated answer with respect to the query.\n"
        "An answer is relevant (score=1.0) if it directly and completely addresses the user's question, without going off-topic.\n\n"
        f"[Query]:\n{query}\n\n"
        f"[Generated Answer]:\n{generated_answer}\n\n"
        "Provide your evaluation in the following JSON format:\n"
        "{\n"
        '  "reasoning": "A brief explanation.",\n'
        '  "score": 1.0 or 0.0\n'
        "}\n"
        "Return ONLY the JSON object. Do not include any explanation outside the JSON."
    )
    
    payload_r = {
        "model": "llama3.1:8b-instruct-q4_K_M",
        "messages": [{"role": "user", "content": relevance_prompt}],
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 100}
    }
    
    faith_score = 1.0
    rel_score = 1.0
    
    try:
        resp_f = requests.post(url, json=payload_f, timeout=20)
        if resp_f.status_code == 200:
            content = resp_f.json()["message"]["content"]
            faith_score = parse_judge_json(content)
    except Exception as e:
        print(f"  [Judge Warn] Faithfulness check failed: {e}")
        
    try:
        resp_r = requests.post(url, json=payload_r, timeout=20)
        if resp_r.status_code == 200:
            content = resp_r.json()["message"]["content"]
            rel_score = parse_judge_json(content)
    except Exception as e:
        print(f"  [Judge Warn] Relevance check failed: {e}")
        
    return faith_score, rel_score


def load_hf_generator(model_id, fallback_id=None):
    from transformers import pipeline
    
    force_quant = None
    if model_id.endswith("-4bit") and not model_id.startswith("unsloth/"):
        force_quant = "4bit"
        model_id = model_id[:-5]
    elif model_id.endswith("-8bit") and not model_id.startswith("unsloth/"):
        force_quant = "8bit"
        model_id = model_id[:-5]
    elif model_id.endswith("-fp16") and not model_id.startswith("unsloth/"):
        force_quant = "fp16"
        model_id = model_id[:-5]

    is_large = any(x in model_id.lower() for x in ["7b", "8b", "70b"])
    if is_large and force_quant is None:
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=2)
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                target_model = None
                for m in models:
                    if "llama3.1:8b" in m or "llama3:8b" in m or "llama3" in m:
                        target_model = m
                        break
                if target_model:
                    print(f"Using local Ollama model '{target_model}' for large model '{model_id}' instead of downloading from Hugging Face.")
                    return OllamaPipeline(target_model)
        except Exception as oe:
            print(f"Ollama connection check failed, will try Hugging Face: {oe}")

    use_auth = "meta-llama" in model_id and "unsloth" not in model_id
    token = os.environ.get("HF_TOKEN")
    
    print(f"Attempting to load Hugging Face pipeline for: {model_id}")
    try:
        if use_auth and not token:
            raise ValueError("Missing HF_TOKEN environment variable required for Llama models.")
        
        is_medium = any(x in model_id.lower() for x in ["3b", "3.5b", "3.8b", "4b"])
        
        kwargs = {
            "token": token if use_auth else None
        }
        if torch.cuda.is_available():
            kwargs["device_map"] = "auto"
            
            if force_quant == "4bit":
                kwargs["model_kwargs"] = {"load_in_4bit": True}
                print(f"Force loading {model_id} on GPU with 4-bit quantization...")
            elif force_quant == "8bit":
                kwargs["model_kwargs"] = {"load_in_8bit": True}
                print(f"Force loading {model_id} on GPU with 8-bit quantization...")
            elif force_quant == "fp16":
                kwargs["torch_dtype"] = torch.float16
                print(f"Force loading {model_id} on GPU in float16...")
            else:
                if is_large or is_medium:
                    try:
                        import bitsandbytes
                        kwargs["model_kwargs"] = {"load_in_4bit": True}
                        print(f"Loading {model_id} on GPU with 4-bit quantization...")
                    except ImportError:
                        kwargs["torch_dtype"] = torch.float16
                        print(f"bitsandbytes not available, loading {model_id} on GPU in float16...")
                else:
                    kwargs["torch_dtype"] = torch.float16
                    print(f"Loading {model_id} on GPU in float16...")
        else:
            kwargs["device"] = -1
            kwargs["torch_dtype"] = torch.float32
            print(f"CUDA not available, loading {model_id} on CPU in float32...")
            
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
                is_medium_fb = any(x in fallback_id.lower() for x in ["3b", "3.5b", "3.8b", "4b"])
                fallback_kwargs = {
                    "token": token if use_auth else None
                }
                if torch.cuda.is_available():
                    fallback_kwargs["device_map"] = "auto"
                    if is_large_fb or is_medium_fb:
                        try:
                            import bitsandbytes
                            fallback_kwargs["model_kwargs"] = {"load_in_4bit": True}
                        except ImportError:
                            fallback_kwargs["torch_dtype"] = torch.float16
                    else:
                        fallback_kwargs["torch_dtype"] = torch.float16
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
