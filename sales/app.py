from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime #to save the history of purchases by a customer
import requests #for accessing other APIs

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#Goods Model

#define different classes for managing sales vs. managing goods
class Goods(db.Model):
    name = db.Column(db.String(200), unique = True, nullable = False)
    price = db.Column(db.Float, nullable=False)
    totalAmount = db.Column(db.Integer, nullable = False)

class Sales(db.Model):
    username = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    goodName = db.Column(db.String(200), nullable = False)
    time = db.Column(db.DateTime, default=datetime.utcnow) #takes current time

# Create declared tables
with app.app_context():
    db.create_all()


#to access customer api
customer_service_balance =   # Replace with the actual URL


#App Routes 

@app.route('/')
def home():
    return "Welcome to the Sales Service API!"


@app.route('/display', methods=['GET'])
def display_goods():
    goods = Goods.query.all();
        #loop over every item:
    goods_list = [{'name': good.name, 'price': good.price} for good in goods_list]
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
    
    if object and object.totalAmount > 0 : #good is available
        #check for money amount
        #need to access customer wallet
        return ##
    else:
        return ##

if __name__ == "__main__":
    app.run(debug=True)