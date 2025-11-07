from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFont,
    QPageLayout,
    QPageSize,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextTableFormat,
)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout

from models.database import Database


class PreviewDialog(QDialog):
    """Preview dialog for invoice"""

    def __init__(self, invoice_data: list, parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.db = Database()
        self.settings = self.db.get_settings()
        self.setup_ui()
        self.generate_preview()

    def setup_ui(self):
        self.setWindowTitle("Xem trÆ°á»›c hÃ³a Ä‘Æ¡n")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # Text edit for preview
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        layout.addWidget(self.preview_text)

        # Buttons
        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("Há»§y")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        print_btn = QPushButton("Xuáº¥t hÃ³a Ä‘Æ¡n")
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

        # Store name (centered)
        if self.settings.get("store_name_use"):
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignHCenter)
            cursor.setBlockFormat(block_format)

            self.apply_text_format(
                cursor, self.settings.get("store_name", ""), "store_name"
            )
            cursor.insertBlock()

        # Address (centered)
        if self.settings.get("address_use"):
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignHCenter)
            cursor.setBlockFormat(block_format)

            self.apply_text_format(cursor, self.settings.get("address", ""), "address")
            cursor.insertBlock()

        # Phone and Date row
        block_format = cursor.blockFormat()
        block_format.setAlignment(Qt.AlignLeft)
        cursor.setBlockFormat(block_format)

        # Current datetime
        now = datetime.now()
        datetime_str = now.strftime("%H:%M - %d/%m/%Y")

        if self.settings.get("phone_use"):
            phone_text = self.settings.get("phone", "")
            # Create a line with date on left and phone on right
            line = f"{datetime_str}".ljust(40) + f"SÄT: {phone_text}".rjust(40)
            cursor.insertText(line)
        else:
            cursor.insertText(datetime_str)

        cursor.insertBlock()
        cursor.insertBlock()

        # Table
        table_fontsize = self.settings.get("table_fontsize", 10)

        # Create table
        table_format = QTextTableFormat()
        table_format.setBorderStyle(QTextTableFormat.BorderStyle_Solid)
        table_format.setCellPadding(5)
        table_format.setCellSpacing(0)

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

        # Create table with rows
        num_rows = len(valid_items) + 2  # +1 for header, +1 for total
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

        headers = ["STT", "Sáº£n pháº©m", "Sá»‘ lÆ°á»£ng", "ÄÆ¡n giÃ¡", "ThÃ nh tiá»n"]
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

        # Total row
        total_row = len(valid_items) + 1

        # Empty STT
        cell = table.cellAt(total_row, 0)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText("")

        # "Tá»•ng cá»™ng"
        cell = table.cellAt(total_row, 1)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText("Tá»•ng cá»™ng")

        # Total quantity
        cell = table.cellAt(total_row, 2)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_quantity:.0f}")

        # Total price
        cell = table.cellAt(total_row, 3)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_price:,.0f}")

        # Total amount
        cell = table.cellAt(total_row, 4)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.setCharFormat(header_format)
        cell_cursor.insertText(f"{total_amount:,.0f}")

        # Move cursor after table
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()

        # Tax information
        tax_percentage = self.settings.get("tax_percentage", 0)
        if tax_percentage > 0:
            tax_name = self.settings.get("tax_name", "")
            tax_amount = total_amount * (tax_percentage / 100)
            total_with_tax = total_amount + tax_amount

            cursor.insertBlock()
            tax_text = f"Tá»•ng + Sá»‘ tiá»n thuáº¿ ({tax_percentage:.0f}% {tax_name}) = {total_with_tax:,.0f}"
            cursor.insertText(tax_text)

        cursor.insertBlock()
        cursor.insertBlock()

        # Seller and Buyer
        cursor.insertText("NgÆ°á»i bÃ¡n hÃ ng:".ljust(50) + "NgÆ°á»i mua hÃ ng:")

        self.preview_text.setDocument(document)

    def print_invoice(self):
        """Print the invoice"""
        printer = QPrinter(QPrinter.HighResolution)

        # Set page size to A5
        page_layout = QPageLayout()
        page_layout.setPageSize(QPageSize(QPageSize.A5))
        printer.setPageLayout(page_layout)

        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.Accepted:
            self.preview_text.document().print_(printer)
            self.accept()
