APP_STYLE = """
QMainWindow {
    background-color: #0a0a0f;
}
QWidget {
    font-family: 'Segoe UI', 'Tajawal', system-ui, sans-serif;
}
QLabel {
    color: #e8e8ee;
}
QPushButton {
    background-color: #1e1e30;
    color: #e8e8ee;
    border: 1px solid #2a2a40;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #2a2a40;
    border-color: #ff6b35;
}
QPushButton:pressed {
    background-color: #3a3a50;
}
QPushButton#primaryBtn {
    background-color: #ff6b35;
    border-color: #ff6b35;
    color: white;
}
QPushButton#primaryBtn:hover {
    background-color: #e55a2b;
}
QPushButton#dangerBtn {
    background-color: #dc2626;
    border-color: #dc2626;
    color: white;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #12121a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2a2a40;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #3a3a50;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QListWidget {
    background: #12121a;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    color: #e8e8ee;
    font-size: 14px;
    outline: none;
}
QListWidget::item {
    padding: 16px;
    border-bottom: 1px solid #1e1e30;
}
QListWidget::item:selected {
    background: #1e1e30;
    border-left: 3px solid #ff6b35;
}
QListWidget::item:hover {
    background: #181825;
}
QTextEdit {
    background: #12121a;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    color: #e8e8ee;
    padding: 16px;
    font-size: 14px;
    line-height: 1.7;
}
QTextEdit:focus {
    border-color: #ff6b35;
}
QComboBox {
    background: #1e1e30;
    border: 1px solid #2a2a40;
    border-radius: 8px;
    color: #e8e8ee;
    padding: 8px 16px;
    font-size: 13px;
    min-width: 120px;
}
QComboBox:hover {
    border-color: #ff6b35;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background: #1e1e30;
    border: 1px solid #2a2a40;
    color: #e8e8ee;
    selection-background-color: #ff6b35;
}
QSplitter::handle {
    background: #1e1e30;
    width: 2px;
}
QProgressBar {
    background: #1e1e30;
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    color: #e8e8ee;
    font-size: 10px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff6b35, stop:1 #7c3aed);
    border-radius: 6px;
}
"""

NEWS_CARD_STYLE = """
QFrame#newsCard {
    background: #12121a;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 16px;
}
QFrame#newsCard:hover {
    background: #181825;
    border-color: #ff6b35;
}
"""

STATUS_BAR_STYLE = """
QStatusBar {
    background: #0a0a0f;
    border-top: 1px solid #1e1e30;
    color: #8888a0;
    font-size: 12px;
    padding: 4px 12px;
}
"""
