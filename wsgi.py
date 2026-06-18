"""
PythonAnywhere WSGI
"""
import sys, os
from pathlib import Path
BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from rss_service import _load_cache
_load_cache()

from web_app import app as application
