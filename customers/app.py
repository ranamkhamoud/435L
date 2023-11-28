from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

# Database Configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Customer Model
class Customer(db.Model):
    username = db.Column(db.String(80), primary_key=True, unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    wallet = db.Column(db.Float, default=0.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<Customer {self.username}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return "Welcome to the Customer Service API!"

@app.route('/register', methods=['POST'])
def register_customer():
    data = request.json
    required_fields = ['username', 'full_name', 'password', 'age', 'address', 'gender', 'marital_status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        age = int(data['age'])
        if age < 0:
            return jsonify({'error': 'Age cannot be negative'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid age'}), 400

    try:
        new_customer = Customer(
            username=data['username'],
            full_name=data['full_name'],
            age=age,
            address=data['address'],
            gender=data['gender'],
            marital_status=data['marital_status']
        )
        new_customer.set_password(data['password'])
        db.session.add(new_customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Rollback to save the session state
        return jsonify({'error': 'Username already exists'}), 409

    return jsonify({'message': 'Customer registered successfully'}), 201

@app.route('/delete/<username>', methods=['DELETE'])
def delete_customer(username):
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

@app.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.json
    if 'age' in data:
        try:
            age = int(data['age'])
            if age < 0:
                raise ValueError
            customer.age = age
        except ValueError:
            return jsonify({'error': 'Invalid age'}), 400

    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    if not customers:
        return jsonify({'error': 'No customers found'}), 404

    customer_list = [{'username': customer.username, 'full_name': customer.full_name, 'age': customer.age, 'address': customer.address, 'gender': customer.gender, 'marital_status': customer.marital_status, 'wallet': customer.wallet} for customer in customers]
    return jsonify(customer_list), 200

@app.route('/customer/<username>', methods=['GET'])
def get_customer(username):
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer_info = {'username': customer.username, 'full_name': customer.full_name, 'age': customer.age, 'address': customer.address, 'gender': customer.gender, 'marital_status': customer.marital_status, 'wallet': customer.wallet}
    return jsonify(customer_info), 200

@app.route('/charge_wallet/<username>', methods=['POST'])
def charge_wallet(username):
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    try:
        amount = float(request.json.get('amount', 0))
        if amount <= 0:
            raise ValueError
        customer.wallet += amount
        db.session.commit()
        return jsonify({'message': f'{amount} added to wallet', 'new_balance': customer.wallet}), 200
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

@app.route('/deduct_wallet/<username>', methods=['POST'])
def deduct_wallet(username):
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    try:
        amount = float(request.json.get('amount', 0))
        if amount <= 0 or customer.wallet < amount:
            raise ValueError
        customer.wallet -= amount
        db.session.commit()
        return jsonify({'message': f'{amount} deducted from wallet', 'new_balance': customer.wallet}), 200
    except ValueError:
        return jsonify({'error': 'Invalid amount or insufficient funds'}), 400

#additional route (to check the balance of the customer)
@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    try:
        customer = Customer.query.get(username)
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        balance_info = {
            'username': customer.username,
            'balance': customer.wallet,
        }

        return jsonify(balance_info), 200

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error fetching customer balance: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    app.run(debug=True)
