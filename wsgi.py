"""
WSGI entry point for PythonAnywhere / Render / Gunicorn
"""
import sys, os, threading
from pathlib import Path
BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from rss_service import background_refresh, fetch_all_news
threading.Thread(target=background_refresh, daemon=True).start()

from web_app import app as application

if __name__ == '__main__':
    from web_app import app
    app.run()
