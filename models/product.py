class Product:
    def __init__(self, id, name, price, quantity, category, low_stock_threshold=5, revenue=0):
        self.id = id
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category
        self.low_stock_threshold = int(low_stock_threshold)
        self.revenue = float(revenue)

    def __str__(self):
        warning = "⚠️ Low stock!" if self.quantity <= self.low_stock_threshold else ""
        return f"{self.name} - ${self.price:.2f} x {self.quantity} [{self.category}] {warning}"



