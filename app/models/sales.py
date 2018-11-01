from app.models.db import init_db
from instance.config import app_config
from app.models.products import ProductsData
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims, get_jwt_identity)


sales_list = []

class salesData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()
    
    def post_sale(self, product_name, product_quantity, price):
        self.curr.execute("SELECT product_id, category_id, product_quantity FROM products WHERE product_name=%s",(product_name,))
        product = self.curr.fetchone()
        product_id = product[0]
        existing_product_quantity = product[2]

        # get user attendant
        current_user = get_jwt_identity()
        self.curr.execute("SELECT * FROM users WHERE email=%s",(current_user,))
        user = self.curr.fetchone()
        employee_no = user[0]

        self.curr.execute("INSERT INTO sales(category_id,product_id, product_quantity, price, attended_by) VALUES(%s, %s,  %s,  %s, %s)", (1, product_id, product_quantity, price,employee_no,))
        self.db.commit()

        # update product quantity after sale
        new_product_quantity = int(existing_product_quantity) - int(product_quantity)
        if new_product_quantity < 1:
            return {"message":"product out of stock"}
        self.curr.execute("UPDATE products SET product_quantity=%s WHERE product_id=%s",(new_product_quantity, product_id,))
        return self.db.commit()

    def get_all_sales_records(self):
        self.curr.execute("SELECT * FROM sales")
        data = self.curr.fetchall()
        for i, items in enumerate(data):
            sales_id, category_id, product_id, sold_quantity, price, attended_by = items

              # get products
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product = self.curr.fetchone()
            product_name = product[0]

            # get user who sold product
            attended_by = get_jwt_identity()

            fetched_data = dict(
                product_id = product_id,
                product_name = product_name,
                sold_quantity = sold_quantity,
                price = price,
                attended_by = attended_by
            )
            sales_list.append(fetched_data)
        response = sales_list
        return response
