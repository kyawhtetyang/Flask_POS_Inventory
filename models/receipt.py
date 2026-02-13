import os
from datetime import datetime

RECEIPT_DIR = "receipts"

class Receipt:
    invoice_counter = 1

    def __init__(self, items, payment_method, discount=0, tax=0):
        self.invoice_id = Receipt.invoice_counter
        Receipt.invoice_counter += 1
        self.items = items  # list of (name, qty, price)
        self.discount = float(discount or 0)
        self.tax = float(tax or 0)
        self.payment_method = payment_method
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_text(self):
        lines = []
        lines.append("\n====== RECEIPT ======")
        lines.append(f"Invoice: {self.invoice_id} | Time: {self.timestamp}")
        total = 0.0
        for name, qty, price in self.items:
            subtotal = float(qty) * float(price)
            total += subtotal
            lines.append(f"{name} x{qty} @ ${float(price):.2f} = ${subtotal:.2f}")
        if self.discount > 0:
            lines.append(f"Discount: -${self.discount:.2f}")
            total -= self.discount
        if self.tax > 0:
            lines.append(f"Tax: +${self.tax:.2f}")
            total += self.tax
        lines.append(f"Payment Method: {self.payment_method}")
        lines.append(f"TOTAL: ${total:.2f}")
        lines.append("====================\n")
        return "\n".join(lines)

    def save_receipt(self):
        os.makedirs(RECEIPT_DIR, exist_ok=True)
        text = self.generate_text()
        filename = f"receipt_{self.invoice_id}.txt"
        path = os.path.join(RECEIPT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"🧾 Saved receipt → {path}")
        return text, path

