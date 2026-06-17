import feedparser, json, hashlib, time, threading, socket
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import config

_lock = threading.Lock()
_news_cache = []
_last_fetch = 0

def fetch_single_feed(source: dict) -> list:
    items = []
    try:
        socket.setdefaulttimeout(6)
        d = feedparser.parse(source["url"])
        for e in d.entries[:config.MAX_ARTICLES_PER_FEED]:
            title = (e.get("title") or "").strip()
            link = (e.get("link") or "").strip()
            if not title or not link:
                continue
            summary = (e.get("summary") or e.get("description") or "")[:400]
            published = (e.get("published") or e.get("updated") or "")
            items.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "source_name": source["name"],
                "source_url": source["url"],
                "lang": source["lang"],
                "id": hashlib.md5((title + link).encode()).hexdigest()[:12],
            })
    except:
        pass
    return items

def fetch_all_news(force=False) -> list:
    global _news_cache, _last_fetch
    now = time.time()

    if not force and _news_cache and (now - _last_fetch) < config.CACHE_TTL:
        return _news_cache

    from rss_sources import get_all_sources
    sources = get_all_sources()
    all_articles = []

    with ThreadPoolExecutor(max_workers=50) as ex:
        futures = {ex.submit(fetch_single_feed, s): s for s in sources}
        for f in as_completed(futures):
            try:
                all_articles.extend(f.result())
            except:
                pass

    seen = set()
    deduped = []
    for a in all_articles:
        key = a["title"][:80].lower()
        if key not in seen:
            seen.add(key)
            deduped.append(a)

    deduped.sort(key=lambda x: x.get("published", ""), reverse=True)

    with _lock:
        _news_cache = deduped
        _last_fetch = now

    try:
        with open(config.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "_ts": now, "articles": deduped[:500]
            }, f, ensure_ascii=False)
    except:
        pass

    return deduped

def _load_cache():
    global _news_cache
    try:
        p = Path(config.CACHE_FILE)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            _news_cache = [a for a in data.get("articles", []) if a.get("title")]
    except:
        pass

def get_cached_news(lang=None) -> list:
    global _news_cache
    if not _news_cache:
        _load_cache()
        return _news_cache
    if lang and lang != "all":
        return [a for a in _news_cache if a.get("lang") == lang]
    return _news_cache

def background_refresh():
    time.sleep(10)
    try:
        fetch_all_news()
    except:
        pass
    while True:
        time.sleep(config.REFRESH_INTERVAL)
        try:
            fetch_all_news(force=True)
        except:
            pass
