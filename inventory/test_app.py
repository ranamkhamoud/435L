import pytest
from app import app, db  
from app import InventoryItem  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
app.config['TESTING'] = True

@pytest.fixture
def client():
    # Setup the test client
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_goods(client):
    response = client.post('/inventory/add', json={
        'name': 'Laptop',
        'category': 'Electronics',
        'price': 1000.00,
        'description': 'High-end gaming laptop',
        'stock_count': 5
    })
    assert response.status_code == 201

def test_update_goods(client):
    with client.application.app_context():
        # Add a good first
        item = InventoryItem(name='Phone', category='Electronics', price=500, description='Smartphone', stock_count=10)
        db.session.add(item)
        db.session.commit()

        # Fetch the item again before updating
        item = db.session.get(InventoryItem, item.id)
        response = client.put(f'/inventory/update/{item.id}', json={'stock_count': 8})
        assert response.status_code == 200

def test_deduce_goods(client):
    with client.application.app_context():
        # Add a good first
        item = InventoryItem(name='Tablet', category='Electronics', price=300, description='Mini tablet', stock_count=10)
        db.session.add(item)
        db.session.commit()

        # Fetch the item again before deducing
        item = db.session.get(InventoryItem, item.id)
        response = client.post(f'/inventory/deduce/{item.id}', json={'amount': 2})
        assert response.status_code == 200
def test_add_goods_invalid_data(client):
    response = client.post('/inventory/add', json={
        'name': '',  # Invalid name
        'category': 'Electronics',
        'price': 1000.00,
        'description': 'High-end gaming laptop',
        'stock_count': 5
    })
    assert response.status_code == 400  # Assuming your API returns 400 for bad input

def test_update_nonexistent_goods(client):
    response = client.put('/inventory/update/999', json={'stock_count': 8})  # Non-existent item ID
    assert response.status_code == 404

def test_update_goods_invalid_data(client):
    with client.application.app_context():
        item = InventoryItem(name='Camera', category='Electronics', price=250, description='Digital camera', stock_count=5)
        db.session.add(item)
        db.session.commit()

        response = client.put(f'/inventory/update/{item.id}', json={'stock_count': -1})  # Invalid stock count
        assert response.status_code == 400

def test_deduce_goods_invalid_amount(client):
    with client.application.app_context():
        item = InventoryItem(name='Mouse', category='Electronics', price=25, description='Wireless mouse', stock_count=15)
        db.session.add(item)
        db.session.commit()

        response = client.post(f'/inventory/deduce/{item.id}', json={'amount': 20})  # More than available
        assert response.status_code == 400

def test_deduce_nonexistent_goods(client):
    response = client.post('/inventory/deduce/999', json={'amount': 1})  # Non-existent item ID
    assert response.status_code == 404

def test_inventory_item_representation(client):
    with client.application.app_context():
        item = InventoryItem(name='Headphones', category='Electronics', price=50, description='Noise-cancelling headphones', stock_count=10)
        db.session.add(item)
        db.session.commit()

        fetched_item = db.session.get(InventoryItem, item.id)
        assert str(fetched_item) == f'<InventoryItem {item.name}>'