import pytest
from app import app, db, Customer  
from datetime import datetime

@pytest.fixture(scope='module')
def test_sale():
    #configure app
    app.config['TESTING'] = True 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_DATABASE_URI'] = False

    #test
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client 

        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def new_good():
    good = Goods(name='test_name', price=100.0, totalAmount=10)
    return good

def new_sale():
    sale = Sales(username='test_user', name='test_good',price=50.0,time=datetime.utcnow())
    return sale

#testing 
def test_new_good(new_good):
    assert new_good.name == 'test_name'
    assert new_good.price == 100.0
    assert new_good.totalAmount == 10

def test_new_sale(new_sale):
    assert new_sale.username == 'test_user'
    assert new_sale.name == 'test_good'
    assert new_sale.price == 50.0

#endpoint
def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Sales Service API!" in response.data

def test_display_goods(test_client):
    #create goods to display
    db.session.add(new_good)
    db.session.commit()

    response = test_client.get('/display')
    assert response.status_code == 200
    goods_data = response.get_json()

    assert isinstance(goods_data, dict) #instance of goods list
    assert 'Goods' in goods_data
    assert len(goods_data['Goods']) == 1
    assert goods_data['Goods'][0]['name'] == new_good.name
    assert goods_data['Goods'][0]['price'] == new_good.price

def test_get_goods_info(test_client, new_good):
    #create new good to get info
    db.session.add(new_good)
    db.session.commit()

    response = test_client.get(f'/goods/{new_good.name}')
    assert response.status_code == 200
    goods_info = response.get_json()
    
    assert goods_info['name'] == new_good.name
    assert goods_info['price'] == new_good.price
    assert goods_info['count'] == new_good.totalAmount

    response = test_client.get('/goods/nonexistinggood')
    assert response.status_code == 404

def test_sale_transaction(test_client, new_good, new_sale):
    #create new good to sell
    db.session.add(new_good)
    db.session.commit()

    # best case
    data = {'name': 'Test Good', 'customer_user': 'testuser'}
    response = test_client.post('/sale', json=data)
    assert response.status_code == 200
    assert b'Sale successful' in response.data

    # error case:  not available
    new_good.totalAmount = 0
    db.session.commit()
    response = test_client.post('/sale', json=data)
    assert response.status_code == 404
    assert b'Item not available' in response.data

    # error case:  insufficient funds
    response = test_client.post('/sale', json={'name': 'Test Good', 'customer_user': 'insufficientuser'})
    assert response.status_code == 400
    assert b'Customer has insufficient funds' in response.data

def test_get_sales_history(test_client, new_sale):
    #create new sale to get history
    db.session.add(new_sale)
    db.session.commit()

    # best case
    response = test_client.get(f'/sales-history/{new_sale.username}') 
    assert response.status_code == 200
    sales_history = response.get_json()

    assert isinstance(sales_history, dict)  
    assert 'sales_history' in sales_history #available in history (sold?)
    assert len(sales_history['sales_history']) == 1
    assert sales_history['sales_history'][0]['good'] == new_sale.name
    assert sales_history['sales_history'][0]['price'] == new_sale.price
    assert 'timestamp' in sales_history['sales_history'][0]

    # error case: no sales history 
    response = test_client.get('/sales-history/nonexistinguser')
    assert response.status_code == 200
    assert 'No sales history found' in response.json['message']

