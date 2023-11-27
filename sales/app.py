from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime #to save the history of purchases by a customer

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

#App Routes 

@app.route('/')
def home():
    return "Welcome to the Sales Service API!"

#note: create app routes for displaying goods, getting the details for each good, and when a sale happens 
    #needs to include if-statement
    #include error statements