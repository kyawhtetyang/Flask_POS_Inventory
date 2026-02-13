import sqlite3

class Customer:
    def __init__(self, db_path="shop.db"):
        # Fix: allow multi-thread access
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
        """)
        self.conn.commit()

    def add_customer(self, name, phone=None, email=None):
        self.cursor.execute("""
            INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)
        """, (name.strip(), (phone or "").strip(), (email or "").strip()))
        self.conn.commit()
        print(f"✅ Added customer '{name}'")

    def list_customers(self):
        self.cursor.execute("SELECT * FROM customers ORDER BY name")
        rows = self.cursor.fetchall()
        return rows  # Return instead of print for template

    def find_customer_id(self, name):
        self.cursor.execute("SELECT id FROM customers WHERE name=?", (name.strip(),))
        row = self.cursor.fetchone()
        return row["id"] if row else None


