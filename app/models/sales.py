from app.models.db import init_db
from app.models.products import productsData
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims, get_jwt_identity)


sales_list = []

class salesData():
    def __init__(self):
        self.db = init_db()                             
        self.curr = self.db.cursor()
        self.product = productsData()
    
    def post_sale(self, product_name, product_quantity, price):
        # get product id from products table
        self.curr.execute("SELECT product_id, category_id, product_quantity FROM products WHERE product_name=%s",(product_name,))
        product = self.curr.fetchone()
        product_id = product[0]
        category_id = product[1]
        get_product_quantity = product[2]

        # get user attendant
        current_user = get_jwt_identity()
        self.curr.execute("SELECT * FROM users WHERE email=%s",(current_user,))
        user = self.curr.fetchone()
        employee_no = user[0]

        self.curr.execute("INSERT INTO sales(category_id,product_id, product_quantity, price, attended_by) VALUES(%s, %s,  %s,  %s, %s)", (category_id, product_id, product_quantity, price,employee_no,))
        self.db.commit()

        # update product quantity after sale
        new_product_quantity = int(get_product_quantity) - int(product_quantity)
        if new_product_quantity < 1:
            return {"message":"product out of stock"}
        print(new_product_quantity)
        self.curr.execute("UPDATE products SET product_quantity=%s WHERE product_id=%s",(new_product_quantity, product_id,))
        return self.db.commit()

    def get_all_sales_records(self):
        self.curr.execute("SELECT * FROM sales")
        data = self.curr.fetchall()
        for i, items in enumerate(data):
            sales_id, category_id, product_id, sold_quantity, price, attended_by = items

            # get product categories
            self.curr.execute("SELECT category_name FROM product_categories WHERE category_id=%s",(category_id,))
            category = self.curr.fetchone()
            product_category = category[0]

            # get products
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product = self.curr.fetchone()
            product_name = product[0]

            # get user who sold product
            attended_by = get_jwt_identity()

            fetched_data = dict(
                product_id = product_id,
                product_category = product_category,
                product_name = product_name,
                sold_quantity = sold_quantity,
                price = price,
                attended_by = attended_by
            )
            # sale = [sale for sale in sales_list if sales_id == sale["sales_id"]]
            # if sale:
            #     response = sales_list
            # else:
            sales_list.append(fetched_data)
        response = sales_list
        return response
    
