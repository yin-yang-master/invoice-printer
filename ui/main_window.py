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
        self.setWindowTitle("Phần mềm in hóa đơn")
        self.resize(1000, 700)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.invoice_tab = InvoiceTab()
        self.settings_tab = SettingsTab()
        self.about_tab = AboutTab()

        # Add tabs
        self.tabs.addTab(self.invoice_tab, "Xuất hóa đơn")
        self.tabs.addTab(self.settings_tab, "Cài đặt")
        self.tabs.addTab(self.about_tab, "Thông tin")

        self.setCentralWidget(self.tabs)
