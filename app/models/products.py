from app.models.db import init_db
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)

product_list = []

class productsData():
    def __init__(self):
        self.db = init_db()                             
        self.curr = self.db.cursor()
    
    def get_all_products(self):
        self.curr.execute("SELECT * FROM products")
        data = self.curr.fetchall()
        
        for i, items in enumerate(data):
            productid, product_category, product_name, product_quantity, price = items
            fetched_data = dict(
                productid = int(productid),
                product_category = product_category,
                product_name = product_name,
                product_quantity = product_quantity,
                price = price
            )
            product = [product for product in product_list if productid == product["productid"]]
            if product:
                response = product_list
            else:
                product_list.append(fetched_data)
        response = product_list
        return response

    def add_product(self, productid, product_category, product_name, product_quantity,price):
        # handle a product already exists
        product = [product for product in product_list if productid != product["productid"]]
        if not product:
            response = {"message":"product already exist"}
        else:
            self.curr.execute("INSERT INTO products(productid, product_category, product_name, product_quantity,price) VALUES(%s, %s,  %s,  %s,  %s)", (productid, product_category, product_name, product_quantity, price,))
            response = self.db.commit()
            response = {'message':'product added successfully'}
        return response
    
    # update a product
    def update_product(self, productid, product_category, product_name, product_quantity,price, prodid):
        
    #    product already exists


        # user must be an admin
        # claims = get_jwt_claims()
        # if claims['role'] != "admin":
        #     return {"message": "Sorry, you don't have administrator rights"}
        product = [product for product in product_list if productid == product["productid"]]
        if not product:
            return {"products does not exist"}
        else:
            res = self.curr.execute("UPDATE products SET productid=%s, product_category=%s, product_name=%s, product_quantity=%s, price=%s WHERE productid=%s", (productid, product_category, product_name, product_quantity, price, prodid))
            if res:
                self.db.commit()
                return 'success'
            else:
                return {'failed'}

    def delete_product(self, prodid):
        self.curr.execute("DELETE FROM products WHERE productid=%s", (prodid,))
        return self.db.commit()