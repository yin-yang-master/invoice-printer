from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutTab(QWidget):
    """About tab"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Author label
        author_label = QLabel("Author: Â© Ã‚m DÆ°Æ¡ng TiÃªn Sinh 2025")
        author_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        author_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(author_label)
