import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse

def extract_article(url: str, timeout=15) -> dict:
    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.text and len(article.text) > 100:
            text = article.text
        else:
            text = _fallback_extract(url, timeout)

        return {
            "title": article.title or "",
            "text": text or "",
            "authors": article.authors or [],
            "publish_date": str(article.publish_date or ""),
            "top_image": article.top_image or "",
            "url": url,
        }
    except:
        text = _fallback_extract(url, timeout)
        return {
            "title": "",
            "text": text or "",
            "authors": [],
            "publish_date": "",
            "top_image": "",
            "url": url,
        }

def _fallback_extract(url: str, timeout=15) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ar,fr;q=0.9,en;q=0.8",
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        paragraphs = soup.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30)
        if len(text) < 100:
            body = soup.find("body")
            if body:
                text = body.get_text(separator="\n", strip=True)[:5000]
        return text[:8000]
    except:
        return ""
