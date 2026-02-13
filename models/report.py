from datetime import datetime

class Report:
    def __init__(self, inventory):
        self.inventory = inventory
        self.cursor = inventory.cursor

    def daily_sales_data(self, date_str=None):
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT s.id, p.name, s.quantity, s.unit_price, s.subtotal, s.discount, s.tax, s.total_price, s.payment_method, s.timestamp
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.timestamp LIKE ?
            ORDER BY s.id
        """, (f"{date_str}%",))
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]  # return as list of dicts for template

    def top_selling_data(self, limit=5):
        self.cursor.execute("""
            SELECT p.name, SUM(s.quantity) as qty_sold, SUM(s.subtotal) as gross
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.name
            ORDER BY qty_sold DESC, gross DESC
            LIMIT ?
        """, (int(limit),))
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def revenue_summary_data(self, start_date, end_date):
        self.cursor.execute("""
            SELECT SUM(total_price) as total_rev, SUM(discount) as total_disc, SUM(tax) as total_tax
            FROM sales
            WHERE date(timestamp) BETWEEN date(?) AND date(?)
        """, (start_date, end_date))
        r = self.cursor.fetchone()
        return {
            "total_rev": float(r["total_rev"] or 0),
            "total_disc": float(r["total_disc"] or 0),
            "total_tax": float(r["total_tax"] or 0)
        }

