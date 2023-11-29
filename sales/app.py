"""
Sales Service API

This module is a Flask application for a Sales Service API. Consists of functions for managing goods, sales transactions, and sales history.

"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Database Configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Sales Model
class Sales(db.Model):
    """
    Represents a sales transaction in the database.

    Attributes:
        id (int): Unique identifier for the sales transaction.
        username (str): Username of the customer involved in the sale.
        price (float): Total price of the sale.
        name (str): Name of the item sold.
        time (datetime): Timestamp of when the sale occurred.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

# Create declared tables
with app.app_context():
    db.create_all()

# URL to Inventory API
inventory_service_url = os.environ.get('INVENTORY_SERVICE_URL') or 'http://localhost:5002'  # URL to Inventory API
# URL to Customer API
customer_service_url = os.environ.get('CUSTOMER_SERVICE_URL') or 'http://localhost:5001'  # URL to Customer API

# App Routes
@app.route('/')
def home():
    """Returns a welcome message."""
    return "Welcome to the Sales Service API!"

@app.route('/display', methods=['GET'])
def display_goods():
    """
    Fetches and displays goods from the Inventory Service.

    Returns:
        JSON: A list of goods along with their details fetched from the Inventory Service.
    """
    response = requests.get(f'{inventory_service_url}/inventory/goods')
    if response.status_code == 200:
        return jsonify({'Goods': response.json()})
    else:
        return jsonify({'error': 'Unable to fetch goods from Inventory Service'}), 500

@app.route('/sale', methods=['POST'])
def sale_transaction():
    """
    Handles the sales transaction.

    Processes the sale of an item by checking its availability, confirming the customer's balance, and updating the sales history.

    Returns:
        JSON: A success message if the sale is successful or an error message otherwise.
    """

    data = request.json
    good_name = data.get('name')
    customer_user = data.get('customer_user')

    # Check availability of the good in inventory
    inventory_api_url = f'{inventory_service_url}/inventory/goods/{good_name}'
    inventory_response = requests.get(inventory_api_url)

    if inventory_response.status_code != 200:
        # Log and return error if item is not found in inventory
        print(f"Failed to retrieve item from inventory. Status: {inventory_response.status_code}, Response: {inventory_response.text}")
        return jsonify({'error': 'Item not available in inventory'}), inventory_response.status_code

    good_data = inventory_response.json()
    if good_data.get('price', 0) <= 0:
        return jsonify({'error': 'Item not available'}), 404

    # Check customer's balance
    customer_balance_api_url = f'{customer_service_url}/balance/{customer_user}'
    try:
        customer_balance_response = requests.get(customer_balance_api_url)

        if customer_balance_response.status_code != 200:
            print(f"Failed to retrieve customer balance. Status: {customer_balance_response.status_code}, Response: {customer_balance_response.text}")
            return jsonify({'error': 'Failed to retrieve customer balance'}), customer_balance_response.status_code

        customer_balance_data = customer_balance_response.json()
        if customer_balance_data.get('balance', 0) < good_data['price']:
            return jsonify({'error': 'Insufficient funds'}), 400

        # Deduct amount from customer's wallet
        wallet_deduct_api_url = f'{customer_service_url}/deduct_wallet/{customer_user}'
        wallet_deduct_response = requests.post(wallet_deduct_api_url, json={'amount': good_data['price']})

        if wallet_deduct_response.status_code != 200:
            print(f"Failed to deduct amount from wallet. Status: {wallet_deduct_response.status_code}, Response: {wallet_deduct_response.text}")
            return jsonify({'error': 'Failed to deduct amount from wallet'}), wallet_deduct_response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Network error during customer balance check or wallet deduction: {e}")
        return jsonify({'error': f'Error during transaction: {str(e)}'}), 500

    # Register the sale
    sale = Sales(username=customer_user, name=good_name, price=good_data['price'], time=datetime.utcnow())
    db.session.add(sale)
    db.session.commit()

    return jsonify({'message': 'Sale successful'}), 200

# additional route in case of sales history 
@app.route('/sales-history/<username>', methods=['GET'])
def get_sales_history(username):

    """
    Retrieves the sales history of a specific customer.

    Args:
        username (str): Username of the customer.

    Returns:
        JSON: A list of all sales transactions associated with the given username.
    """
    history = Sales.query.filter_by(username=username).all()

    if history:
        formatted_sales_history = [
            {
                'good': sale.name,
                'price': sale.price,
                'time': sale.time.strftime('%Y-%m-%d %H:%M:%S')
            }
            for sale in history
        ]
        return jsonify({'sales_history': formatted_sales_history})
    else:
        return jsonify({'message': f'No sales history found for {username}'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
