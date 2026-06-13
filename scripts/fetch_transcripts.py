import os
import re
import json
import yaml
import sys
import subprocess

# Ensure youtube-transcript-api is installed
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Installing youtube-transcript-api dynamically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api"])
    from youtube_transcript_api import YouTubeTranscriptApi

# Setup paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "_data")
OUTPUT_FILE = os.path.join(DATA_DIR, "youtube_transcripts.json")

def extract_youtube_id(url):
    """Extracts the 11-character YouTube video ID from a URL."""
    if not url:
        return None
    # Matches ?v=<id> or &v=<id>
    match = re.search(r"[?&]v=([^&#\s]+)", url)
    if match:
        return match.group(1)
    # Matches youtu.be/<id>
    match = re.search(r"youtu\.be/([^?&#\s]+)", url)
    if match:
        return match.group(1)
    return None

def main():
    videos = []

    # Parse talks.yml
    talks_path = os.path.join(DATA_DIR, "talks.yml")
    if os.path.isfile(talks_path):
        print("Parsing talks.yml...")
        with open(talks_path, "r", encoding="utf-8") as f:
            talks = yaml.safe_load(f) or []
        for talk in talks:
            title = talk.get("title", "")
            links = talk.get("links", [])
            if not isinstance(links, list):
                continue
            for link in links:
                if isinstance(link, list) and len(link) >= 2:
                    label, url = link[0], link[1]
                    if label.lower() == "youtube":
                        vid = extract_youtube_id(url)
                        if vid:
                            videos.append({
                                "video_id": vid,
                                "title": title,
                                "url": url,
                                "original_type": "talk"
                            })

    # Parse defense.yml
    defense_path = os.path.join(DATA_DIR, "defense.yml")
    if os.path.isfile(defense_path):
        print("Parsing defense.yml...")
        with open(defense_path, "r", encoding="utf-8") as f:
            defenses = yaml.safe_load(f) or []
        for df in defenses:
            title = df.get("title", "")
            links = df.get("links", [])
            if not isinstance(links, list):
                continue
            for link in links:
                if isinstance(link, list) and len(link) >= 2:
                    label, url = link[0], link[1]
                    if label.lower() == "youtube":
                        vid = extract_youtube_id(url)
                        if vid:
                            videos.append({
                                "video_id": vid,
                                "title": title,
                                "url": url,
                                "original_type": "milestone"
                            })

    print(f"Found {len(videos)} YouTube videos to fetch transcripts for.")

    transcripts_data = []
    for video in videos:
        vid = video["video_id"]
        title = video["title"]
        print(f"Fetching transcript for video {vid} ('{title}')...")
        try:
            api = YouTubeTranscriptApi()
            fetched = api.fetch(vid, languages=["en"])
            text = " ".join([snippet.text for snippet in fetched])
            text = re.sub(r"\s+", " ", text).strip()
            
            transcripts_data.append({
                "video_id": vid,
                "title": title,
                "url": video["url"],
                "transcript": text,
                "original_type": video["original_type"]
            })
            print(f"Successfully fetched transcript ({len(text.split())} words).")
        except Exception as e:
            # Captions might be disabled, or the video could lack English subtitles.
            # We log a warning and skip to next video.
            print(f"Warning: Could not fetch English transcript for {vid}: {e}")

    # Write output to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(transcripts_data, f, ensure_ascii=False, indent=2)

    print(f"Done! Saved {len(transcripts_data)} transcripts to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
