#!/usr/bin/env python3
"""
يقين الصحفي - YAQEEN AL-SAHAFI
منصة الأخبار المغربية مع إعادة الصياغة بالذكاء الاصطناعي
تشغيل: python main.py
"""

import sys, os, threading
from pathlib import Path

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from dotenv import load_dotenv
load_dotenv(BASE / '.env')

from rss_service import background_refresh
threading.Thread(target=background_refresh, daemon=True).start()

from config import GROQ_KEYS
print('=' * 50)
print('يقين الصحفي  -  YAQEEN Al-Sahafi')
print('=' * 50)
print('Groq keys: %d (Round-Robin)' % len(GROQ_KEYS))
print('RSS sources: 141')
print('Server: http://localhost:5000')
print('=' * 50)

from web_app import app
app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
