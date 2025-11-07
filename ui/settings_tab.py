from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from models.database import Database


class FieldSettings(QWidget):
    """Widget for a single field settings row"""

    def __init__(self, label_text: str, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        # Label
        label = QLabel(f"{self.label_text}:")
        label.setFixedWidth(120)
        layout.addWidget(label)

        # Text input
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input, 2)

        # Use checkbox
        self.use_checkbox = QCheckBox("Sá»­ dá»¥ng")
        self.use_checkbox.setChecked(True)
        layout.addWidget(self.use_checkbox)

        # Bold checkbox
        self.bold_checkbox = QCheckBox("In Ä‘áº­m")
        layout.addWidget(self.bold_checkbox)

        # Italic checkbox
        self.italic_checkbox = QCheckBox("In nghiÃªng")
        layout.addWidget(self.italic_checkbox)

        # Underline checkbox
        self.underline_checkbox = QCheckBox("Gáº¡ch chÃ¢n")
        layout.addWidget(self.underline_checkbox)

        # Font size
        layout.addWidget(QLabel("Font size:"))
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setMinimum(6)
        self.fontsize_spin.setMaximum(72)
        self.fontsize_spin.setValue(12)
        self.fontsize_spin.setFixedWidth(60)
        layout.addWidget(self.fontsize_spin)

    def get_data(self):
        """Get field data"""
        return {
            "text": self.text_input.text(),
            "use": self.use_checkbox.isChecked(),
            "bold": self.bold_checkbox.isChecked(),
            "italic": self.italic_checkbox.isChecked(),
            "underline": self.underline_checkbox.isChecked(),
            "fontsize": self.fontsize_spin.value(),
        }

    def set_data(self, data: dict):
        """Set field data"""
        self.text_input.setText(data.get("text", ""))
        self.use_checkbox.setChecked(data.get("use", True))
        self.bold_checkbox.setChecked(data.get("bold", False))
        self.italic_checkbox.setChecked(data.get("italic", False))
        self.underline_checkbox.setChecked(data.get("underline", False))
        self.fontsize_spin.setValue(data.get("fontsize", 12))


class SettingsTab(QWidget):
    """Settings tab"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Store info group
        store_group = QGroupBox("ThÃ´ng tin cá»­a hÃ ng")
        store_layout = QVBoxLayout(store_group)

        # Store name
        self.store_name = FieldSettings("TÃªn cá»­a hÃ ng")
        store_layout.addWidget(self.store_name)

        # Address
        self.address = FieldSettings("Äá»‹a chá»‰")
        store_layout.addWidget(self.address)

        # Phone
        self.phone = FieldSettings("Sá»‘ Ä‘iá»‡n thoáº¡i")
        store_layout.addWidget(self.phone)

        scroll_layout.addWidget(store_group)

        # Tax group
        tax_group = QGroupBox("Thuáº¿")
        tax_layout = QVBoxLayout(tax_group)

        tax_row = QHBoxLayout()
        tax_row.addWidget(QLabel("TÃªn thuáº¿:"))
        self.tax_name = QLineEdit()
        self.tax_name.setPlaceholderText("VD: VAT")
        tax_row.addWidget(self.tax_name)

        tax_row.addWidget(QLabel("Pháº§n trÄƒm:"))
        self.tax_percentage = QSpinBox()
        self.tax_percentage.setMinimum(0)
        self.tax_percentage.setMaximum(100)
        self.tax_percentage.setValue(0)
        self.tax_percentage.setSuffix("%")
        self.tax_percentage.setFixedWidth(100)
        tax_row.addWidget(self.tax_percentage)
        tax_row.addStretch()

        tax_layout.addLayout(tax_row)
        scroll_layout.addWidget(tax_group)

        # Table settings group
        table_group = QGroupBox("CÃ i Ä‘áº·t báº£ng")
        table_layout = QHBoxLayout(table_group)

        table_layout.addWidget(QLabel("Fontsize dá»¯ liá»‡u báº£ng:"))
        self.table_fontsize = QSpinBox()
        self.table_fontsize.setMinimum(6)
        self.table_fontsize.setMaximum(72)
        self.table_fontsize.setValue(10)
        self.table_fontsize.setFixedWidth(100)
        table_layout.addWidget(self.table_fontsize)
        table_layout.addStretch()

        scroll_layout.addWidget(table_group)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Save button
        save_btn = QPushButton("LÆ°u")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setFixedHeight(40)
        main_layout.addWidget(save_btn)

    def load_settings(self):
        """Load settings from database"""
        settings = self.db.get_settings()
        if settings:
            self.store_name.set_data(
                {
                    "text": settings.get("store_name", ""),
                    "use": settings.get("store_name_use", True),
                    "bold": settings.get("store_name_bold", False),
                    "italic": settings.get("store_name_italic", False),
                    "underline": settings.get("store_name_underline", False),
                    "fontsize": settings.get("store_name_fontsize", 12),
                }
            )

            self.address.set_data(
                {
                    "text": settings.get("address", ""),
                    "use": settings.get("address_use", True),
                    "bold": settings.get("address_bold", False),
                    "italic": settings.get("address_italic", False),
                    "underline": settings.get("address_underline", False),
                    "fontsize": settings.get("address_fontsize", 12),
                }
            )

            self.phone.set_data(
                {
                    "text": settings.get("phone", ""),
                    "use": settings.get("phone_use", True),
                    "bold": settings.get("phone_bold", False),
                    "italic": settings.get("phone_italic", False),
                    "underline": settings.get("phone_underline", False),
                    "fontsize": settings.get("phone_fontsize", 12),
                }
            )

            self.tax_name.setText(settings.get("tax_name", ""))
            self.tax_percentage.setValue(int(settings.get("tax_percentage", 0)))
            self.table_fontsize.setValue(settings.get("table_fontsize", 10))

    def save_settings(self):
        """Save settings to database"""
        store_data = self.store_name.get_data()
        address_data = self.address.get_data()
        phone_data = self.phone.get_data()

        settings = {
            "store_name": store_data["text"],
            "store_name_use": store_data["use"],
            "store_name_bold": store_data["bold"],
            "store_name_italic": store_data["italic"],
            "store_name_underline": store_data["underline"],
            "store_name_fontsize": store_data["fontsize"],
            "address": address_data["text"],
            "address_use": address_data["use"],
            "address_bold": address_data["bold"],
            "address_italic": address_data["italic"],
            "address_underline": address_data["underline"],
            "address_fontsize": address_data["fontsize"],
            "phone": phone_data["text"],
            "phone_use": phone_data["use"],
            "phone_bold": phone_data["bold"],
            "phone_italic": phone_data["italic"],
            "phone_underline": phone_data["underline"],
            "phone_fontsize": phone_data["fontsize"],
            "tax_name": self.tax_name.text(),
            "tax_percentage": float(self.tax_percentage.value()),
            "table_fontsize": self.table_fontsize.value(),
        }

        self.db.save_settings(settings)

        QMessageBox.information(self, "ThÃ nh cÃ´ng", "ÄÃ£ lÆ°u cÃ i Ä‘áº·t!")
