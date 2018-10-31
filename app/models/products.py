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
        product_list = []
        for i, items in enumerate(data):
            productid, category_id, product_name, product_quantity, price = items

            # get product categories
            # self.curr.execute("SELECT category_name FROM product_categories WHERE category_id=%s",(category_id,))
            # data = self.curr.fetchone()
            # product_category = category[0]
            # print(product_category)
            data = self.check_category()
            print(data)
            # for 
            product_category = data[1]


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
        for i, items in enumerate(data):
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


    def add_product(self,category_id, product_name, product_quantity,price):
        # check if product category exists
        category = self.check_category()
        check_category = [product for product in category if product['category_id']==category_id]
        if check_category:
            self.add_category
            
        self.curr.execute("INSERT INTO products(category_id, product_name, product_quantity, price) VALUES(%s, %s, %s,  %s)", (category_id, product_name,product_quantity, price,))
        return self.db.commit()
    
    # update a product
    def update_product(self, product_category, product_name, product_quantity,price, prodid):
        """update an existing product model
        
        """
        # get category of the product category
        self.curr.execute("SELECT category_id FROM products WHERE product_id=%s", (prodid,))
        products_data = self.curr.fetchone()
        print(products_data)
        productId = products_data[0]
        update_query = self.curr.execute("UPDATE product_categories SET category_name=%s WHERE category_id=%s", (product_category, productId))
        if not update_query:
            self.curr.execute("INSERT INTO product_categories(category_name) VALUES(%s)",(product_category,))
            self.db.commit()
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
