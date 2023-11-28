"""
Sales Service API

This module is a Flask application for a Sales Service API. Consists of functions for managing goods, sales transactions, and sales history.

"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime #to save the history of purchases by a customer
import requests #for accessing other APIs
import os
app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#Goods Model

#define different classes for managing sales vs. managing goods
class Goods(db.Model):
    """
    Goods Model 

    Represents a list of the available goods in database

    Attributes:
    - name (str): the name of the good documented
    - price (float): the price of the good
    - totalAmount (int): the amount of the good available
    """
    name = db.Column(db.String(200), unique = True, nullable = False)
    price = db.Column(db.Float, nullable=False)
    totalAmount = db.Column(db.Integer, nullable = False)

class Sales(db.Model):
    """
    Sales Model 

    Represents a sales transaction 

    Attributes:
    - username (str): the username of the customer that purchased the good
    - price (float): the price of the sold good
    - name (str): the name of the sold good
    - time (datetime): timestap of the time the good was sold
    """
    username = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    time = db.Column(db.DateTime, default=datetime.utcnow) #takes current time

# Create declared tables
with app.app_context():
    db.create_all()


#to access customer api
customer_service_balance = "http://localhost:5001/balance/<username>" # double check ports


#App Routes 

@app.route('/')
def home():
    return "Welcome to the Sales Service API!"


@app.route('/display', methods=['GET'])
def display_goods():
    goods = Goods.query.all();
        #loop over every item:
    goods_list = [{'name': good.name, 'price': good.price} for good in goods]
    return jsonify({'Goods' : goods_list})

#get method (retrieve data)
@app.route('/goods/<name>', methods=['GET'])
def get_goods_info(name):
    object = Goods.query.filter_by(name = object.name).first()

    if object: #good is available
        return jsonify({'name':object.name, 'price':object.price, 'count':object.totalAmount})
    else:
        return jsonify({'error': f'{name} not found in list of goods'}), 404

#post method (submit data to be processed)
@app.route('/sale', methods=['POST'])
def sale_transaction():
    data = request.json
    good_name = data.get('name')
    customer_user = data.get('customer_user')

    object = Goods.query.filter_by(name='good_name').first()
    
    if not object and object.totalAmount <= 0 : #good is not available
        return jsonify({'error': 'Item not available'}), 404
    
    try:
        customer_service_amount = {'customer_user': customer_user, 'required_amount': object.price}
        balance_output = requests.post(customer_service_balance, json=customer_service_amount)
        balance_data = balance_output.json()

        if balance_output.status_code == 200:
            object.totalAmount -= 1

            sale = Sales(username=customer_user, name=good_name, price=object.price, time=datetime.utcnow())
            db.session.add(sale)
            db.session.commit()

            return jsonify({'message': 'Sale successful', 'new_balance': balance_data.get('new_balance')}), 200
        else:
            requests.post(f"{customer_service_balance}/charge_wallet/{customer_user}", json={'amount': object.price})
            return jsonify({'error': 'Customer has insufficient funds'}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error connecting to customer service: {e}'}), 500

# additional route in case of sales history 
@app.route('/sales-history/<username>', methods=['GET'])
def get_sales_history(username):
    history = Sales.query.filter_by(username=username).all()

    if history:
        formatted_sales_history = [
            {
                'good': sale.name,
                'price': sale.price,
                'timestamp': sale.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for sale in history
        ]
        return jsonify({'sales_history': formatted_sales_history})
    else:
        return jsonify({'message': f'No sales history found for {username}'})


if __name__ == "__main__":
    app.run(debug=True)