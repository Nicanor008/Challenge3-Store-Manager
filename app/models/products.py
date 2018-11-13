from app.models.db import init_db
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from instance.config import app_config

product_list = []

class ProductsData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()
    
    def get_all_products(self):
        self.curr.execute("SELECT * FROM products")
        data = self.curr.fetchall()
        product_list = []
        for i, items in enumerate(data):
            productid, category_id, product_name, product_quantity, price = items

            fetched_data = dict(
                productid = int(productid),
                product_name = product_name,
                product_quantity = int(product_quantity),
                price = price
            )
            product = [product for product in product_list if productid == product["productid"]]
            if product:
                response = product_list
            else:
                product_list.append(fetched_data)
        response = product_list
        return response

    def check_category(self):
        """add a product category

        pick an existing category if available
        """
        # check if category exists
        query = "SELECT * FROM product_categories"
        self.curr.execute(query)
        data = self.curr.fetchall()
        categories = []
        for items in data:
            category_id, category_name = items
            fetched_categories = dict(
                category_id=category_id,
                category_name=category_name
            )
            categories.append(fetched_categories)
        return categories
    
    def add_category(self, product_category):
        # if category doesn't exist, add new category
        self.curr.execute("INSERT INTO product_categories (category_name) values(%s)",(product_category,))
        return self.db.commit()

    def add_product(self,product_category, product_name, product_quantity,price):
        # check if product category exists
        category = self.check_category()
        check_category = [product for product in category if product["category_name"]==product_category]
        if not check_category:
            self.add_category
        
        self.curr.execute("INSERT INTO products (category_id, product_name, product_quantity, price) VALUES(%s, %s, %s,  %s)", ("null", product_name,product_quantity, price,))
        return self.db.commit()
    
    # update a product
    def update_product(self, product_category, product_name, product_quantity,price, product_id):
        """update an existing product model
        """
        self.curr.execute("UPDATE products SET product_name=%s, product_quantity=%s, price=%s WHERE product_id=%s", (product_name, product_quantity, price, product_id))
        return self.db.commit()

    def delete_product(self, product_id):
        """delete a product model
        """
        self.curr.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        return self.db.commit()

    def get_single_product(self, product_id):
        self.curr.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
        data = self.curr.fetchone()

        if not data:
            return {"message":"Product Not Available"}, 404

        fetched_data = dict(productid= data[0],
                product_name =data[2],
                product_price =data[4],
                product_quantity = int(data[3])
            )
        return fetched_data
