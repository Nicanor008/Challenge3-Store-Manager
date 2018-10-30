from app.models.db import init_db
from app.models.products import product_list

class salesData():
    def __init__(self):
        self.db = init_db()                             
        self.curr = self.db.cursor()
    
    def post_sale(salesid, product_category, product_name, product_quantity, price):
        # check if product exists
        product = [product for product in product_list if product_name != product["product_name"]]
        if not product:
            response = {"message":"product does not exist"}
        else:
            self.curr.execute("INSERT INTO products(productid, product_category, product_name, product_quantity,price) VALUES(%s, %s,  %s,  %s,  %s)", (productid, product_category, product_name, product_quantity, price,))
            response = self.db.commit()
            response = {'message':'product added successfully'}
        return response