from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pcwebsite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

active_users = {}

with app.app_context():
    db.create_all()

@app.route('/api/products', methods=['GET'])
def get_products():
    with open('static/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    return jsonify(products)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = request.cookies.get('token')
    if token and token in active_users:
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            token = str(uuid.uuid4())
            active_users[token] = username
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie('token', token)
            return resp
        else:
            return "Invalid username or password!", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        email = request.form['email']
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return "User or email already exists!", 400

        new_user = User(username=username, password=password, first_name=first_name,
                        last_name=last_name, birth_date=birth_date, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/main')
def main():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('main.html', username=username)

@app.route('/shoppingcart')
def shoppingcart():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('shoppingcart.html', username=username)

@app.route('/comparisons')
def comparisons():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('comparisons.html', username=username)

@app.route('/accessories')
def accessories():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('accessories.html', username=username)

@app.route('/mouses')
def mouses():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('mouses.html')
@app.route('/keyboards')
def keyboards():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('keyboards.html')
@app.route('/headphones')
def headphones():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('headphones.html')
@app.route('/microphones')
def microphones():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('microphones.html')
@app.route('/contacts')
def contacts():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))
    username = active_users[token]
    return render_template('contacts.html', username=username)
@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return redirect(url_for('index'))

    username = active_users[token]
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found!", 404
    return render_template('profile.html', user=user)
@app.route('/logout')
def logout():
    token = request.cookies.get('token')
    if token in active_users:
        del active_users[token]
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('token')
    return resp
@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def manage_cart():
    token = request.cookies.get('token')
    if not token or token not in active_users:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.filter_by(username=active_users[token]).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if request.method == 'GET':
        items = CartItem.query.filter_by(user_id=user.id).all()
        return jsonify([{'product_id': item.product_id, 'quantity': item.quantity} for item in items])
    elif request.method == 'POST':
        data = request.get_json()
        product_id = data.get('product_id')
        quantity_change = data.get('quantity_change', 1)
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity_change
            if cart_item.quantity > 10:
                cart_item.quantity = 10
            elif cart_item.quantity < 1:
                cart_item.quantity = 1
            else:
                db.session.add(cart_item)
        else:
            cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity_change)
            db.session.add(cart_item)
        db.session.commit()
        return jsonify({'success': True}), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        product_id = data.get('product_id')
        cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
        return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
