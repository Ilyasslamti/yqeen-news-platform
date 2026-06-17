from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette

LANG_CONFIG = {
    "all": {"label": "الكل", "color": "#7c3aed"},
    "ar": {"label": "العربية", "color": "#f59e0b"},
    "fr": {"label": "Français", "color": "#3b82f6"},
    "en": {"label": "English", "color": "#10b981"},
}

class NewsListItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, article, parent=None):
        super().__init__(parent)
        self.article = article
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        badge_layout = QHBoxLayout()
        badge_layout.setSpacing(8)

        lang = self.article.get("lang", "en")
        cfg = LANG_CONFIG.get(lang, LANG_CONFIG["en"])
        lang_tag = QLabel(cfg["label"])
        lang_tag.setStyleSheet(f"""
            background: {cfg['color']}22;
            color: {cfg['color']};
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        """)
        lang_tag.setFixedHeight(22)

        source = QLabel(self.article.get("source_name", ""))
        source.setStyleSheet("color: #8888a0; font-size: 11px; font-weight: 500;")

        badge_layout.addWidget(lang_tag)
        badge_layout.addWidget(source)
        badge_layout.addStretch()
        layout.addLayout(badge_layout)

        title = QLabel(self.article.get("title", ""))
        title.setWordWrap(True)
        title.setStyleSheet("color: #e8e8ee; font-size: 14px; font-weight: 600; line-height: 1.4;")
        title.setMaximumHeight(60)
        layout.addWidget(title)

        summary = QLabel(self.article.get("summary", "")[:200])
        summary.setWordWrap(True)
        summary.setStyleSheet("color: #8888a0; font-size: 12px; line-height: 1.5;")
        summary.setMaximumHeight(40)
        layout.addWidget(summary)

    def mousePressEvent(self, event):
        self.clicked.emit(self.article.get("id", ""))
        super().mousePressEvent(event)


class LangFilterBar(QWidget):
    lang_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active_lang = "all"
        self._buttons = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(8)

        for lang_key, cfg in LANG_CONFIG.items():
            btn = QPushButton(cfg["label"])
            btn.setCheckable(True)
            btn.setChecked(lang_key == "all")
            btn.setStyleSheet(self._btn_style(lang_key == "all", cfg["color"]))
            btn.clicked.connect(lambda checked, k=lang_key: self._on_click(k))
            self._buttons[lang_key] = btn
            layout.addWidget(btn)

        layout.addStretch()

    def _btn_style(self, active, color):
        if active:
            return f"""
                QPushButton {{
                    background: {color};
                    border: 1px solid {color};
                    color: white;
                    border-radius: 20px;
                    padding: 8px 20px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """
        return """
            QPushButton {
                background: #1e1e30;
                border: 1px solid #2a2a40;
                color: #8888a0;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                border-color: #ff6b35;
                color: #e8e8ee;
            }
        """

    def _on_click(self, lang_key):
        self._active_lang = lang_key
        for k, btn in self._buttons.items():
            cfg = LANG_CONFIG.get(k, LANG_CONFIG["en"])
            btn.setChecked(k == lang_key)
            btn.setStyleSheet(self._btn_style(k == lang_key, cfg["color"]))
        self.lang_changed.emit(lang_key)


class NewsListView(QWidget):
    article_selected = pyqtSignal(dict)
    refresh_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.articles = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        header = QLabel("الأخبار المغربية")
        header.setStyleSheet("font-size: 22px; font-weight: 800; color: #ff6b35; padding: 8px 0;")
        layout.addWidget(header)

        sub = QLabel("مجمعة من 140+ مصدر RSS")
        sub.setStyleSheet("font-size: 13px; color: #8888a0; margin-bottom: 4px;")
        layout.addWidget(sub)

        self.lang_filter = LangFilterBar()
        self.lang_filter.lang_changed.connect(self._filter_changed)
        layout.addWidget(self.lang_filter)

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(4)
        self.list_widget.setFrameShape(QFrame.NoFrame)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)

        self.status_label = QLabel("جاري تحميل الأخبار...")
        self.status_label.setStyleSheet("color: #8888a0; font-size: 12px; padding: 4px 0;")
        layout.addWidget(self.status_label)

    def set_articles(self, articles):
        self.articles = articles
        self._filter_changed(self.lang_filter._active_lang)

    def _filter_changed(self, lang):
        self.list_widget.clear()
        filtered = [a for a in self.articles if lang == "all" or a.get("lang") == lang]
        for a in filtered[:200]:
            item = QListWidgetItem()
            widget = NewsListItem(a)
            widget.clicked.connect(self._on_card_clicked)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        self.status_label.setText(f"{len(filtered)} خبر · {len(self.articles)} إجمالي")

    def _on_card_clicked(self, article_id):
        for a in self.articles:
            if a.get("id") == article_id:
                self.article_selected.emit(a)
                break

    def _on_item_clicked(self, item):
        widget = self.list_widget.itemWidget(item)
        if widget:
            self.article_selected.emit(widget.article)
