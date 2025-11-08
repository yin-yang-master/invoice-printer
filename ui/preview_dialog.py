from datetime import datetime

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import (
    QFont,
    QImage,
    QPageLayout,
    QPageSize,
    QPixmap,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextLength,
    QTextTableFormat,
    QWheelEvent,
)
from PySide6.QtPrintSupport import QPrintDialog, QPrintPreviewWidget, QPrinter
from PySide6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QVBoxLayout

from models.database import Database


class ZoomablePrintPreviewWidget(QPrintPreviewWidget):
    """Print preview widget with mouse wheel zoom support"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_factor = 1.0

    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming"""
        if event.modifiers() == Qt.ControlModifier:
            # Zoom with Ctrl + wheel
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoomIn()
            else:
                self.zoomOut()
            event.accept()
        else:
            # Normal scrolling
            super().wheelEvent(event)


class PreviewDialog(QDialog):
    """Preview dialog for invoice"""

    def __init__(self, invoice_data: list, customer_info: dict = None, invoice_type: str = "", parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.customer_info = customer_info or {}
        self.invoice_type = invoice_type
        self.db = Database()
        self.settings = self.db.get_settings()
        self.document = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Xem trước hóa đơn")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # Print preview widget with zoom support
        self.preview_widget = ZoomablePrintPreviewWidget()
        self.preview_widget.paintRequested.connect(self.print_preview)
        layout.addWidget(self.preview_widget)

        # Buttons
        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        print_btn = QPushButton("Xuất hóa đơn")
        print_btn.clicked.connect(self.print_invoice)
        button_layout.addWidget(print_btn)

        layout.addLayout(button_layout)

    def apply_text_format(self, cursor: QTextCursor, text: str, settings_prefix: str):
        """Apply text formatting based on settings"""
        char_format = QTextCharFormat()

        bold = self.settings.get(f"{settings_prefix}_bold", False)
        italic = self.settings.get(f"{settings_prefix}_italic", False)
        underline = self.settings.get(f"{settings_prefix}_underline", False)
        fontsize = self.settings.get(f"{settings_prefix}_fontsize", 12)

        font = QFont()
        font.setPointSize(fontsize)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(underline)

        char_format.setFont(font)
        cursor.setCharFormat(char_format)
        cursor.insertText(text)

    def generate_preview(self):
        """Generate invoice preview"""
        document = QTextDocument()
        cursor = QTextCursor(document)

        # Header table with logo and store info (2 columns)
        header_format = QTextTableFormat()
        header_format.setBorder(0)
        header_format.setCellPadding(5)
        header_format.setCellSpacing(0)
        header_format.setWidth(QTextLength(QTextLength.PercentageLength, 100))
        
        header_table = cursor.insertTable(1, 2, header_format)
        
        # Left column - Logo
        logo_data = self.settings.get("logo")
        if logo_data:
            cell = header_table.cellAt(0, 0)
            cell_cursor = cell.firstCursorPosition()
            
            # Load image from binary data
            image = QImage()
            image.loadFromData(QByteArray(logo_data))
            
            # Scale image to fit
            if not image.isNull():
                scaled_image = image.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                document.addResource(QTextDocument.ImageResource, "logo", scaled_image)
                
                cell_block_format = cell_cursor.blockFormat()
                cell_block_format.setAlignment(Qt.AlignCenter)
                cell_cursor.setBlockFormat(cell_block_format)
                
                image_format = QTextCharFormat()
                cell_cursor.insertImage("logo")
        
        # Right column - Store info (centered)
        cell = header_table.cellAt(0, 1)
        cell_cursor = cell.firstCursorPosition()
        
        # Store name
        if self.settings.get("store_name_use"):
            cell_block_format = cell_cursor.blockFormat()
            cell_block_format.setAlignment(Qt.AlignHCenter)
            cell_cursor.setBlockFormat(cell_block_format)
            self.apply_text_format(cell_cursor, self.settings.get("store_name", ""), "store_name")
            cell_cursor.insertBlock()
        
        # Description
        if self.settings.get("description_use"):
            cell_block_format = cell_cursor.blockFormat()
            cell_block_format.setAlignment(Qt.AlignHCenter)
            cell_cursor.setBlockFormat(cell_block_format)
            self.apply_text_format(cell_cursor, self.settings.get("description", ""), "description")
            cell_cursor.insertBlock()
        
        # Address
        if self.settings.get("address_use"):
            cell_block_format = cell_cursor.blockFormat()
            cell_block_format.setAlignment(Qt.AlignHCenter)
            cell_cursor.setBlockFormat(cell_block_format)
            self.apply_text_format(cell_cursor, self.settings.get("address", ""), "address")
            cell_cursor.insertBlock()
        
        # Phone
        if self.settings.get("phone_use"):
            cell_block_format = cell_cursor.blockFormat()
            cell_block_format.setAlignment(Qt.AlignHCenter)
            cell_cursor.setBlockFormat(cell_block_format)
            phone_text = self.settings.get("phone", "")
            self.apply_text_format(cell_cursor, f"SĐT: {phone_text}", "phone")
        
        # Move cursor after header table
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()

        # Invoice type (centered)
        if self.invoice_type:
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignHCenter)
            cursor.setBlockFormat(block_format)
            
            self.apply_text_format(cursor, self.invoice_type, "invoice_type")
            cursor.insertBlock()

        cursor.insertBlock()

        # Customer info (left aligned)
        block_format = cursor.blockFormat()
        block_format.setAlignment(Qt.AlignLeft)
        cursor.setBlockFormat(block_format)
        
        # Customer name
        if self.customer_info.get("name"):
            customer_name_label = self.settings.get("customer_name", "Khách hàng:")
            self.apply_text_format(cursor, f"{customer_name_label} {self.customer_info.get('name')}", "customer_name")
            cursor.insertBlock()
        
        # Customer address
        if self.customer_info.get("address"):
            customer_address_label = self.settings.get("customer_address", "Địa chỉ:")
            self.apply_text_format(cursor, f"{customer_address_label} {self.customer_info.get('address')}", "customer_address")
            cursor.insertBlock()
        
        if self.customer_info.get("name") or self.customer_info.get("address"):
            cursor.insertBlock()

        # Table
        table_fontsize = self.settings.get("table_fontsize", 10)

        # Create table
        table_format = QTextTableFormat()
        table_format.setBorderStyle(QTextTableFormat.BorderStyle_Solid)
        table_format.setCellPadding(5)
        table_format.setCellSpacing(0)
        table_format.setWidth(QTextLength(QTextLength.PercentageLength, 100))
        table_format.setAlignment(Qt.AlignLeft)

        # Calculate totals
        total_quantity = 0
        total_price = 0
        total_amount = 0

        valid_items = []
        for item in self.invoice_data:
            try:
                qty = float(item["quantity"]) if item["quantity"] else 0
                price = float(item["unit_price"]) if item["unit_price"] else 0
                if qty > 0 and price > 0:
                    amount = qty * price
                    valid_items.append(
                        {
                            "name": item["product_name"],
                            "quantity": qty,
                            "price": price,
                            "amount": amount,
                        }
                    )
                    total_quantity += qty
                    total_price += price
                    total_amount += amount
            except ValueError:
                continue

        # Calculate tax
        tax_use = self.settings.get("tax_use", True)
        tax_percentage = self.settings.get("tax_percentage", 0)
        tax_name = self.settings.get("tax_name", "")
        
        # Create table with rows
        # +1 for header, +1 for product total, +1 for tax (if used and > 0), +1 for final total
        # If no tax: header + items + product total + final total (same value) = need 3 rows
        # If has tax: header + items + product total + tax + final total = need 4 rows
        has_tax = tax_use and tax_percentage > 0
        extra_rows = 4 if has_tax else 3
        num_rows = len(valid_items) + extra_rows
        table = cursor.insertTable(num_rows, 5, table_format)

        # Set font for table
        table_font = QFont()
        table_font.setPointSize(table_fontsize)

        # Header row
        header_format = QTextCharFormat()
        header_font = QFont()
        header_font.setPointSize(table_fontsize)
        header_font.setBold(True)
        header_format.setFont(header_font)

        headers = ["STT", "Sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"]
        for col, header in enumerate(headers):
            cell = table.cellAt(0, col)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText(header)

        # Data rows
        normal_format = QTextCharFormat()
        normal_format.setFont(table_font)

        for row, item in enumerate(valid_items, start=1):
            # STT
            cell = table.cellAt(row, 0)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(str(row))

            # Product name
            cell = table.cellAt(row, 1)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(item["name"])

            # Quantity
            cell = table.cellAt(row, 2)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(f"{item['quantity']:.0f}")

            # Unit price
            cell = table.cellAt(row, 3)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(f"{item['price']:,.0f}")

            # Amount
            cell = table.cellAt(row, 4)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(f"{item['amount']:,.0f}")

        # Product total row (Tổng giá trị sản phẩm)
        current_row = len(valid_items) + 1

        # Empty STT
        cell = table.cellAt(current_row, 0)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText("")

        # "Tổng giá trị sản phẩm"
        cell = table.cellAt(current_row, 1)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText("Tổng giá trị sản phẩm")

        # Total quantity
        cell = table.cellAt(current_row, 2)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_quantity:.0f}")

        # Total price
        cell = table.cellAt(current_row, 3)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_price:,.0f}")

        # Total amount
        cell = table.cellAt(current_row, 4)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_amount:,.0f}")

        # Tax row (if tax is used and > 0)
        if has_tax:
            current_row += 1
            tax_amount = total_amount * (tax_percentage / 100)
            
            # Empty STT
            cell = table.cellAt(current_row, 0)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText("")
            
            # Tax name with value
            cell = table.cellAt(current_row, 1)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(f"{tax_name} ({tax_percentage:.0f}%)")
            
            # Empty quantity
            cell = table.cellAt(current_row, 2)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText("")
            
            # Empty unit price
            cell = table.cellAt(current_row, 3)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText("")
            
            # Tax amount
            cell = table.cellAt(current_row, 4)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(normal_format)
            cell_cursor.insertText(f"{tax_amount:,.0f}")
            
            # Final total row (Tổng cộng)
            current_row += 1
            total_with_tax = total_amount + tax_amount
            
            # Empty STT
            cell = table.cellAt(current_row, 0)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # "Tổng cộng"
            cell = table.cellAt(current_row, 1)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("Tổng cộng")
            
            # Empty quantity
            cell = table.cellAt(current_row, 2)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # Empty unit price
            cell = table.cellAt(current_row, 3)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # Total with tax
            cell = table.cellAt(current_row, 4)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText(f"{total_with_tax:,.0f}")
        else:
            # If no tax, just rename current total to "Tổng cộng"
            current_row += 1
            
            # Empty STT
            cell = table.cellAt(current_row, 0)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # "Tổng cộng"
            cell = table.cellAt(current_row, 1)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("Tổng cộng")
            
            # Empty quantity
            cell = table.cellAt(current_row, 2)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # Empty unit price
            cell = table.cellAt(current_row, 3)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText("")
            
            # Total amount (same as product total)
            cell = table.cellAt(current_row, 4)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.setCharFormat(header_format)
            cell_cursor.insertText(f"{total_amount:,.0f}")

        # Move cursor after table
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()

        # Date (right aligned)
        now = datetime.now()
        date_str = f"Ngày {now.day} tháng {now.month} năm {now.year}"
        
        block_format = cursor.blockFormat()
        block_format.setAlignment(Qt.AlignRight)
        cursor.setBlockFormat(block_format)
        
        # Apply date formatting
        date_format = QTextCharFormat()
        date_font = QFont()
        date_font.setPointSize(self.settings.get("date_fontsize", 10))
        date_font.setBold(self.settings.get("date_bold", False))
        date_font.setItalic(self.settings.get("date_italic", False))
        date_font.setUnderline(self.settings.get("date_underline", False))
        date_format.setFont(date_font)
        cursor.setCharFormat(date_format)
        cursor.insertText(date_str)
        
        cursor.insertBlock()
        cursor.insertBlock()

        # Signature table - 2 columns for customer and creator
        signature_format = QTextTableFormat()
        signature_format.setBorder(0)  # No border
        signature_format.setCellPadding(5)
        signature_format.setCellSpacing(0)
        signature_format.setWidth(QTextLength(QTextLength.PercentageLength, 100))
        
        signature_table = cursor.insertTable(1, 2, signature_format)
        
        # Signature text format
        signature_text_format = QTextCharFormat()
        signature_font = QFont()
        signature_font.setPointSize(self.settings.get("signature_fontsize", 10))
        signature_font.setBold(self.settings.get("signature_bold", False))
        signature_font.setItalic(self.settings.get("signature_italic", False))
        signature_font.setUnderline(self.settings.get("signature_underline", False))
        signature_text_format.setFont(signature_font)
        
        # Customer column (left)
        cell = signature_table.cellAt(0, 0)
        cell_cursor = cell.firstCursorPosition()
        cell_block_format = cell_cursor.blockFormat()
        cell_block_format.setAlignment(Qt.AlignHCenter)
        cell_cursor.setBlockFormat(cell_block_format)
        cell_cursor.setCharFormat(signature_text_format)
        cell_cursor.insertText("Khách hàng")
        
        # Creator column (right)
        cell = signature_table.cellAt(0, 1)
        cell_cursor = cell.firstCursorPosition()
        cell_block_format = cell_cursor.blockFormat()
        cell_block_format.setAlignment(Qt.AlignHCenter)
        cell_cursor.setBlockFormat(cell_block_format)
        cell_cursor.setCharFormat(signature_text_format)
        cell_cursor.insertText("Người tạo")

        return document

    def print_preview(self, printer):
        """Render document for preview"""
        if self.document is None:
            self.document = self.generate_preview()
        
        self.document.print_(printer)

    def print_invoice(self):
        """Print the invoice"""
        printer = QPrinter(QPrinter.HighResolution)

        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.Accepted:
            if self.document:
                self.document.print_(printer)
            self.accept()
