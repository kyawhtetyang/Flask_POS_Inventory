# Flask POS Inventory

A Flask-based Point of Sale and inventory management app with:
- role-based login (`Cashier`, `Manager`, `Admin`)
- inventory and pricing management
- sales processing with receipt generation
- customer tracking
- sales/reporting views

## Project Structure

- `app.py` Flask app and routes
- `models/` business/data access layer
- `templates/` Jinja templates
- `static/` CSS and static assets
- `shop.db` local SQLite database (ignored)
- `receipts/` generated receipts (ignored)

## Local Setup

1. Create virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure environment:
   - `cp .env.example .env`
   - set a strong `SECRET_KEY`
4. Run app:
   - `python app.py`
5. Open:
   - `http://127.0.0.1:5000`

## Default Admin

On first run, app bootstraps default admin credentials:
- username: `admin`
- password: `admin123`

Change this immediately for real usage.

## Testing

Run:
- `pytest -q`
