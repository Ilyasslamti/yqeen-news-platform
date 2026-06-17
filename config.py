import os, itertools, threading
from pathlib import Path
from dotenv import load_dotenv

_BASE = Path(__file__).resolve().parent
load_dotenv(_BASE / '.env')

GROQ_KEYS = [
    os.getenv('GROQ_KEY_1', ''),
    os.getenv('GROQ_KEY_2', ''),
    os.getenv('GROQ_KEY_3', ''),
    os.getenv('GROQ_KEY_4', ''),
]
GROQ_KEYS = [k for k in GROQ_KEYS if k]

_key_lock = threading.Lock()
_key_cycle = itertools.cycle(GROQ_KEYS) if GROQ_KEYS else iter([])

def get_next_groq_key():
    with _key_lock:
        return next(_key_cycle, None)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_REPO = 'yqeen-news-platform'

MAX_ARTICLES_PER_FEED = int(os.getenv('MAX_ARTICLES_PER_FEED', '10'))
CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))
REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '300'))

CACHE_FILE = str(_BASE / 'news_cache.json')
SOURCES_FILE = str(_BASE / 'moroccan_sources.json')
