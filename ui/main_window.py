from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.about_tab import AboutTab
from ui.invoice_tab import InvoiceTab
from ui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Pháº§n má»m in hÃ³a Ä‘Æ¡n")
        self.resize(1000, 700)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.invoice_tab = InvoiceTab()
        self.settings_tab = SettingsTab()
        self.about_tab = AboutTab()

        # Add tabs
        self.tabs.addTab(self.invoice_tab, "Xuáº¥t hÃ³a Ä‘Æ¡n")
        self.tabs.addTab(self.settings_tab, "CÃ i Ä‘áº·t")
        self.tabs.addTab(self.about_tab, "ThÃ´ng tin")

        self.setCentralWidget(self.tabs)
