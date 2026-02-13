import os
from datetime import datetime
from .inventory import Inventory

RECEIPT_DIR = "receipts"

class Sale:
    def __init__(self, inventory_obj):
        self.inventory = inventory_obj
        self.conn = inventory_obj.conn
        self.cursor = inventory_obj.cursor
        os.makedirs(RECEIPT_DIR, exist_ok=True)

    def sell_product(self, items, discount=0.0, tax=0.0, payment_method="Cash", customer_id=None):
        """
        items: list of tuples [(product_name, quantity)]
        """
        sold_items = []
        gross_total = 0.0

        # Validate and compute
        for name, qty in items:
            product = self.inventory.find_product(name)
            if not product:
                print(f"❌ Product '{name}' not found.")
                continue
            if qty <= 0:
                print(f"❌ Invalid quantity for '{name}'.")
                continue
            if qty > product.quantity:
                print(f"❌ Not enough stock for '{name}'. Available: {product.quantity}")
                continue

            subtotal = product.price * qty
            gross_total += subtotal
            sold_items.append((product, qty, product.price, subtotal))

        if not sold_items:
            print("❌ No valid items to sell.")
            return False

        # Compute totals
        discount = float(discount or 0)
        tax = float(tax or 0)
        net_total = gross_total - discount + tax
        if net_total < 0:
            print("❌ Total cannot be negative.")
            return False

        # Commit stock changes
        for product, qty, unit_price, subtotal in sold_items:
            new_qty = product.quantity - qty
            new_rev = product.revenue + subtotal
            self.cursor.execute(
                "UPDATE products SET quantity=?, revenue=? WHERE id=?",
                (new_qty, new_rev, product.id)
            )

        # Create receipt text and save file
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        receipt_file = os.path.join(RECEIPT_DIR, f"receipt_{timestamp_str}.txt")
        with open(receipt_file, "w", encoding="utf-8") as f:
            f.write("====== RECEIPT ======\n")
            f.write(f"Time: {datetime.now()}\n\n")
            total_calc = 0.0
            for product, qty, unit_price, subtotal in sold_items:
                f.write(f"{product.name} x{qty} @ ${unit_price:.2f} = ${subtotal:.2f}\n")
                total_calc += subtotal
            f.write(f"\nDiscount: -${discount:.2f}\n")
            f.write(f"Tax: +${tax:.2f}\n")
            total_calc = total_calc - discount + tax
            f.write(f"TOTAL: ${total_calc:.2f}\n")
            f.write(f"Payment Method: {payment_method}\n")
            f.write("====================\n")
        print(f"🧾 Sale recorded, receipt saved → {receipt_file}")

        # Log each sale in the database
        timestamp_db = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for product, qty, unit_price, subtotal in sold_items:
            self.cursor.execute("""
                INSERT INTO sales (product_id, quantity, unit_price, subtotal, discount, tax, total_price,
                                   payment_method, customer_id, receipt_path, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.id, qty, unit_price, subtotal, discount, tax, net_total,
                payment_method, customer_id, receipt_file, timestamp_db
            ))

        self.conn.commit()
        return True


