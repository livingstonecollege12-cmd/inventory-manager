# Inventory Manager
Mobile-friendly Flask + SQLite app for adding and deleting products and calculating total stock value.

Run:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```
Visit `http://127.0.0.1:8000`.

Before public deployment, set `FLASK_SECRET_KEY` to a strong secret, add login/authorization and CSRF protection, and add tests, edit/search functions, and a deployment guide. Do not store sensitive data in this starter app.
