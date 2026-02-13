import sqlite3
from .product import Product  # relative import fixed

class Inventory:
    def __init__(self, db_path="shop.db"):
        # Only one connection with timeout and row_factory
        self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT,
            low_stock_threshold INTEGER DEFAULT 5,
            revenue REAL DEFAULT 0
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL DEFAULT 0,
            tax REAL DEFAULT 0,
            total_price REAL NOT NULL,
            payment_method TEXT,
            customer_id INTEGER,
            receipt_path TEXT,
            timestamp TEXT NOT NULL
        )
        """)
        self.conn.commit()

    # -------- inventory ops --------
    def add_product(self, name, price, quantity, category="General"):
        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, quantity, category)
                VALUES (?, ?, ?, ?)
            """, (name.strip(), float(price), int(quantity), category.strip()))
            self.conn.commit()
            print(f"✅ Added {name} (${price}, {quantity}) in '{category}'")
        except sqlite3.IntegrityError:
            self.cursor.execute("""
                UPDATE products SET quantity = quantity + ?, price = ?
                WHERE name = ?
            """, (int(quantity), float(price), name.strip()))
            self.conn.commit()
            print(f"✅ Updated {name}: quantity increased and price updated")

    def list_products(self):
        self.cursor.execute("SELECT * FROM products ORDER BY name")
        rows = self.cursor.fetchall()
        if not rows:
            print("Inventory is empty.")
            return
        print("\n📦 Inventory:")
        for row in rows:
            print(Product(row["id"], row["name"], row["price"], row["quantity"],
                          row["category"], row["low_stock_threshold"], row["revenue"]))

    def search_product(self, keyword):
        self.cursor.execute("SELECT * FROM products WHERE name LIKE ? ORDER BY name", (f"%{keyword}%",))
        rows = self.cursor.fetchall()
        if not rows:
            print("No products found.")
            return
        print(f"\n🔎 Search results for '{keyword}':")
        for row in rows:
            print(Product(row["id"], row["name"], row["price"], row["quantity"],
                          row["category"], row["low_stock_threshold"], row["revenue"]))

    def update_price(self, name, new_price):
        self.cursor.execute("UPDATE products SET price = ? WHERE name = ?", (float(new_price), name.strip()))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"✅ Updated {name} price to ${float(new_price):.2f}")
        else:
            print("❌ Product not found.")

    def find_product(self, name):
        self.cursor.execute("SELECT * FROM products WHERE name = ?", (name.strip(),))
        row = self.cursor.fetchone()
        return Product(row["id"], row["name"], row["price"], row["quantity"],
                       row["category"], row["low_stock_threshold"], row["revenue"]) if row else None


