from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSplitter, QStatusBar, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.news_list import NewsListView
from ui.article_view import ArticleView
from ui.styles import APP_STYLE, STATUS_BAR_STYLE


class NewsFetcher(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            from rss_service import fetch_all_news
            articles = fetch_all_news(force=True)
            self.finished.emit(articles)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.articles = []
        self._setup_ui()
        self._load_news()

    def _setup_ui(self):
        self.setWindowTitle("يقين الصحفي - منصة الأخبار المغربية")
        self.setMinimumSize(1400, 800)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setStyleSheet("background: #0a0a0f; border-bottom: 1px solid #1e1e30;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 12, 20, 12)

        logo = QLabel("📰 يقين الصحفي")
        logo.setStyleSheet("font-size: 22px; font-weight: 800; color: #ff6b35;")
        header_layout.addWidget(logo)

        subtitle = QLabel("منصة الأخبار المغربية · 140+ مصدر RSS")
        subtitle.setStyleSheet("font-size: 13px; color: #8888a0; margin-left: 12px;")
        header_layout.addWidget(subtitle)

        header_layout.addStretch()

        self.refresh_btn = QPushButton("⟳ تحديث")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: #ff6b35; border: none;
                color: white; padding: 8px 24px;
                border-radius: 8px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: #e55a2b; }
        """)
        self.refresh_btn.clicked.connect(self._refresh_news)
        header_layout.addWidget(self.refresh_btn)

        self.source_count = QLabel("")
        self.source_count.setStyleSheet("color: #8888a0; font-size: 12px; margin-left: 12px;")
        header_layout.addWidget(self.source_count)

        main_layout.addWidget(header)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)

        self.news_list = NewsListView()
        self.news_list.article_selected.connect(self._on_article_selected)
        splitter.addWidget(self.news_list)

        self.article_view = ArticleView()
        splitter.addWidget(self.article_view)

        splitter.setSizes([450, 950])
        main_layout.addWidget(splitter, 1)

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STATUS_BAR_STYLE)
        self.status_label = QLabel("جاهز")
        self.status_bar.addWidget(self.status_label)
        self.setStatusBar(self.status_bar)

        auto_refresh = QTimer()
        auto_refresh.timeout.connect(self._auto_refresh)
        auto_refresh.start(300000)
        self.auto_refresh = auto_refresh

    def _load_news(self):
        self.status_label.setText("جاري تحميل الأخبار من 140+ مصدر RSS...")
        self.refresh_btn.setEnabled(False)

        try:
            from rss_service import get_cached_news, fetch_all_news
            cached = get_cached_news()
            if cached:
                self.articles = cached
                self.news_list.set_articles(self.articles)
                self.status_label.setText(f"✅ {len(self.articles)} خبر من الذاكرة المؤقتة")
                self.source_count.setText(f"المصادر: {len(cached)} خبر")

            self.fetcher = NewsFetcher()
            self.fetcher.finished.connect(self._on_news_loaded)
            self.fetcher.error.connect(self._on_news_error)
            self.fetcher.start()
        except Exception as e:
            self.status_label.setText(f"خطأ في التحميل: {e}")
            self.refresh_btn.setEnabled(True)

    def _on_news_loaded(self, articles):
        self.articles = articles
        self.news_list.set_articles(articles)
        self.refresh_btn.setEnabled(True)

        from rss_sources import TOTAL_SOURCES
        self.status_label.setText(f"✅ {len(articles)} خبر من {TOTAL_SOURCES} مصدر RSS")
        self.source_count.setText(f"المصادر: {TOTAL_SOURCES} · الأخبار: {len(articles)}")

    def _on_news_error(self, err):
        self.status_label.setText(f"خطأ: {err}")
        self.refresh_btn.setEnabled(True)

    def _on_article_selected(self, article):
        self.article_view.show_article(article)
        self.status_label.setText(f"عرض: {article.get('title', '')[:60]}...")

    def _refresh_news(self):
        self.articles = []
        self.news_list.set_articles([])
        self._load_news()

    def _auto_refresh(self):
        try:
            from rss_service import fetch_all_news
            fetch_all_news(force=True)
        except:
            pass
