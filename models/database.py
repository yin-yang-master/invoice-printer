import sqlite3
from typing import Any, Dict, Optional


class Database:
    """Database handler for invoice printer settings"""

    def __init__(self, db_path: str = "invoice_settings.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logo BLOB,
                
                store_name TEXT,
                store_name_use BOOLEAN DEFAULT 1,
                store_name_bold BOOLEAN DEFAULT 0,
                store_name_italic BOOLEAN DEFAULT 0,
                store_name_underline BOOLEAN DEFAULT 0,
                store_name_fontsize INTEGER DEFAULT 12,
                
                description TEXT,
                description_use BOOLEAN DEFAULT 1,
                description_bold BOOLEAN DEFAULT 0,
                description_italic BOOLEAN DEFAULT 0,
                description_underline BOOLEAN DEFAULT 0,
                description_fontsize INTEGER DEFAULT 10,
                
                address TEXT,
                address_use BOOLEAN DEFAULT 1,
                address_bold BOOLEAN DEFAULT 0,
                address_italic BOOLEAN DEFAULT 0,
                address_underline BOOLEAN DEFAULT 0,
                address_fontsize INTEGER DEFAULT 12,
                
                phone TEXT,
                phone_use BOOLEAN DEFAULT 1,
                phone_bold BOOLEAN DEFAULT 0,
                phone_italic BOOLEAN DEFAULT 0,
                phone_underline BOOLEAN DEFAULT 0,
                phone_fontsize INTEGER DEFAULT 12,
                
                customer_name TEXT DEFAULT 'Khách hàng:',
                customer_name_bold BOOLEAN DEFAULT 0,
                customer_name_italic BOOLEAN DEFAULT 0,
                customer_name_underline BOOLEAN DEFAULT 0,
                customer_name_fontsize INTEGER DEFAULT 11,
                
                customer_address TEXT DEFAULT 'Địa chỉ:',
                customer_address_bold BOOLEAN DEFAULT 0,
                customer_address_italic BOOLEAN DEFAULT 0,
                customer_address_underline BOOLEAN DEFAULT 0,
                customer_address_fontsize INTEGER DEFAULT 11,
                
                invoice_type TEXT DEFAULT 'HÓA ĐƠN',
                invoice_type_bold BOOLEAN DEFAULT 1,
                invoice_type_italic BOOLEAN DEFAULT 0,
                invoice_type_underline BOOLEAN DEFAULT 0,
                invoice_type_fontsize INTEGER DEFAULT 14,
                
                tax_use BOOLEAN DEFAULT 1,
                tax_name TEXT,
                tax_percentage REAL DEFAULT 0,
                
                table_fontsize INTEGER DEFAULT 10,
                
                date_fontsize INTEGER DEFAULT 10,
                date_bold BOOLEAN DEFAULT 0,
                date_italic BOOLEAN DEFAULT 0,
                date_underline BOOLEAN DEFAULT 0,
                
                signature_fontsize INTEGER DEFAULT 10,
                signature_bold BOOLEAN DEFAULT 0,
                signature_italic BOOLEAN DEFAULT 0,
                signature_underline BOOLEAN DEFAULT 0
            )
        """
        )

        # Check if settings exist, if not create default
        cursor.execute("SELECT COUNT(*) FROM settings")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO settings (store_name, address, phone, tax_name, tax_percentage, table_fontsize)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                ("Cửa hàng mẫu", "Địa chỉ mẫu", "0123456789", "VAT", 10.0, 10),
            )

        conn.commit()
        conn.close()

    def get_settings(self) -> Optional[Dict[str, Any]]:
        """Get current settings"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM settings ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            columns = [
                "id",
                "logo",
                "store_name",
                "store_name_use",
                "store_name_bold",
                "store_name_italic",
                "store_name_underline",
                "store_name_fontsize",
                "description",
                "description_use",
                "description_bold",
                "description_italic",
                "description_underline",
                "description_fontsize",
                "address",
                "address_use",
                "address_bold",
                "address_italic",
                "address_underline",
                "address_fontsize",
                "phone",
                "phone_use",
                "phone_bold",
                "phone_italic",
                "phone_underline",
                "phone_fontsize",
                "customer_name",
                "customer_name_bold",
                "customer_name_italic",
                "customer_name_underline",
                "customer_name_fontsize",
                "customer_address",
                "customer_address_bold",
                "customer_address_italic",
                "customer_address_underline",
                "customer_address_fontsize",
                "invoice_type",
                "invoice_type_bold",
                "invoice_type_italic",
                "invoice_type_underline",
                "invoice_type_fontsize",
                "tax_use",
                "tax_name",
                "tax_percentage",
                "table_fontsize",
                "date_fontsize",
                "date_bold",
                "date_italic",
                "date_underline",
                "signature_fontsize",
                "signature_bold",
                "signature_italic",
                "signature_underline",
            ]
            return dict(zip(columns, row))
        return None

    def save_settings(self, settings: Dict[str, Any]):
        """Save settings to database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE settings SET
                logo = ?,
                
                store_name = ?,
                store_name_use = ?,
                store_name_bold = ?,
                store_name_italic = ?,
                store_name_underline = ?,
                store_name_fontsize = ?,
                
                description = ?,
                description_use = ?,
                description_bold = ?,
                description_italic = ?,
                description_underline = ?,
                description_fontsize = ?,
                
                address = ?,
                address_use = ?,
                address_bold = ?,
                address_italic = ?,
                address_underline = ?,
                address_fontsize = ?,
                
                phone = ?,
                phone_use = ?,
                phone_bold = ?,
                phone_italic = ?,
                phone_underline = ?,
                phone_fontsize = ?,
                
                customer_name = ?,
                customer_name_bold = ?,
                customer_name_italic = ?,
                customer_name_underline = ?,
                customer_name_fontsize = ?,
                
                customer_address = ?,
                customer_address_bold = ?,
                customer_address_italic = ?,
                customer_address_underline = ?,
                customer_address_fontsize = ?,
                
                invoice_type = ?,
                invoice_type_bold = ?,
                invoice_type_italic = ?,
                invoice_type_underline = ?,
                invoice_type_fontsize = ?,
                
                tax_use = ?,
                tax_name = ?,
                tax_percentage = ?,
                table_fontsize = ?,
                
                date_fontsize = ?,
                date_bold = ?,
                date_italic = ?,
                date_underline = ?,
                
                signature_fontsize = ?,
                signature_bold = ?,
                signature_italic = ?,
                signature_underline = ?
            WHERE id = (SELECT MAX(id) FROM settings)
        """,
            (
                settings.get("logo"),
                settings.get("store_name", ""),
                settings.get("store_name_use", True),
                settings.get("store_name_bold", False),
                settings.get("store_name_italic", False),
                settings.get("store_name_underline", False),
                settings.get("store_name_fontsize", 12),
                settings.get("description", ""),
                settings.get("description_use", True),
                settings.get("description_bold", False),
                settings.get("description_italic", False),
                settings.get("description_underline", False),
                settings.get("description_fontsize", 10),
                settings.get("address", ""),
                settings.get("address_use", True),
                settings.get("address_bold", False),
                settings.get("address_italic", False),
                settings.get("address_underline", False),
                settings.get("address_fontsize", 12),
                settings.get("phone", ""),
                settings.get("phone_use", True),
                settings.get("phone_bold", False),
                settings.get("phone_italic", False),
                settings.get("phone_underline", False),
                settings.get("phone_fontsize", 12),
                settings.get("customer_name", "Khách hàng:"),
                settings.get("customer_name_bold", False),
                settings.get("customer_name_italic", False),
                settings.get("customer_name_underline", False),
                settings.get("customer_name_fontsize", 11),
                settings.get("customer_address", "Địa chỉ:"),
                settings.get("customer_address_bold", False),
                settings.get("customer_address_italic", False),
                settings.get("customer_address_underline", False),
                settings.get("customer_address_fontsize", 11),
                settings.get("invoice_type", "HÓA ĐƠN"),
                settings.get("invoice_type_bold", True),
                settings.get("invoice_type_italic", False),
                settings.get("invoice_type_underline", False),
                settings.get("invoice_type_fontsize", 14),
                settings.get("tax_use", True),
                settings.get("tax_name", ""),
                settings.get("tax_percentage", 0.0),
                settings.get("table_fontsize", 10),
                settings.get("date_fontsize", 10),
                settings.get("date_bold", False),
                settings.get("date_italic", False),
                settings.get("date_underline", False),
                settings.get("signature_fontsize", 10),
                settings.get("signature_bold", False),
                settings.get("signature_italic", False),
                settings.get("signature_underline", False),
            ),
        )

        conn.commit()
        conn.close()
