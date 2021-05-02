class Transform:
    
    def __init__(self, data):
        # self.raw_data = data
        self.data = data
        # self.split_data = []
        
    def remove_names(self):        
        for order_dict in self.data:
            del order_dict['customer_name']
            
    def remove_payment_details(self):
        for order_dict in self.data:
            del order_dict['payment_method']
            del order_dict['card_details']         
    
    def add_id(self):
        for index, order_dict in enumerate(self.data):
            order_dict['id'] = index
    
    def sort_by_id(self):
        sorted_list = sorted(self.data, key = lambda k: k['id'])
        self.data = sorted_list
                    
    def split_date_time(self):
        for order_dict in self.data:
            order_date_time = order_dict['date_time'].split(' ')
            del order_dict['date_time']
            order_dict['date'] = order_date_time[0]
            order_dict['time'] = order_date_time[1]
            
    def split_product_price(self):
        # Does it work? We don't know 
        for order_dict in self.data:
            product_string =  order_dict['products']
            product_details = product_string.rsplit('-', 1)            
            
            order_dict['product_price'] = product_details[-1].strip() #Adds the product price as a key value pair in original dictionary
            dirty_product = product_details[0]
            product_size = dirty_product.split(' ', 1)[0].title()
            product_name = dirty_product.split(' ', 1)[1].title().strip()
            clean_product = product_name + ' ' + product_size
            
            order_dict['product'] = clean_product
            del order_dict['products']
            
    def seperate_products_string(self, order_dict):
        products_to_split = order_dict['products']        
        list_products = products_to_split.split(',')        
        for product in list_products:
            temp_dict = order_dict.copy() # Makes a COPY of the original dictionary
            temp_dict['products'] = product.strip() # Overwrites value held at 'products' key into copy of order dictionary
            self.data.append(temp_dict) # Inserts into the same index of the original dictionary in the list   
                
    def split_products(self):
        data_copy = self.data.copy()
        self.data = []
        
        for index in range(len(data_copy)):                      
            product_list = data_copy[index]['products'].split(',')
            if len(product_list) > 1:                
                order_to_split = data_copy[index]
                self.seperate_products_string(order_to_split)
            else:
                self.data.append(data_copy[index])
                
    def reverse_date(self):
        for order_dict in self.data:
            old_date = order_dict['date']
            split_date = old_date.split('/')
            rev_date = split_date[::-1]
            new_date = '-'.join(rev_date)
            order_dict['date'] = new_date
            
    def rejoin_date_time(self):
        for order_dict in self.data:
            order_dict['date_time'] = ' '.join([order_dict['date'],order_dict['time']])
            del order_dict['date']
            del order_dict['time']