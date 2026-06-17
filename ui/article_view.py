from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QComboBox, QProgressBar, QScrollArea, QFrame, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QTextCursor
import time

LANG_OPTIONS = [
    ("ar", "العربية"),
    ("fr", "Français"),
    ("en", "English"),
]

class ArticleLoader(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            import sys
            sys.path.insert(0, ".")
            from article_service import extract_article
            result = extract_article(self.url)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class RewriteWorker(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, text, lang):
        super().__init__()
        self.text = text
        self.lang = lang

    def run(self):
        try:
            import sys
            sys.path.insert(0, ".")
            from rewriter_service import rewrite_article
            self.progress.emit(50)
            result = rewrite_article(self.text, self.lang)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(f"[خطأ في إعادة الصياغة: {e}]")


class ArticleView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_article = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.title_label = QLabel("اختر خبراً لعرضه")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #e8e8ee; line-height: 1.3;")
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(16)

        self.source_label = QLabel("")
        self.source_label.setStyleSheet("color: #8888a0; font-size: 13px;")
        meta_layout.addWidget(self.source_label)

        self.lang_label = QLabel("")
        self.lang_label.setStyleSheet("""
            padding: 2px 12px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        """)
        meta_layout.addWidget(self.lang_label)

        self.open_btn = QPushButton("فتح الرابط الأصلي")
        self.open_btn.setStyleSheet("""
            QPushButton {
                background: #1e1e30; border: 1px solid #2a2a40;
                color: #e8e8ee; padding: 6px 16px;
                border-radius: 8px; font-size: 12px;
            }
            QPushButton:hover { border-color: #ff6b35; }
        """)
        self.open_btn.clicked.connect(self._open_original)
        meta_layout.addWidget(self.open_btn)

        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        original_scroll = QScrollArea()
        original_scroll.setWidgetResizable(True)
        original_scroll.setFrameShape(QFrame.NoFrame)

        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)
        original_layout.setContentsMargins(0, 0, 0, 0)

        original_header = QLabel("النص الأصلي")
        original_header.setStyleSheet("font-size: 14px; font-weight: 600; color: #f59e0b; margin-bottom: 4px;")
        original_layout.addWidget(original_header)

        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setPlaceholderText("سيظهر النص الأصلي هنا بعد تحميل المقال...")
        self.original_text.setMinimumWidth(300)
        original_layout.addWidget(self.original_text)

        self.load_progress = QProgressBar()
        self.load_progress.setVisible(False)
        original_layout.addWidget(self.load_progress)

        original_scroll.setWidget(original_container)
        splitter.addWidget(original_scroll)

        rewrite_scroll = QScrollArea()
        rewrite_scroll.setWidgetResizable(True)
        rewrite_scroll.setFrameShape(QFrame.NoFrame)

        rewrite_container = QWidget()
        rewrite_layout = QVBoxLayout(rewrite_container)
        rewrite_layout.setContentsMargins(0, 0, 0, 0)

        rewrite_header = QLabel("إعادة الصياغة الصحفية")
        rewrite_header.setStyleSheet("font-size: 14px; font-weight: 600; color: #ff6b35; margin-bottom: 4px;")
        rewrite_layout.addWidget(rewrite_header)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        controls_layout.addWidget(QLabel("الصياغة إلى:"))
        self.lang_combo = QComboBox()
        for val, label in LANG_OPTIONS:
            self.lang_combo.addItem(label, val)
        controls_layout.addWidget(self.lang_combo)

        self.rewrite_btn = QPushButton("⟳ إعادة الصياغة")
        self.rewrite_btn.setObjectName("primaryBtn")
        self.rewrite_btn.clicked.connect(self._do_rewrite)
        controls_layout.addWidget(self.rewrite_btn)

        self.copy_btn = QPushButton("نسخ النتيجة")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background: #1e1e30; border: 1px solid #2a2a40;
                color: #e8e8ee; padding: 8px 18px;
                border-radius: 8px; font-size: 13px;
            }
            QPushButton:hover { border-color: #10b981; color: #10b981; }
        """)
        self.copy_btn.clicked.connect(self._copy_result)
        controls_layout.addWidget(self.copy_btn)

        controls_layout.addStretch()
        rewrite_layout.addLayout(controls_layout)

        self.rewritten_text = QTextEdit()
        self.rewritten_text.setReadOnly(True)
        self.rewritten_text.setPlaceholderText("انقر 'إعادة الصياغة' لتوليد نسخة صحفية احترافية...")
        self.rewritten_text.setMinimumWidth(300)
        rewrite_layout.addWidget(self.rewritten_text)

        self.rewrite_progress = QProgressBar()
        self.rewrite_progress.setVisible(False)
        rewrite_layout.addWidget(self.rewrite_progress)

        rewrite_scroll.setWidget(rewrite_container)
        splitter.addWidget(rewrite_scroll)

        splitter.setSizes([400, 400])
        layout.addWidget(splitter, 1)

    def show_article(self, article):
        self.current_article = article
        self.title_label.setText(article.get("title", ""))
        self.source_label.setText(f"📰 {article.get('source_name', '')}")

        lang = article.get("lang", "en")
        lang_colors = {"ar": "#f59e0b", "fr": "#3b82f6", "en": "#10b981"}
        lang_names = {"ar": "العربية", "fr": "Français", "en": "English"}
        color = lang_colors.get(lang, "#8888a0")
        self.lang_label.setText(lang_names.get(lang, lang.upper()))
        self.lang_label.setStyleSheet(f"""
            background: {color}22; color: {color};
            padding: 2px 12px; border-radius: 10px;
            font-size: 11px; font-weight: 600;
        """)

        self.original_text.clear()
        self.rewritten_text.clear()

        summary = article.get("summary", "")
        if summary:
            self.original_text.setPlainText(summary)
            idx = 0
            for val, _ in LANG_OPTIONS:
                if val == lang:
                    self.lang_combo.setCurrentIndex(idx)
                    break
                idx += 1

        self.load_progress.setVisible(True)
        self.load_progress.setValue(10)
        self.loader = ArticleLoader(article.get("link", ""))
        self.loader.finished.connect(self._on_article_loaded)
        self.loader.error.connect(self._on_load_error)
        self.loader.start()

    def _on_article_loaded(self, result):
        self.load_progress.setValue(100)
        self.load_progress.setVisible(False)
        text = result.get("text", "") or result.get("title", "")
        if text:
            self.original_text.setPlainText(text)
            if result.get("title"):
                self.title_label.setText(result["title"])

    def _on_load_error(self, err):
        self.load_progress.setVisible(False)
        summary = self.current_article.get("summary", "") if self.current_article else ""
        if not self.original_text.toPlainText() and summary:
            self.original_text.setPlainText(summary)

    def _do_rewrite(self):
        text = self.original_text.toPlainText().strip()
        if not text or len(text) < 50:
            self.rewritten_text.setPlainText("النص قصير جداً لإعادة الصياغة. اختر خبراً آخر.")
            return

        lang = self.lang_combo.currentData()
        self.rewrite_btn.setEnabled(False)
        self.rewrite_btn.setText("جاري إعادة الصياغة...")
        self.rewrite_progress.setVisible(True)
        self.rewrite_progress.setValue(10)

        self.worker = RewriteWorker(text, lang)
        self.worker.finished.connect(self._on_rewrite_done)
        self.worker.progress.connect(self.rewrite_progress.setValue)
        self.worker.start()

    def _on_rewrite_done(self, result):
        self.rewrite_btn.setEnabled(True)
        self.rewrite_btn.setText("⟳ إعادة الصياغة")
        self.rewrite_progress.setVisible(False)
        self.rewritten_text.setPlainText(result)

    def _copy_result(self):
        text = self.rewritten_text.toPlainText()
        if text:
            clip = self.window().clipboard() if hasattr(self.window(), 'clipboard') else None
            if clip:
                clip.setText(text)
            else:
                from PyQt5.QtWidgets import QApplication
                QApplication.clipboard().setText(text)

    def _open_original(self):
        if self.current_article:
            import webbrowser
            webbrowser.open(self.current_article.get("link", ""))
