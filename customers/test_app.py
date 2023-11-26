import pytest
from app import app, db, Customer  

@pytest.fixture(scope='module')
def test_client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up the test client
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client  # This is where the testing happens

        db.session.remove()
        db.drop_all()
@pytest.fixture(scope='module')
def new_customer():
    customer = Customer(username='testuser', full_name='Test User', password_hash='hashedpassword', age=30, address='123 Test St', gender='Male', marital_status='Single', wallet=100.0)
    return customer

# Model Tests
def test_new_customer(new_customer):
    assert new_customer.username == 'testuser'
    assert new_customer.full_name == 'Test User'
    assert new_customer.age == 30
    assert new_customer.address == '123 Test St'
    assert new_customer.gender == 'Male'
    assert new_customer.marital_status == 'Single'
    assert new_customer.wallet == 100.0

# Endpoint Tests
def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Customer Service API!" in response.data

def test_register_customer(test_client):
    # Success case
    data = {'username': 'newuser', 'full_name': 'New User', 'password': 'newpassword', 'age': 25, 'address': '456 New St', 'gender': 'Female', 'marital_status': 'Single'}
    response = test_client.post('/register', json=data)
    assert response.status_code == 201
    assert b'Customer registered successfully' in response.data

    # Error case: Missing fields
    data = {'username': 'incompleteuser'}
    response = test_client.post('/register', json=data)
    assert response.status_code == 400

def test_update_customer(test_client, new_customer):
    # Setup - Create a customer to update
    db.session.add(new_customer)
    db.session.commit()

    # Success case
    update_data = {'full_name': 'Updated Name'}
    response = test_client.put(f'/update/{new_customer.username}', json=update_data)
    assert response.status_code == 200
    assert b'Customer updated successfully' in response.data

    # Error case: Customer not found
    response = test_client.put('/update/nonexistinguser', json=update_data)
    assert response.status_code == 404

def test_get_customers(test_client, new_customer):
    # Setup for success case
    db.session.add(new_customer)
    db.session.commit()

    # Success case: Retrieve customers
    response = test_client.get('/customers')
    assert response.status_code == 200
    customers_data = response.get_json()
    assert isinstance(customers_data, list)
    assert len(customers_data) == 1
    assert customers_data[0]['username'] == new_customer.username

    # Cleanup after success case
    db.session.delete(new_customer)
    db.session.commit()

    # Error case: No customers found
    response = test_client.get('/customers')
    assert response.status_code == 404
    error_message = response.get_json()
    assert error_message['error'] == 'No customers found'


def test_get_customer(test_client, new_customer):
    # Setup - Create a customer
    db.session.add(new_customer)
    db.session.commit()

    # Success case
    response = test_client.get(f'/customer/{new_customer.username}')
    assert response.status_code == 200
    customer_data = response.get_json()
    assert customer_data['username'] == new_customer.username

    # Error case: Customer not found
    response = test_client.get('/customer/nonexistinguser')
    assert response.status_code == 404

def test_charge_wallet(test_client, new_customer):
    # Setup - Create a customer
    db.session.add(new_customer)
    db.session.commit()

    # Success case
    charge_data = {'amount': 50}
    response = test_client.post(f'/charge_wallet/{new_customer.username}', json=charge_data)
    assert response.status_code == 200
    assert b'added to wallet' in response.data

    # Error case: Customer not found
    response = test_client.post('/charge_wallet/nonexistinguser', json=charge_data)
    assert response.status_code == 404

def test_deduct_wallet(test_client, new_customer):
    # Setup - Create a customer
    db.session.add(new_customer)
    db.session.commit()

    # Success case
    deduct_data = {'amount': 30}
    response = test_client.post(f'/deduct_wallet/{new_customer.username}', json=deduct_data)
    assert response.status_code == 200
    assert b'deducted from wallet' in response.data

    # Error case: Insufficient funds
    insufficient_data = {'amount': 1000}
    response = test_client.post(f'/deduct_wallet/{new_customer.username}', json=insufficient_data)
    assert response.status_code == 400
def test_delete_customer(test_client, new_customer):
    # Setup - Create a customer to delete
    db.session.add(new_customer)
    db.session.commit()

    # Success case
    response = test_client.delete(f'/delete/{new_customer.username}')
    assert response.status_code == 200
    assert b'Customer deleted successfully' in response.data

    # Error case: Customer not found
    response = test_client.delete('/delete/nonexistinguser')
    assert response.status_code == 404