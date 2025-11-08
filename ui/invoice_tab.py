from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ProductRow(QWidget):
    """A single row for product input"""

    def __init__(self, row_number: int, delete_callback=None, parent=None):
        super().__init__(parent)
        self.row_number = row_number
        self.delete_callback = delete_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        # STT label
        self.stt_label = QLabel(f"{self.row_number}")
        self.stt_label.setFixedWidth(30)
        layout.addWidget(self.stt_label)

        # Product name
        self.product_name = QLineEdit()
        self.product_name.setPlaceholderText("Tên sản phẩm")
        layout.addWidget(self.product_name, 3)

        # Quantity
        self.quantity = QLineEdit()
        self.quantity.setPlaceholderText("Số lượng")
        layout.addWidget(self.quantity, 1)

        # Unit price
        self.unit_price = QLineEdit()
        self.unit_price.setPlaceholderText("Đơn giá")
        layout.addWidget(self.unit_price, 1)

        # Delete button
        self.delete_btn = QPushButton("Xóa")
        self.delete_btn.setFixedWidth(60)
        self.delete_btn.clicked.connect(self.on_delete)
        layout.addWidget(self.delete_btn)

    def on_delete(self):
        """Handle delete button click"""
        if self.delete_callback:
            self.delete_callback(self)

    def get_data(self):
        """Get row data"""
        return {
            "product_name": self.product_name.text(),
            "quantity": self.quantity.text(),
            "unit_price": self.unit_price.text(),
        }

    def update_row_number(self, number: int):
        """Update row number display"""
        self.row_number = number
        self.stt_label.setText(f"{number}")


class InvoiceTab(QWidget):
    """Invoice creation tab"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_rows = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Invoice type section
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Loại hóa đơn:"))
        self.invoice_type = QComboBox()
        self.invoice_type.addItems([
            "PHIẾU XUẤT HÓA ĐƠN KIÊM BẢO HÀNH",
            "HÓA ĐƠN BÁN LẺ",
            "PHIẾU XUẤT KHO"
        ])
        type_layout.addWidget(self.invoice_type, 1)
        type_layout.addStretch(2)
        main_layout.addLayout(type_layout)
        main_layout.addSpacing(10)

        # Customer info section
        customer_layout = QHBoxLayout()
        
        # Customer name
        customer_layout.addWidget(QLabel("Tên khách hàng:"))
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Nhập tên khách hàng")
        customer_layout.addWidget(self.customer_name, 1)
        
        # Customer address
        customer_layout.addWidget(QLabel("Địa chỉ:"))
        self.customer_address = QLineEdit()
        self.customer_address.setPlaceholderText("Nhập địa chỉ khách hàng")
        customer_layout.addWidget(self.customer_address, 2)
        
        main_layout.addLayout(customer_layout)
        main_layout.addSpacing(10)

        # Header labels
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("STT"), 0)

        product_label = QLabel("Tên sản phẩm")
        header_layout.addWidget(product_label, 3)

        quantity_label = QLabel("Số lượng")
        header_layout.addWidget(quantity_label, 1)

        price_label = QLabel("Đơn giá")
        header_layout.addWidget(price_label, 1)

        # Empty space for delete button column
        header_layout.addWidget(QLabel(""), 0)
        empty_label = QLabel("")
        empty_label.setFixedWidth(60)
        header_layout.addWidget(empty_label)

        main_layout.addLayout(header_layout)

        # Scroll area for product rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_widget = QWidget()
        self.rows_layout = QVBoxLayout(scroll_widget)
        self.rows_layout.setAlignment(Qt.AlignTop)

        # Add first row by default
        self.add_row()

        # Add row button (centered below rows, inside scroll area)
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        self.add_row_btn = QPushButton("Thêm")
        self.add_row_btn.clicked.connect(self.add_row)
        self.add_row_btn.setFixedWidth(100)
        add_button_layout.addWidget(self.add_row_btn)
        add_button_layout.addStretch()
        self.rows_layout.addLayout(add_button_layout)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Export invoice button
        self.export_btn = QPushButton("Xuất hóa đơn")
        self.export_btn.clicked.connect(self.export_invoice)
        self.export_btn.setFixedHeight(40)
        main_layout.addWidget(self.export_btn)

    def add_row(self):
        """Add a new product row"""
        row_number = len(self.product_rows) + 1
        row = ProductRow(row_number, delete_callback=self.delete_row)
        self.product_rows.append(row)

        # Insert row before the add button
        # The add button is the last item in rows_layout
        insert_index = self.rows_layout.count() - 1
        self.rows_layout.insertWidget(insert_index, row)

    def delete_row(self, row_widget):
        """Delete a product row"""
        # Don't delete if it's the last row
        if len(self.product_rows) <= 1:
            return

        # Remove from list and layout
        if row_widget in self.product_rows:
            self.product_rows.remove(row_widget)
            row_widget.deleteLater()

            # Update row numbers
            for i, row in enumerate(self.product_rows, start=1):
                row.update_row_number(i)

    def get_invoice_data(self):
        """Get all invoice data"""
        data = []
        for row in self.product_rows:
            row_data = row.get_data()
            # Only include rows with data
            if (
                row_data["product_name"]
                or row_data["quantity"]
                or row_data["unit_price"]
            ):
                data.append(row_data)
        return data

    def export_invoice(self):
        """Export invoice - this will be connected to preview dialog"""
        from ui.preview_dialog import PreviewDialog

        invoice_data = self.get_invoice_data()
        if not invoice_data:
            return

        customer_info = {
            "name": self.customer_name.text(),
            "address": self.customer_address.text()
        }
        
        invoice_type = self.invoice_type.currentText()

        dialog = PreviewDialog(invoice_data, customer_info, invoice_type, parent=self)
        dialog.exec()
