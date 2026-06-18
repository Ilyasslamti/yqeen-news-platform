import requests, re
from bs4 import BeautifulSoup

def extract_article(url: str, timeout=8) -> dict:
    text, title = "", ""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "ar,fr;q=0.9,en;q=0.8",
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "lxml")
        if soup.title:
            title = soup.title.get_text(strip=True)
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
            tag.decompose()
        for div in soup.find_all("div", class_=re.compile(r"(comment|sidebar|ad|menu|footer|header)")):
            div.decompose()
        ps = soup.find_all("p")
        paragraphs = [p.get_text(strip=True) for p in ps if len(p.get_text(strip=True)) > 40]
        text = "\n\n".join(paragraphs[:60])[:8000]
        if len(text) < 200:
            body = soup.find("body")
            if body:
                text = body.get_text(separator="\n", strip=True)[:6000]
    except:
        pass
    return {"title": title, "text": text, "url": url}
