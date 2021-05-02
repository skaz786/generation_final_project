import os
import psycopg2

dbname = os.environ["dbname"]
user = os.environ["user"]
password = os.environ["pass"]
host = os.environ["host"]
port = os.environ["port"]
    
def open_connection():
    conn = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
        )
    return conn

def create_products_table_in_cafe_db():
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = """CREATE TABLE IF NOT EXISTS products (
                            product_id INT IDENTITY PRIMARY KEY NOT NULL,
                            product_name VARCHAR(100) NOT NULL,
                            product_price DECIMAL(6,2) NOT NULL
                            )"""
            cursor.execute(postgresql)
            connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to create the products table: " + str(e))

def create_cafe_locations_table_in_cafe_db():
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = """CREATE TABLE IF NOT EXISTS cafe_locations (
                            location_id INT IDENTITY PRIMARY KEY NOT NULL,
                            location VARCHAR(100) NOT NULL
                            )"""
            cursor.execute(postgresql)
            connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to create the cafe_locations table: " + str(e))

def create_orders_table_in_cafe_db():
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = """CREATE TABLE IF NOT EXISTS orders (
                            order_id INT IDENTITY PRIMARY KEY NOT NULL,
                            date_time TIMESTAMP NOT NULL,
                            location_id INT NOT NULL,
                            order_price DECIMAL(6,2) NOT NULL,
                            CONSTRAINT fk_location_id FOREIGN KEY(location_id) REFERENCES cafe_locations(location_id)
                            )"""
            cursor.execute(postgresql)
            connection.commit()
        connection.close()
    except Exception as e:
      print("An error occurred when attempting to create the orders table: " + str(e))

def create_products_in_orders_table_in_cafe_db():
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = """CREATE TABLE IF NOT EXISTS products_in_orders (
                            order_id INT NOT NULL,
                            product_id INT NOT NULL,
                            CONSTRAINT fk_order_id FOREIGN KEY(order_id) REFERENCES orders(order_id),
                            CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES products(product_id)
                            )"""
            cursor.execute(postgresql)
            connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to create the products_in_orders table: " + str(e))
       
def fetch_location_data():
    temp_dict = {}
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = "SELECT * from cafe_locations"
            cursor.execute(postgresql)
            rows = cursor.fetchall()
            for row in rows:
                temp_dict[str(row[1])] = int(row[0])
            cursor.close()
    except Exception as e:
        print("An error occurred when attempting to fetch data from the cafe_locations table: " + str(e))

    return temp_dict

def fetch_product_data():
    temp_dict = {}
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = "SELECT * from products"
            cursor.execute(postgresql)
            rows = cursor.fetchall()
            for row in rows:
               temp_dict[str(row[1])] = int(row[0])
            cursor.close()
    except Exception as e:
        print("An error occurred when attempting to fetch data from the products table: " + str(e))

    return temp_dict

def load_into_cafe_locations_table(data_list):
    unique_location_list = list(set((order_dict['location']) for order_dict in data_list))
    sql_location_dict = fetch_location_data()
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            for location in unique_location_list:
                if location not in sql_location_dict:
                    cursor.execute("INSERT INTO cafe_locations (location) SELECT '{}' WHERE NOT EXISTS (SELECT location_id FROM cafe_locations WHERE location = '{}')".format(location, location))
                    connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to load data into the cafe_locations table: " + str(e))

def load_into_products_table(data_list):
    unique_product_list = sorted(list(set((order_dict['product'], order_dict['product_price']) for order_dict in data_list)))
    sql_product_dict = fetch_product_data()
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            for product in unique_product_list:
                if product[0] not in sql_product_dict:
                    cursor.execute("INSERT INTO products (product_name, product_price) SELECT '{}', '{}' WHERE NOT EXISTS (SELECT product_id FROM products WHERE product_name = '{}')".format(product[0], product[1], product[0]))
                    connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to load data into the products table: " + str(e))

def load_into_orders_table_and_update_local_ids(data_list):
    current_table = "orders"
    sql_location_dict = fetch_location_data()
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            for dictionary in data_list:
                rows_before = fetch_table_size(current_table)
                
                postgresql_1 = "INSERT INTO orders (date_time, location_id, order_price) SELECT '{}', '{}', '{}' WHERE NOT EXISTS (SELECT order_id FROM orders WHERE date_time = '{}' AND location_id = '{}' AND order_price = '{}')".format(dictionary['date_time'], sql_location_dict[dictionary['location']], dictionary['total'], dictionary['date_time'], sql_location_dict[dictionary['location']], dictionary['total'])
                cursor.execute(postgresql_1)
                connection.commit()
                
                rows_after = fetch_table_size(current_table)
                
                if rows_before != rows_after:                       
                    postgresql_2 = "SELECT order_id from orders WHERE order_id = (SELECT max(order_id) FROM orders)"
                    cursor.execute(postgresql_2)
                    row = cursor.fetchone()
                    dictionary['id'] = row[0]
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to load data into the orders table: " + str(e))

def load_into_products_in_orders_table(data_list):
    sql_product_dict = fetch_product_data()
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            for dictionary in data_list:
                postgresql = "INSERT INTO products_in_orders (order_id, product_id) SELECT '{}', '{}' WHERE NOT EXISTS (SELECT order_id FROM products_in_orders WHERE order_id = '{}' AND product_id = '{}')".format(dictionary['id'], sql_product_dict[dictionary['product']], dictionary['id'], sql_product_dict[dictionary['product']])
                cursor.execute(postgresql)
                connection.commit()
        connection.close()
    except Exception as e:
        print("An error occurred when attempting to load data into the products_in_orders table: " + str(e))

def fetch_table_size(table_name):    
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            postgresql = "SELECT COUNT(*) FROM {}".format(table_name)
            cursor.execute(postgresql)
            table_size = cursor.fetchone()
            cursor.close()
    except Exception as e:
        print("An error occurred when attempting to fetch size data from the {} table: ".format(table_name) + str(e))
    
    return table_size