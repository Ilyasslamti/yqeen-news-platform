"""
WSGI entry point for PythonAnywhere / Render / Gunicorn
"""
import sys, os, threading
from pathlib import Path
BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from rss_service import background_refresh, _load_cache, fetch_all_news
_load_cache()
threading.Thread(target=background_refresh, daemon=True).start()

from web_app import app as application
