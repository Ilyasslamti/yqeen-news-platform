"""
يقين الصحفي - Web Application
Flask-based news aggregator with AI rewriting
"""

import sys, os, json, hashlib, threading, time
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory

BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from config import GROQ_KEYS
from rss_service import fetch_all_news, get_cached_news, background_refresh

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

_THREAD_LOCK = threading.Lock()

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return resp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    lang = request.args.get('lang', 'all')
    articles = get_cached_news(lang)
    if not articles:
        threading.Thread(target=fetch_all_news, daemon=True).start()
        return jsonify({'success': True, 'articles': [], 'count': 0, 'loading': True})
    return jsonify({
        'success': True,
        'articles': articles[:80],
        'count': len(articles),
        'language': lang,
    })

@app.route('/api/refresh')
def api_refresh():
    threading.Thread(target=lambda: fetch_all_news(force=True), daemon=True).start()
    return jsonify({'success': True, 'message': 'Refresh started'})

@app.route('/api/extract', methods=['POST'])
def api_extract():
    data = request.get_json()
    url = (data or {}).get('url', '')
    if not url:
        return jsonify({'success': False, 'error': 'URL required'}), 400
    from article_service import extract_article
    result = extract_article(url)
    text = result.get('text', '') or result.get('title', '')
    return jsonify({
        'success': True,
        'title': result.get('title', ''),
        'text': text[:8000],
        'url': url,
    })

@app.route('/api/rewrite', methods=['POST'])
def api_rewrite():
    data = request.get_json()
    text = (data or {}).get('text', '').strip()
    lang = (data or {}).get('lang', 'ar')
    if not text or len(text) < 50:
        return jsonify({'success': False, 'error': 'Text too short'}), 400
    from rewriter_service import rewrite_article
    result = rewrite_article(text[:4000], lang)
    return jsonify({
        'success': True,
        'original': text[:500],
        'rewritten': result or text,
        'language': lang,
    })

@app.route('/api/stats')
def api_stats():
    articles = get_cached_news()
    from rss_sources import TOTAL_SOURCES
    return jsonify({
        'success': True,
        'total_sources': TOTAL_SOURCES,
        'cached_articles': len(articles),
        'groq_keys': len(GROQ_KEYS),
        'languages': list(MOROCCAN_SOURCES.keys()),
    })

from rss_sources import MOROCCAN_SOURCES

if __name__ == '__main__':
    print('Starting YAQEEN Al-Sahafi Web Server...')
    threading.Thread(target=background_refresh, daemon=True).start()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
