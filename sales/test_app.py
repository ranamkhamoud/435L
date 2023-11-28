import os
import pytest
import requests_mock
from app import app, db, Sales

# URL to Inventory API
inventory_service_url = os.environ.get('INVENTORY_SERVICE_URL') or 'http://localhost:5002'  # URL to Inventory API
  # URL to Customer API
customer_service_url = os.environ.get('CUSTOMER_SERVICE_URL') or 'http://localhost:5001'  # URL to Customer API

# Set up the Flask test client
@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    # Configure the app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Create a test client using the Flask application
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
        yield testing_client  # This is where the testing happens
        with flask_app.app_context():
            db.drop_all()

# Mock external requests
@pytest.fixture
def mock_external_requests():
    with requests_mock.Mocker() as m:
        yield m

# Test the home endpoint
def test_home_endpoint(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Sales Service API!" in response.data

# Test display goods
def test_display_goods(test_client, mock_external_requests):
    mock_external_requests.get('http://localhost:5002/inventory/goods', json={"goods": []})
    response = test_client.get('/display')
    assert response.status_code == 200
    assert b"Goods" in response.data

# Test sale transaction
def test_sale_transaction(test_client, mock_external_requests):
    # Mock the inventory service response
    mock_external_requests.get('http://localhost:5002/inventory/goods/good_name', json={"price": 100}, status_code=200)
    # Mock the customer service responses
    mock_external_requests.get('http://localhost:5001/balance/customer_user', json={"balance": 200}, status_code=200)
    mock_external_requests.post('http://localhost:5001/deduct_wallet/customer_user', json={}, status_code=200)

    # Test successful transaction
    response = test_client.post('/sale', json={"name": "good_name", "customer_user": "customer_user"})
    assert response.status_code == 200
    assert b"Sale successful" in response.data

    # Verify database entry
    with app.app_context():
        sale = Sales.query.filter_by(username="customer_user").first()
        assert sale is not None
        assert sale.name == "good_name"

# Test sales history
def test_sales_history(test_client):
    response = test_client.get('/sales-history/customer_user')
    assert response.status_code == 200
    # Add more assertions based on your expected output

