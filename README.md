# Flask POS Inventory

A Flask-based Point of Sale and inventory app with role-based access, inventory management, sales processing, customer records, and reporting.

## Current UI Model (Final)

- Branding: `Flask POS`
- Consistent two-size typography:
  - normal text
  - button text
- Modal-first CRUD flow:
  - Inventory: `Add Product` modal + `Update Price` modal
  - Customers: `Add Customer` modal
  - Admin: `Add User` modal
- Sales flow:
  - quantity is entered in Sales
  - unit price is pulled from Inventory

## Features

- Authentication with roles: `Cashier`, `Manager`, `Admin`
- Inventory CRUD (add product, update product price)
- Sales checkout with discount/tax/payment/customer
- Receipt generation to `receipts/`
- Customer management
- Reports (daily sales, top selling, revenue summary)

## Project Structure

- `app.py` Flask routes and app bootstrap
- `models/` business/data access layer
- `templates/` Jinja UI templates
- `static/` CSS assets
- `tests/` smoke tests

Notes:
- `templates/add_product.html` and `templates/update_price.html` are kept as fallback route views.
- Main day-to-day UX is modal-based from primary pages.

## Local Setup

1. Create venv:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure env:
   - `cp .env.example .env`
   - set strong `SECRET_KEY`
4. Run:
   - `python app.py`
5. Open:
   - `http://127.0.0.1:5000`

## Default Admin (First Run)

- username: `admin`
- password: `admin123`

Change this for real usage.

## Test

- `pytest -q`
