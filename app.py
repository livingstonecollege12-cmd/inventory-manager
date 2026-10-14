import os, sqlite3
from contextlib import closing
from flask import Flask, request, redirect, url_for, render_template_string, flash
app=Flask(__name__); app.secret_key=os.getenv('FLASK_SECRET_KEY','dev-only-change-this'); DB=os.getenv('DATABASE_PATH','inventory.db')
PAGE="""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Inventory Manager</title><style>body{font-family:system-ui;background:#f4f6fb;color:#182033;margin:0;padding:24px}main{max-width:1000px;margin:auto}h1{margin-bottom:4px}.muted{color:#64708a}form.add{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:8px;margin:20px 0}input,button{padding:11px;border:1px solid #ccd3e0;border-radius:8px;font:inherit}button{background:#182033;color:white;cursor:pointer}table{width:100%;border-collapse:collapse;background:white}th,td{text-align:left;padding:12px;border-bottom:1px solid #e8ebf2}.danger{background:#a32929}@media(max-width:650px){form.add{grid-template-columns:1fr}body{padding:12px}}</style></head><body><main><h1>Inventory Manager</h1><p class='muted'>Track products and stock for a small business.</p>{% with messages=get_flashed_messages() %}{% if messages %}<p>{{ messages[0] }}</p>{% endif %}{% endwith %}<form class='add' method='post' action='/products'><input name='name' placeholder='Product name' maxlength='100' required><input name='quantity' type='number' min='0' placeholder='Quantity' required><input name='price' type='number' min='0' step='0.01' placeholder='Unit price' required><button>Add product</button></form><table><thead><tr><th>Product</th><th>Quantity</th><th>Unit price</th><th>Stock value</th><th></th></tr></thead><tbody>{% for p in products %}<tr><td>{{ p.name }}</td><td>{{ p.quantity }}</td><td>{{ '%.2f'|format(p.price) }}</td><td>{{ '%.2f'|format(p.quantity*p.price) }}</td><td><form method='post' action='/products/{{ p.id }}/delete'><button class='danger'>Delete</button></form></td></tr>{% else %}<tr><td colspan='5'>No products yet. Add your first product.</td></tr>{% endfor %}</tbody></table><p><strong>Total stock value:</strong> {{ '%.2f'|format(total) }}</p></main></body></html>"""
def connect():
 con=sqlite3.connect(DB); con.row_factory=sqlite3.Row; return con
with closing(connect()) as con:
 con.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,quantity INTEGER NOT NULL CHECK(quantity>=0),price REAL NOT NULL CHECK(price>=0))'); con.commit()
@app.get('/')
def home():
 with closing(connect()) as con: products=con.execute('SELECT * FROM products ORDER BY name').fetchall()
 return render_template_string(PAGE,products=products,total=sum(p['quantity']*p['price'] for p in products))
@app.post('/products')
def add_product():
 name=request.form.get('name','').strip()
 try: quantity=int(request.form.get('quantity','')); price=float(request.form.get('price',''))
 except ValueError: flash('Quantity and price must be valid numbers.'); return redirect(url_for('home'))
 if not name or len(name)>100 or quantity<0 or price<0: flash('Enter a valid name and non-negative quantity and price.'); return redirect(url_for('home'))
 with closing(connect()) as con: con.execute('INSERT INTO products(name,quantity,price) VALUES (?,?,?)',(name,quantity,price)); con.commit()
 flash('Product added.'); return redirect(url_for('home'))
@app.post('/products/<int:product_id>/delete')
def delete_product(product_id):
 with closing(connect()) as con: con.execute('DELETE FROM products WHERE id=?',(product_id,)); con.commit()
 flash('Product deleted if it existed.'); return redirect(url_for('home'))
@app.get('/health')
def health(): return {'status':'ok'}
if __name__=='__main__': app.run(host='127.0.0.1',port=int(os.getenv('PORT','8000')),debug=False)
