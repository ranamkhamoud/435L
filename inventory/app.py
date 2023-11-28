from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration for Inventory Service
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inventory Model
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    stock_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<InventoryItem {self.name}>'

# Create the database tables
with app.app_context():
    db.create_all()

# API to add goods
@app.route('/inventory/add', methods=['POST'])
def add_goods():
    data = request.json
    # Validate input data
    if not all(key in data for key in ['name', 'category', 'price', 'stock_count']) or data['name'] == '':
        return jsonify({'error': 'Invalid input data'}), 400

    new_item = InventoryItem(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        description=data.get('description', ''),
        stock_count=data['stock_count']
    )

    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'}), 201

# API to update goods
@app.route('/inventory/update/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    item = db.session.get(InventoryItem, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data = request.json
    # Validate input data
    if 'stock_count' in data and data['stock_count'] < 0:
        return jsonify({'error': 'Invalid stock count'}), 400

    for key, value in data.items():
        setattr(item, key, value)

    db.session.commit()
    return jsonify({'message': 'Item updated successfully'}), 200

# API to deduce goods
@app.route('/inventory/deduce/<int:item_id>', methods=['POST'])
def deduce_goods(item_id):
    item = db.session.get(InventoryItem, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    amount = request.json.get('amount', 1)
    if amount <= 0 or item.stock_count < amount:
        return jsonify({'error': 'Invalid deduction amount'}), 400

    item.stock_count -= amount
    db.session.commit()
    return jsonify({'message': f'{amount} units deduced', 'new_stock_count': item.stock_count}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
