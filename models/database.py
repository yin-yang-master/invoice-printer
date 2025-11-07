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
                store_name TEXT,
                store_name_use BOOLEAN DEFAULT 1,
                store_name_bold BOOLEAN DEFAULT 0,
                store_name_italic BOOLEAN DEFAULT 0,
                store_name_underline BOOLEAN DEFAULT 0,
                store_name_fontsize INTEGER DEFAULT 12,
                
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
                
                tax_name TEXT,
                tax_percentage REAL DEFAULT 0,
                
                table_fontsize INTEGER DEFAULT 10
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
                ("Cá»­a hÃ ng máº«u", "Äá»‹a chá»‰ máº«u", "0123456789", "VAT", 10.0, 10),
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
                "store_name",
                "store_name_use",
                "store_name_bold",
                "store_name_italic",
                "store_name_underline",
                "store_name_fontsize",
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
                "tax_name",
                "tax_percentage",
                "table_fontsize",
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
                store_name = ?,
                store_name_use = ?,
                store_name_bold = ?,
                store_name_italic = ?,
                store_name_underline = ?,
                store_name_fontsize = ?,
                
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
                
                tax_name = ?,
                tax_percentage = ?,
                table_fontsize = ?
            WHERE id = (SELECT MAX(id) FROM settings)
        """,
            (
                settings.get("store_name", ""),
                settings.get("store_name_use", True),
                settings.get("store_name_bold", False),
                settings.get("store_name_italic", False),
                settings.get("store_name_underline", False),
                settings.get("store_name_fontsize", 12),
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
                settings.get("tax_name", ""),
                settings.get("tax_percentage", 0.0),
                settings.get("table_fontsize", 10),
            ),
        )

        conn.commit()
        conn.close()
