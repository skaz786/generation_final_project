import csv
import os
import src.db as db
import src.transform as transform

def start_transformation(csv_data):

    cafe_data = transform.Transform(csv_data)
    # if __name__ == '__main__':
    
    db.create_products_table_in_cafe_db()
    print('Created products table')
    db.create_cafe_locations_table_in_cafe_db()
    print('Created cafe_locations table')
    db.create_orders_table_in_cafe_db()
    print('Created orders table')
    db.create_products_in_orders_table_in_cafe_db()
    print('Created products_in_orders table')

    cafe_data.remove_names()
    cafe_data.remove_payment_details()
    cafe_data.split_date_time()
    cafe_data.reverse_date()
    cafe_data.rejoin_date_time()
    cafe_data.add_id()
    print('Completed first set of transformation')
    
    db.load_into_cafe_locations_table(cafe_data.data)
    print('Loaded into cafe_locations table')
    db.load_into_orders_table_and_update_local_ids(cafe_data.data)
    print('Loaded into orders table')
    
    cafe_data.split_products()
    cafe_data.split_product_price()
    cafe_data.sort_by_id()
    print('Completed second set of transformation')
    
    db.load_into_products_table(cafe_data.data)
    print('Loaded into products table')
    db.load_into_products_in_orders_table(cafe_data.data)
    print('Loaded into products_in_orders table')
