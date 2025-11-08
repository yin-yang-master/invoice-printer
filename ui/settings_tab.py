from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
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


class CustomerFieldSettings(QWidget):
    """Widget for customer field settings without 'Use' checkbox"""

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

        # Bold checkbox
        self.bold_checkbox = QCheckBox("In đậm")
        layout.addWidget(self.bold_checkbox)

        # Italic checkbox
        self.italic_checkbox = QCheckBox("In nghiêng")
        layout.addWidget(self.italic_checkbox)

        # Underline checkbox
        self.underline_checkbox = QCheckBox("Gạch chân")
        layout.addWidget(self.underline_checkbox)

        # Font size
        layout.addWidget(QLabel("Font size:"))
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setMinimum(6)
        self.fontsize_spin.setMaximum(72)
        self.fontsize_spin.setValue(11)
        self.fontsize_spin.setFixedWidth(60)
        layout.addWidget(self.fontsize_spin)

    def get_data(self):
        """Get field data"""
        return {
            "text": self.text_input.text(),
            "bold": self.bold_checkbox.isChecked(),
            "italic": self.italic_checkbox.isChecked(),
            "underline": self.underline_checkbox.isChecked(),
            "fontsize": self.fontsize_spin.value(),
        }

    def set_data(self, data: dict):
        """Set field data"""
        self.text_input.setText(data.get("text", ""))
        self.bold_checkbox.setChecked(data.get("bold", False))
        self.italic_checkbox.setChecked(data.get("italic", False))
        self.underline_checkbox.setChecked(data.get("underline", False))
        self.fontsize_spin.setValue(data.get("fontsize", 11))


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
        self.use_checkbox = QCheckBox("Sử dụng")
        self.use_checkbox.setChecked(True)
        layout.addWidget(self.use_checkbox)

        # Bold checkbox
        self.bold_checkbox = QCheckBox("In đậm")
        layout.addWidget(self.bold_checkbox)

        # Italic checkbox
        self.italic_checkbox = QCheckBox("In nghiêng")
        layout.addWidget(self.italic_checkbox)

        # Underline checkbox
        self.underline_checkbox = QCheckBox("Gạch chân")
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

        # Logo group
        logo_group = QGroupBox("Logo")
        logo_layout = QVBoxLayout(logo_group)
        
        logo_btn_layout = QHBoxLayout()
        self.logo_btn = QPushButton("Chọn ảnh logo")
        self.logo_btn.clicked.connect(self.select_logo)
        logo_btn_layout.addWidget(self.logo_btn)
        
        self.clear_logo_btn = QPushButton("Xóa logo")
        self.clear_logo_btn.clicked.connect(self.clear_logo)
        logo_btn_layout.addWidget(self.clear_logo_btn)
        logo_layout.addLayout(logo_btn_layout)
        
        self.logo_preview = QLabel("Chưa có logo")
        self.logo_preview.setAlignment(Qt.AlignCenter)
        self.logo_preview.setFixedHeight(150)
        self.logo_preview.setStyleSheet("border: 1px solid #ccc; background: #f5f5f5;")
        logo_layout.addWidget(self.logo_preview)
        
        self.logo_data = None  # Store base64 or binary data
        
        scroll_layout.addWidget(logo_group)

        # Store info group
        store_group = QGroupBox("Thông tin cửa hàng")
        store_layout = QVBoxLayout(store_group)

        # Store name
        self.store_name = FieldSettings("Tên cửa hàng")
        store_layout.addWidget(self.store_name)

        # Description
        self.description = FieldSettings("Mô tả")
        store_layout.addWidget(self.description)

        # Address
        self.address = FieldSettings("Địa chỉ")
        store_layout.addWidget(self.address)

        # Phone
        self.phone = FieldSettings("Số điện thoại")
        store_layout.addWidget(self.phone)

        scroll_layout.addWidget(store_group)

        # Customer info group
        customer_group = QGroupBox("Thông tin khách hàng")
        customer_layout = QVBoxLayout(customer_group)

        # Customer name
        self.customer_name = CustomerFieldSettings("Tên khách hàng")
        customer_layout.addWidget(self.customer_name)

        # Customer address
        self.customer_address = CustomerFieldSettings("Địa chỉ khách hàng")
        customer_layout.addWidget(self.customer_address)

        scroll_layout.addWidget(customer_group)

        # Invoice type group
        invoice_type_group = QGroupBox("Loại hóa đơn")
        invoice_type_layout = QVBoxLayout(invoice_type_group)

        self.invoice_type = CustomerFieldSettings("Loại hóa đơn")
        invoice_type_layout.addWidget(self.invoice_type)

        scroll_layout.addWidget(invoice_type_group)

        # Tax group
        tax_group = QGroupBox("Thuế")
        tax_layout = QVBoxLayout(tax_group)

        tax_row = QHBoxLayout()
        
        self.tax_use = QCheckBox("Sử dụng")
        self.tax_use.setChecked(True)
        tax_row.addWidget(self.tax_use)
        
        tax_row.addWidget(QLabel("Tên thuế:"))
        self.tax_name = QLineEdit()
        self.tax_name.setPlaceholderText("VD: VAT")
        tax_row.addWidget(self.tax_name)

        tax_row.addWidget(QLabel("Phần trăm:"))
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
        table_group = QGroupBox("Cài đặt bảng")
        table_layout = QHBoxLayout(table_group)

        table_layout.addWidget(QLabel("Fontsize dữ liệu bảng:"))
        self.table_fontsize = QSpinBox()
        self.table_fontsize.setMinimum(6)
        self.table_fontsize.setMaximum(72)
        self.table_fontsize.setValue(10)
        self.table_fontsize.setFixedWidth(100)
        table_layout.addWidget(self.table_fontsize)
        table_layout.addStretch()

        scroll_layout.addWidget(table_group)

        # Date/Time settings
        date_group = QGroupBox("Cài đặt thời gian")
        date_layout = QHBoxLayout(date_group)
        
        date_layout.addWidget(QLabel("Fontsize:"))
        self.date_fontsize = QSpinBox()
        self.date_fontsize.setMinimum(6)
        self.date_fontsize.setMaximum(72)
        self.date_fontsize.setValue(10)
        self.date_fontsize.setFixedWidth(100)
        date_layout.addWidget(self.date_fontsize)
        
        self.date_bold = QCheckBox("In đậm")
        date_layout.addWidget(self.date_bold)
        
        self.date_italic = QCheckBox("In nghiêng")
        date_layout.addWidget(self.date_italic)
        
        self.date_underline = QCheckBox("Gạch chân")
        date_layout.addWidget(self.date_underline)
        
        date_layout.addStretch()
        scroll_layout.addWidget(date_group)

        # Signature settings
        signature_group = QGroupBox("Cài đặt chữ ký (Khách hàng, Người tạo)")
        signature_layout = QHBoxLayout(signature_group)
        
        signature_layout.addWidget(QLabel("Fontsize:"))
        self.signature_fontsize = QSpinBox()
        self.signature_fontsize.setMinimum(6)
        self.signature_fontsize.setMaximum(72)
        self.signature_fontsize.setValue(10)
        self.signature_fontsize.setFixedWidth(100)
        signature_layout.addWidget(self.signature_fontsize)
        
        self.signature_bold = QCheckBox("In đậm")
        signature_layout.addWidget(self.signature_bold)
        
        self.signature_italic = QCheckBox("In nghiêng")
        signature_layout.addWidget(self.signature_italic)
        
        self.signature_underline = QCheckBox("Gạch chân")
        signature_layout.addWidget(self.signature_underline)
        
        signature_layout.addStretch()
        scroll_layout.addWidget(signature_group)

        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Save button
        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setFixedHeight(40)
        main_layout.addWidget(save_btn)

    def load_settings(self):
        """Load settings from database"""
        settings = self.db.get_settings()
        if settings:
            # Load logo
            logo_data = settings.get("logo")
            if logo_data:
                self.logo_data = logo_data
                pixmap = QPixmap()
                pixmap.loadFromData(logo_data)
                scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_preview.setPixmap(scaled_pixmap)
                self.logo_preview.setText("")
            
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

            self.description.set_data(
                {
                    "text": settings.get("description", ""),
                    "use": settings.get("description_use", True),
                    "bold": settings.get("description_bold", False),
                    "italic": settings.get("description_italic", False),
                    "underline": settings.get("description_underline", False),
                    "fontsize": settings.get("description_fontsize", 10),
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

            self.customer_name.set_data(
                {
                    "text": settings.get("customer_name", "Khách hàng:"),
                    "bold": settings.get("customer_name_bold", False),
                    "italic": settings.get("customer_name_italic", False),
                    "underline": settings.get("customer_name_underline", False),
                    "fontsize": settings.get("customer_name_fontsize", 11),
                }
            )

            self.customer_address.set_data(
                {
                    "text": settings.get("customer_address", "Địa chỉ:"),
                    "bold": settings.get("customer_address_bold", False),
                    "italic": settings.get("customer_address_italic", False),
                    "underline": settings.get("customer_address_underline", False),
                    "fontsize": settings.get("customer_address_fontsize", 11),
                }
            )

            self.invoice_type.set_data(
                {
                    "text": settings.get("invoice_type", "HÓA ĐƠN"),
                    "bold": settings.get("invoice_type_bold", True),
                    "italic": settings.get("invoice_type_italic", False),
                    "underline": settings.get("invoice_type_underline", False),
                    "fontsize": settings.get("invoice_type_fontsize", 14),
                }
            )

            self.tax_use.setChecked(bool(settings.get("tax_use", True)))
            self.tax_name.setText(settings.get("tax_name", ""))
            self.tax_percentage.setValue(int(settings.get("tax_percentage", 0)))
            self.table_fontsize.setValue(int(settings.get("table_fontsize", 10)))
            
            # Load date settings
            self.date_fontsize.setValue(int(settings.get("date_fontsize", 10)))
            self.date_bold.setChecked(bool(settings.get("date_bold", False)))
            self.date_italic.setChecked(bool(settings.get("date_italic", False)))
            self.date_underline.setChecked(bool(settings.get("date_underline", False)))
            
            # Load signature settings
            self.signature_fontsize.setValue(int(settings.get("signature_fontsize", 10)))
            self.signature_bold.setChecked(bool(settings.get("signature_bold", False)))
            self.signature_italic.setChecked(bool(settings.get("signature_italic", False)))
            self.signature_underline.setChecked(bool(settings.get("signature_underline", False)))

    def save_settings(self):
        """Save settings to database"""
        store_data = self.store_name.get_data()
        description_data = self.description.get_data()
        address_data = self.address.get_data()
        phone_data = self.phone.get_data()
        customer_name_data = self.customer_name.get_data()
        customer_address_data = self.customer_address.get_data()
        invoice_type_data = self.invoice_type.get_data()

        settings = {
            "store_name": store_data["text"],
            "store_name_use": store_data["use"],
            "store_name_bold": store_data["bold"],
            "store_name_italic": store_data["italic"],
            "store_name_underline": store_data["underline"],
            "store_name_fontsize": store_data["fontsize"],
            "description": description_data["text"],
            "description_use": description_data["use"],
            "description_bold": description_data["bold"],
            "description_italic": description_data["italic"],
            "description_underline": description_data["underline"],
            "description_fontsize": description_data["fontsize"],
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
            "customer_name": customer_name_data["text"],
            "customer_name_bold": customer_name_data["bold"],
            "customer_name_italic": customer_name_data["italic"],
            "customer_name_underline": customer_name_data["underline"],
            "customer_name_fontsize": customer_name_data["fontsize"],
            "customer_address": customer_address_data["text"],
            "customer_address_bold": customer_address_data["bold"],
            "customer_address_italic": customer_address_data["italic"],
            "customer_address_underline": customer_address_data["underline"],
            "customer_address_fontsize": customer_address_data["fontsize"],
            "invoice_type": invoice_type_data["text"],
            "invoice_type_bold": invoice_type_data["bold"],
            "invoice_type_italic": invoice_type_data["italic"],
            "invoice_type_underline": invoice_type_data["underline"],
            "invoice_type_fontsize": invoice_type_data["fontsize"],
            "tax_use": self.tax_use.isChecked(),
            "tax_name": self.tax_name.text(),
            "tax_percentage": float(self.tax_percentage.value()),
            "table_fontsize": self.table_fontsize.value(),
            "date_fontsize": self.date_fontsize.value(),
            "date_bold": self.date_bold.isChecked(),
            "date_italic": self.date_italic.isChecked(),
            "date_underline": self.date_underline.isChecked(),
            "signature_fontsize": self.signature_fontsize.value(),
            "signature_bold": self.signature_bold.isChecked(),
            "signature_italic": self.signature_italic.isChecked(),
            "signature_underline": self.signature_underline.isChecked(),
        }

        # Add logo data
        settings["logo"] = self.logo_data

        self.db.save_settings(settings)

        QMessageBox.information(self, "Thành công", "Đã lưu cài đặt!")

    def select_logo(self):
        """Select logo image"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_name:
            with open(file_name, 'rb') as f:
                self.logo_data = f.read()
            
            # Show preview
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_preview.setPixmap(scaled_pixmap)
            self.logo_preview.setText("")

    def clear_logo(self):
        """Clear logo"""
        self.logo_data = None
        self.logo_preview.clear()
        self.logo_preview.setText("Chưa có logo")
