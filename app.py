import csv
from io import StringIO
from flask import Response
from flask import Flask, render_template, redirect, request, flash, url_for
from config import Config
from models import db, User, Product, Inventory, Transaction
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ---------------- DATABASE INIT ---------------- #
with app.app_context():
    db.create_all()

# ---------------- LOGIN MANAGER ---------------- #
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------------- ROLE DECORATOR ---------------- #
def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.role not in roles:
                return "Access Denied"
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

# ---------------- LOGIN ---------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"].lower()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password) and user.role.lower() == role:
            login_user(user)
            return redirect("/dashboard")
        flash("Invalid credentials or role mismatch")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# ---------------- DASHBOARD ---------------- #
@app.route("/dashboard")
@login_required
def dashboard():
    products = Product.query.all()
    low_stock = []
    for p in products:
        inv = Inventory.query.filter_by(product_id=p.id).first()
        if inv and inv.quantity < p.min_stock:
            low_stock.append(p.name)
    return render_template("dashboard.html", low_stock=low_stock)

# ---------------- STOCK VIEW (ALL LOGGED USERS) ---------------- #
@app.route("/stock")
@login_required
def stock_view():
    products = Product.query.all()
    stock_data = []

    for p in products:
        inv = Inventory.query.filter_by(product_id=p.id).first()
        qty = inv.quantity if inv else 0
        status = "LOW" if qty < p.min_stock else "OK"

        stock_data.append({
            "name": p.name,
            "category": p.category,
            "quantity": qty,
            "min_stock": p.min_stock,
            "status": status
        })

    return render_template("stock.html", stock_data=stock_data)

# ---------------- EXPORT STOCK CSV ---------------- #
@app.route("/export_stock_csv")
@login_required
def export_stock_csv():
    products = Product.query.all()

    output = StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow(["Product", "Category", "Quantity", "Min Stock", "Status"])

    for p in products:
        inv = Inventory.query.filter_by(product_id=p.id).first()
        qty = inv.quantity if inv else 0
        status = "LOW" if qty < p.min_stock else "OK"

        writer.writerow([p.name, p.category, qty, p.min_stock, status])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=stock_report.csv"}
    )

# ---------------- PRODUCT LIST + CREATE ---------------- #
@app.route("/products", methods=["GET", "POST"])
@login_required
@role_required("admin")
def products():
    if request.method == "POST":
        new_product = Product(
            name=request.form["name"],
            category=request.form["category"],
            min_stock=int(request.form["min_stock"])
        )
        db.session.add(new_product)
        db.session.commit()
        db.session.add(Inventory(product_id=new_product.id, quantity=0))
        db.session.commit()
        flash("Product added successfully")

    return render_template("products.html", products=Product.query.all())

# ---------------- EDIT PRODUCT ---------------- #
@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.category = request.form["category"]
        product.min_stock = int(request.form["min_stock"])
        db.session.commit()
        flash("Product updated successfully")
        return redirect(url_for("products"))

    return render_template("edit_product.html", product=product)

# ---------------- DELETE PRODUCT ---------------- #
@app.route("/delete_product/<int:id>")
@login_required
@role_required("admin")
def delete_product(id):
    product = Product.query.get_or_404(id)

    Inventory.query.filter_by(product_id=id).delete()
    Transaction.query.filter_by(product_id=id).delete()
    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully")
    return redirect(url_for("products"))

# ---------------- INVENTORY ---------------- #
@app.route("/inventory", methods=["GET", "POST"])
@login_required
@role_required("manager", "staff")
def inventory():
    products = Product.query.all()
    if request.method == "POST":
        pid = int(request.form["product_id"])
        qty = int(request.form["quantity"])
        action = request.form["action"]

        inv = Inventory.query.filter_by(product_id=pid).first()
        if action == "OUT" and inv.quantity < qty:
            flash("Not enough stock!")
        else:
            inv.quantity += qty if action == "IN" else -qty
            db.session.add(Transaction(product_id=pid, change=qty, type=action, user=current_user.username))
            db.session.commit()

    return render_template("inventory.html", products=products)

# ---------------- TRANSACTIONS ---------------- #
@app.route("/transactions")
@login_required
@role_required("admin", "manager")
def transactions():
    tx = Transaction.query.order_by(Transaction.time.desc()).all()
    return render_template("transactions.html", tx=tx)

# ---------------- ANALYTICS DASHBOARD ---------------- #
@app.route("/analytics")
@login_required
@role_required("admin", "manager")
def analytics():
    products = Product.query.all()
    transactions = Transaction.query.all()

    # Stock per product
    product_names = []
    stock_levels = []

    for p in products:
        inv = Inventory.query.filter_by(product_id=p.id).first()
        qty = inv.quantity if inv else 0
        product_names.append(p.name)
        stock_levels.append(qty)

    # IN vs OUT counts
    in_count = sum(1 for t in transactions if t.type == "IN")
    out_count = sum(1 for t in transactions if t.type == "OUT")

    return render_template(
        "analytics.html",
        product_names=product_names,
        stock_levels=stock_levels,
        in_count=in_count,
        out_count=out_count
    )


if __name__ == "__main__":
    app.run(debug=True)
