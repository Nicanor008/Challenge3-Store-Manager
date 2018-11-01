from app.models.db import DbSetup
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from instance.config import app_config

product_list = []

class ProductsData(object):
    def __init__(self, config_name):
        self.db_init = DbSetup(config_name)
        self.db = self.db_init.init_db()                             
        self.curr = self.db.cursor()
    
    def get_all_products(self):
        self.curr.execute("SELECT * FROM products")
        data = self.curr.fetchall()
        product_list = []
        for i, items in enumerate(data):
            productid, category_id, product_name, product_quantity, price = items

            
            fetched_data = dict(
                productid = int(productid),
                # product_category = product_category,
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
        self.curr.execute("INSERT INTO product_categories(category_name) values(%s)",(product_category,))
        return self.db.commit()


    def add_product(self,product_category, product_name, product_quantity,price):
        # check if product category exists
        category = self.check_category()
        check_category = [product for product in category if product["category_name"]==product_category]
        if not check_category:
            self.add_category
        
        # self.curr.execute("SELECT * FROM product_categories WHERE category_name=%s",(product_category,))
        # category_data = self.curr.fetchone()
        # print(category_data)
        # category_id = category_data[0]
        self.curr.execute("INSERT INTO products(category_id, product_name, product_quantity, price) VALUES(%s, %s, %s,  %s)", ("null", product_name,product_quantity, price,))
        return self.db.commit()
    
    # update a product
    def update_product(self, product_category, product_name, product_quantity,price, prodid):
        """update an existing product model
        
        """
        # get category of the product category
        # self.curr.execute("SELECT category_id FROM products WHERE product_id=%s", (prodid,))
        # products_data = self.curr.fetchone()
        # productId = products_data[0]
        # update_query = self.curr.execute("UPDATE product_categories SET category_name=%s WHERE category_id=%s", (product_category, productId))
        # if not update_query:
        #     self.curr.execute("INSERT INTO product_categories(category_name) VALUES(%s)",(product_category,))
        #     self.db.commit()
        # product_category = self.check_category()
        # category = [category for category in product_category if category['category_name'] == product_category]
        # print(category)
        # if not category:
        #     self.curr.execute("INSERT INTO product_categories(category_name) VALUES(%s)",(product_category,))
        #     self.db.commit()
        #     self.check_category()
        self.curr.execute("UPDATE products SET product_name=%s, product_quantity=%s, price=%s WHERE product_id=%s", (product_name, product_quantity, price, prodid))
        return self.db.commit()

    def delete_product(self, prodid):
        """delete a product model
        
        """
        self.curr.execute("DELETE FROM products WHERE product_id=%s", (prodid,))
        return self.db.commit()
    
    # def get_single_products(self, product_id):
    #     self.curr.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    #     data = self.curr.fetchone()
    #     for i, items in enumerate(data):
    #         product_id, product_category, product_name, product_quantity, price = items
    #         fetched_data = dict(
    #             product_id = product_id,
    #             product_category = product_category,
    #             product_name = product_name,
    #             product_quantity = product_quantity,
    #             price = price
    #         )
    #         product = [product for product in product_list if product_id == product["product_id"]]
    #         if product:
    #             response = product_list
    #         else:
    #             product_list.append(fetched_data)
    #     response = product_list
    #     return response
