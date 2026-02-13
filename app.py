import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from models.user import User
from models.inventory import Inventory
from models.sale import Sale
from models.customer import Customer
from models.report import Report
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

# Initialize backend modules
users = User()
inventory = Inventory()
sales = Sale(inventory)
customers = Customer()
reports = Report(inventory)

# --- Create initial admin if not exists ---
if not users.authenticate("admin", "admin123"):
    users.add_user("admin", "admin123", "Admin")

# ------------------ Auth ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"].strip()
        pwd = request.form["password"].strip()
        user = users.authenticate(uname, pwd)
        if user:
            session["user"] = user
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.")
    return render_template("login.html", user=None)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ------------------ Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("base.html", user=session["user"])

# ------------------ Inventory ------------------
@app.route("/inventory")
def inventory_list():
    if "user" not in session:
        return redirect(url_for("login"))
    products = inventory.cursor.execute("SELECT * FROM products ORDER BY name").fetchall()
    return render_template("inventory.html", products=products, user=session["user"])

@app.route("/inventory/add", methods=["GET","POST"])
def inventory_add():
    if "user" not in session or session["user"]["role"] not in ("Manager","Admin"):
        flash("❌ Permission denied.")
        return redirect(url_for("inventory_list"))
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        qty = int(request.form["quantity"])
        category = request.form.get("category","General")
        inventory.add_product(name, price, qty, category)
        return redirect(url_for("inventory_list"))
    return render_template("add_product.html", user=session["user"])

@app.route("/inventory/update/<int:product_id>", methods=["GET","POST"])
def inventory_update_price(product_id):
    if "user" not in session or session["user"]["role"] not in ("Manager","Admin"):
        flash("❌ Permission denied.")
        return redirect(url_for("inventory_list"))
    product = inventory.cursor.execute("SELECT * FROM products WHERE id=?",(product_id,)).fetchone()
    if request.method == "POST":
        new_price = float(request.form["price"])
        inventory.update_price(product["name"], new_price)
        return redirect(url_for("inventory_list"))
    return render_template("update_price.html", product=product, user=session["user"])

# ------------------ Sales ------------------
@app.route("/sale", methods=["GET","POST"])
def new_sale():
    if "user" not in session:
        return redirect(url_for("login"))
    products = inventory.cursor.execute("SELECT * FROM products ORDER BY name").fetchall()
    if request.method == "POST":
        items = []
        for key in request.form:
            if key.startswith("qty_") and int(request.form[key]) > 0:
                pid = int(key.split("_")[1])
                pname = inventory.cursor.execute("SELECT name FROM products WHERE id=?",(pid,)).fetchone()["name"]
                items.append((pname, int(request.form[key])))
        discount = float(request.form.get("discount",0))
        tax = float(request.form.get("tax",0))
        payment_method = request.form.get("payment_method","Cash")
        cust_name = request.form.get("customer_name","").strip()
        customer_id = customers.find_customer_id(cust_name) if cust_name else None
        sales.sell_product(items, discount, tax, payment_method, customer_id)
        return redirect(url_for("new_sale"))
    return render_template("sale.html", products=products, user=session["user"])

# ------------------ Reports ------------------
@app.route("/reports")
def report_page():
    if "user" not in session or session["user"]["role"] not in ("Manager","Admin"):
        flash("❌ Permission denied.")
        return redirect(url_for("dashboard"))

    # Get data from Report class
    daily_sales = reports.daily_sales_data()
    top_selling = reports.top_selling_data()
    revenue_summary = reports.revenue_summary_data(
        start_date=datetime.now().strftime("%Y-%m-%d"),
        end_date=datetime.now().strftime("%Y-%m-%d")
    )

    return render_template(
        "reports.html",
        user=session["user"],
        daily_sales=daily_sales,
        top_selling=top_selling,
        revenue_summary=revenue_summary
    )

# ------------------ Customers ------------------
@app.route("/customers")
def customer_page():
    if "user" not in session:
        return redirect(url_for("login"))
    custs = customers.list_customers()  # use new method returning list
    return render_template("customers.html", customers=custs, user=session["user"])

@app.route("/customers/add", methods=["POST"])
def customer_add():
    if "user" not in session:
        return redirect(url_for("login"))
    name = request.form["name"].strip()
    phone = request.form.get("phone","").strip()
    email = request.form.get("email","").strip()
    if name:
        customers.add_customer(name, phone, email)
    return redirect(url_for("customer_page"))

# ------------------ Admin ------------------
@app.route("/admin", methods=["GET","POST"])
def admin_page():
    if "user" not in session or session["user"]["role"] != "Admin":
        flash("❌ Permission denied.")
        return redirect(url_for("dashboard"))
    users_list = users.cursor.execute("SELECT id, username, role FROM users ORDER BY role, username").fetchall()
    if request.method == "POST":
        uname = request.form["username"].strip()
        pwd = request.form["password"].strip()
        role = request.form.get("role","Cashier")
        users.add_user(uname, pwd, role)
        return redirect(url_for("admin_page"))
    return render_template("admin.html", users=users_list, user=session["user"])

if __name__ == "__main__":
    app.run(debug=True)


