from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

# Database Configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(base_dir, '..', 'db', 'database.db')
db_path = os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Customer Model
class Customer(db.Model):
    """
    Represents a customer in the database.

    Attributes:
        username (str): The username of the customer, serving as the primary key.
        full_name (str): The full name of the customer.
        password_hash (str): The hashed password of the customer.
        age (int): The age of the customer.
        address (str): The address of the customer.
        gender (str): The gender of the customer.
        marital_status (str): The marital status of the customer.
        wallet (float): The wallet balance of the customer.
    
    """
    username = db.Column(db.String(80), primary_key=True, unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    wallet = db.Column(db.Float, default=0.0)

    def set_password(self, password):
        """Sets the password of the customer."""
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        """Returns the string representation of the customer."""
        return f'<Customer {self.username}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    """Returns a welcome message."""
    return "Welcome to the Customer Service API!"

@app.route('/register', methods=['POST'])
def register_customer():
    """
    Registers a new customer.

    The customer details are obtained from the JSON request body.
    Validates the required fields and age before creating the customer.
    """
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
    """
    Deletes a customer.

    Args:
        username (str): The username of the customer to be deleted.
    """
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

@app.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    """
    Updates a customer's information.

    Args:
        username (str): The username of the customer to be updated.
    """
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
    """Returns a list of all customers."""
    customers = db.session.query(Customer).all()
    if not customers:
        return jsonify({'error': 'No customers found'}), 404

    customer_list = [{'username': customer.username, 'full_name': customer.full_name, 'age': customer.age, 'address': customer.address, 'gender': customer.gender, 'marital_status': customer.marital_status, 'wallet': customer.wallet} for customer in customers]
    return jsonify(customer_list), 200

@app.route('/customer/<username>', methods=['GET'])
def get_customer(username):
    """
    Retrieves a single customer.

    Args:
        username (str): The username of the customer to be retrieved.
    """
    customer = db.session.get(Customer, username)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer_info = {'username': customer.username, 'full_name': customer.full_name, 'age': customer.age, 'address': customer.address, 'gender': customer.gender, 'marital_status': customer.marital_status, 'wallet': customer.wallet}
    return jsonify(customer_info), 200

@app.route('/charge_wallet/<username>', methods=['POST'])
def charge_wallet(username):
    """
    Charges a customer's wallet.

    Args:
        username (str): The username of the customer whose wallet is to be charged.
    """
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
    """
        Deducts an amount from a customer's wallet.

    Args:
        username (str): The username of the customer whose wallet is to be deducted.
    """

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
@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    """
    Retrieves the balance of a customer's wallet.

    Args:
        username (str): The username of the customer whose balance is to be retrieved.
    """
    customer = db.session.query(Customer).filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    balance_info = {
        'username': customer.username,
        'balance': customer.wallet,
    }

    return jsonify(balance_info), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

