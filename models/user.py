import sqlite3
import hashlib

class User:
    def __init__(self, db_path="shop.db"):
        # Only one connection with timeout and row_factory
        self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('Cashier','Manager','Admin')) NOT NULL
        )
        """)
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, role="Cashier"):
        role = role if role in ("Cashier","Manager","Admin") else "Cashier"
        hashed = self.hash_password(password)
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            """, (username.strip(), hashed, role))
            self.conn.commit()
            print(f"✅ User '{username}' added with role '{role}'")
        except sqlite3.IntegrityError:
            print("❌ Username already exists.")

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username=?", (username.strip(),))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"🗑️ Deleted user '{username}'")
        else:
            print("❌ User not found.")

    def list_users(self):
        self.cursor.execute("SELECT id, username, role FROM users ORDER BY role, username")
        rows = self.cursor.fetchall()
        if not rows:
            print("No users found.")
            return
        print("\n👥 Users:")
        for r in rows:
            print(f"- {r['username']} ({r['role']})")

    def authenticate(self, username, password):
        hashed = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username.strip(), hashed))
        row = self.cursor.fetchone()
        if row:
            print(f"✅ Welcome {row['username']} ({row['role']})")
            return {"id": row["id"], "username": row["username"], "role": row["role"]}
        print("❌ Invalid credentials.")
        return None


