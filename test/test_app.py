import sys
sys.path.append("..") # Goes back a level in the directory
import src.app as app
import src.transform as transform

def test_append_to_list():

    def mock_reader():
        return [[('date_time', '2021-02-23 17:58:17'), ('location', 'Isle of Wight'), ('customer_name', 'Ramon Salters'), ('products', 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75'), ('payment_method', 'CASH'), ('total', '6.85'), ('card_details', 'None')], [('date_time', '2021-02-23 17:59:04'), ('location', 'Isle of Wight'), ('customer_name', 'Stanley Cordano'), ('products', ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45'), ('payment_method', 'CASH'), ('total', '8.50'), ('card_details', 'None')]]
    def mock_cached_list():
        return []
    
    actual = app.append_to_list(mock_reader(), mock_cached_list())
    expected = [{'date_time': '2021-02-23 17:58:17', 'location': 'Isle of Wight', 'customer_name': 'Ramon Salters', 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'payment_method': 'CASH', 'total': '6.85', 'card_details': 'None'}, {'date_time': '2021-02-23 17:59:04', 'location': 'Isle of Wight', 'customer_name': 'Stanley Cordano', 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'payment_method': 'CASH', 'total': '8.50', 'card_details': 'None'}]

    assert actual == expected

def test_remove_names():
    def mock_data():
        return {'date_time': '2021-02-23 17:58:17', 'location': 'Isle of Wight', 'customer_name': 'Ramon Salters', 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'payment_method': 'CASH', 'total': '6.85', 'card_details': 'None'}, {'date_time': '2021-02-23 17:59:04', 'location': 'Isle of Wight', 'customer_name': 'Stanley Cordano', 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'payment_method': 'CASH', 'total': '8.50', 'card_details': 'None'}

    mock_transform = transform.Transform(mock_data())
    
    mock_transform.remove_names()
    
    actual = mock_transform.data
    expected = {'date_time': '2021-02-23 17:58:17', 'location': 'Isle of Wight', 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'payment_method': 'CASH', 'total': '6.85', 'card_details': 'None'}, {'date_time': '2021-02-23 17:59:04', 'location': 'Isle of Wight', 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'payment_method': 'CASH', 'total': '8.50', 'card_details': 'None'}
    
    assert actual == expected

def test_remove_payment_details():
    def mock_data():
        return {'date_time': '2021-02-23 17:58:17', 'location': 'Isle of Wight', 'customer_name': 'Ramon Salters', 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'payment_method': 'CASH', 'total': '6.85', 'card_details': 'None'}, {'date_time': '2021-02-23 17:59:04', 'location': 'Isle of Wight', 'customer_name': 'Stanley Cordano', 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'payment_method': 'CASH', 'total': '8.50', 'card_details': 'None'}

    mock_transform = transform.Transform(mock_data())
    
    mock_transform.remove_payment_details()
    
    actual = mock_transform.data
    expected = {'date_time': '2021-02-23 17:58:17', 'location': 'Isle of Wight', 'customer_name': 'Ramon Salters', 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'total': '6.85'}, {'date_time': '2021-02-23 17:59:04', 'location': 'Isle of Wight', 'customer_name': 'Stanley Cordano', 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'total': '8.50'}
    
    assert actual == expected

def test_split_product():
    def mock_data():
        return [{'id':0, 'products': 'Regular Chai latte - 2.30, Large Chai latte - 2.60, Regular Flavoured hot chocolate - Caramel - 2.60, Large Speciality Tea - Camomile - 1.60, Large Cortado - 2.35, Regular Speciality Tea - English breakfast - 1.30'}]
    
    mock_transform = transform.Transform(mock_data())
    
    mock_transform.split_products()
    
    actual = mock_transform.data
    expected = [{'id': 0, 'products':'Regular Chai latte - 2.30'},
                {'id': 0, 'products':'Large Chai latte - 2.60'},
                {'id': 0, 'products':'Regular Flavoured hot chocolate - Caramel - 2.60'},
                {'id': 0, 'products':'Large Speciality Tea - Camomile - 1.60'},
                {'id': 0, 'products':'Large Cortado - 2.35'},
                {'id': 0, 'products':'Regular Speciality Tea - English breakfast - 1.30'}
                ]
    
    assert actual == expected

def test_split_product_price():
    def mock_data():
        return [{'id': 0, 'products':'Regular Chai latte - 2.30'}]
    
    mock_transform = transform.Transform(mock_data())
    
    mock_transform.split_product_price()
    
    actual = mock_transform.data
    expected = [{'id': 0, 'product':'Chai Latte Regular', 'product_price':'2.30'}]
    
    assert actual == expected
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
# Retired test relating to old csv format
def test_split_products():
    def mock_data():
        return [{'id': 0, 'products': 'Regular,Americano,1.95,,Flat white,2.15,,Flavoured iced latte - Caramel,2.75', 'total': '6.85'}, {'id': 1, 'products': ',Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45', 'total': '8.50'}]

    mock_transform = transform.Transform(mock_data())
    
    mock_transform.split_products()
    
    actual = mock_transform.data
    expected = [{'id': 0, 'products': 'Regular,Americano,1.95', 'total': '6.85'},
                {'id': 0, 'products': ',Flat white,2.15', 'total': '6.85'},
                {'id': 0, 'products': ',Flavoured iced latte - Caramel,2.75', 'total': '6.85'},
                {'id': 1, 'products': ',Frappes - Coffee,2.75', 'total': '8.50'},
                {'id': 1, 'products': ',Speciality Tea - Darjeeling,1.3', 'total': '8.50'},
                {'id': 1, 'products': ',Smoothies - Berry Beautiful,2.0', 'total': '8.50'},
                {'id': 1, 'products': 'Large,Latte,2.45', 'total': '8.50'}
                ]
    
    assert actual == expected

test_split_products()
'''