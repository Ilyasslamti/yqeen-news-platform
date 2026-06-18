"""
سكربت تحديث RSS - يستعمل في الـ Cron (PythonAnywhere)
يشغله PythonAnywhere كل ساعة
"""
import sys, os
from pathlib import Path
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
os.chdir(str(BASE))

from dotenv import load_dotenv
load_dotenv(BASE / '.env')

from rss_service import fetch_all_news
articles = fetch_all_news(force=True)
print(f"Refreshed: {len(articles)} articles")
