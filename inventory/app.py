from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration for Inventory Service
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class InventoryItem(db.Model):
    """
    Represents an item in the inventory.

    Attributes:
        id (int): Unique identifier for the inventory item.
        name (str): Name of the inventory item.
        category (str): Category of the inventory item.
        price (float): Price of the inventory item.
        description (str): Description of the inventory item.
        stock_count (int): Quantity of the inventory item in stock.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    stock_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<InventoryItem {self.name}>'

    def to_dict(self):
        """
        Convert inventory item details into a dictionary.

        Returns:
            dict: Dictionary containing key details of the inventory item.
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
        }

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """
    Home endpoint returning a welcome message.

    Returns:
        str: Welcome message for the Inventory Service API.
    """
    return "Welcome to the Inventory Service API!"

@app.route('/inventory/goods', methods=['GET'])
def get_goods():
    """
    API endpoint to fetch all goods in the inventory.

    Returns:
        JSON: A list of goods from the inventory with their details.
    """
    goods = InventoryItem.query.all()
    return jsonify({'Inventory': [good.to_dict() for good in goods]}), 200

@app.route('/inventory/goods/<string:name>', methods=['GET'])
def get_good(name):
    """
    API endpoint to fetch a specific item by its name.

    Args:
        name (str): The name of the item to retrieve.

    Returns:
        JSON: Details of the requested item or an error message.
    """
    good = InventoryItem.query.filter_by(name=name).first()
    if not good:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(good.to_dict()), 200

@app.route('/inventory/add', methods=['POST'])
def add_goods():
    """
    API endpoint to add a new item to the inventory.

    Returns:
        JSON: A success message or an error message.
    """
    data = request.json
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

@app.route('/inventory/update/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    """
    API endpoint to update the details of an existing inventory item.

    Args:
        item_id (int): The unique identifier of the item to update.

    Returns:
        JSON: A success message or an error message.
    """
    item = db.session.get(InventoryItem, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data = request.json
    if 'stock_count' in data and data['stock_count'] < 0:
        return jsonify({'error': 'Invalid stock count'}), 400

    for key, value in data.items():
        setattr(item, key, value)

    db.session.commit()
    return jsonify({'message': 'Item updated successfully'}), 200

@app.route('/inventory/deduce/<int:item_id>', methods=['POST'])
def deduce_goods(item_id):
    """
    API endpoint to reduce the stock count of an inventory item.

    Args:
        item_id (int): The unique identifier of the item for which stock is to be reduced.

    Returns:
        JSON: A success message or an error message.
    """
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
    app.run(host='0.0.0.0', port=5000)
