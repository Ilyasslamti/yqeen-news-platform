#!/usr/bin/env python3
"""
يقين الصحفي - YAQEEN AL-SAHAFI
منصة الأخبار المغربية الاحترافية مع إعادة الصياغة بالذكاء الاصطناعي
Professional Moroccan News Platform with AI-Powered Rewriting
"""

import sys, os, threading, json
from pathlib import Path

BASE = Path(__file__).resolve().parent
os.chdir(str(BASE))
sys.path.insert(0, str(BASE))

from dotenv import load_dotenv
load_dotenv(BASE / '.env')

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def setup_app():
    app = QApplication(sys.argv)
    app.setApplicationName("يقين الصحفي")
    app.setApplicationDisplayName("YAQEEN Al-Sahafi - Moroccan News Platform")

    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    app.setStyle("Fusion")
    return app

def main():
    app = setup_app()

    from rss_service import background_refresh
    bg = threading.Thread(target=background_refresh, daemon=True)
    bg.start()

    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
