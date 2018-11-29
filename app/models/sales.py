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
        try:
            isinstance(int(price), int)
            isinstance(int(product_quantity), int)
            self.curr.execute("SELECT product_id, category_id, product_quantity FROM products WHERE product_name=%s",(product_name,))
            product = self.curr.fetchone()
            product_id = product[0]
            existing_product_quantity = product[2]

            # get user attendant
            current_user = get_jwt_identity()
            self.curr.execute("SELECT employee_no FROM users WHERE email=%s",(current_user,))
            employee_no = self.curr.fetchone()

            self.curr.execute("INSERT INTO sales (category_id,product_id, product_quantity, price, attended_by) VALUES(%s, %s,  %s,  %s, %s)", (1, product_id, product_quantity, price,employee_no,))
            self.db.commit()

            # update product quantity after sale
            new_product_quantity = int(existing_product_quantity) - int(product_quantity)
            if new_product_quantity < 0:
                return {"message":"product out of stock"}
            self.curr.execute("UPDATE products SET product_quantity=%s WHERE product_id=%s",(new_product_quantity, product_id,))
            self.db.commit()
            return {'message':'Sale record posted Successfully'}
        except ValueError:
            response = {'message':'Product Quantity and Price should only be an integer'}
            return response

    def get_all_sales_records(self):
        claims = get_jwt_claims()
        if claims['role'] != "attendant":
            return {"message": "Sorry, you must be an attendant"}

        attended_by = get_jwt_identity()
        self.curr.execute("SELECT employee_no FROM users WHERE email=%s", (attended_by,))
        current_user = self.curr.fetchone()

        self.curr.execute("SELECT * FROM sales WHERE attended_by=%s", (current_user,))
        data = self.curr.fetchall()
        if not data:
            return {"message":"No sale records"}

        for i, items in enumerate(data):
            sales_id, category_id, product_id, sold_quantity, price, attended_by = items

              # get products
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product_name = self.curr.fetchone()
            
            # get user who sold product
            attended_by = get_jwt_identity()

            fetched_data = dict(
                sales_id = sales_id,
                product_id = product_id,
                product_name = product_name,
                sold_quantity = sold_quantity,
                price = price,
                attended_by = attended_by
            )
            user = [user for user in sales_list if sales_id == user["sales_id"]]
            if user:
                response = sales_list
            elif not product_name:
                response = sales_list
            else:
                sales_list.append(fetched_data)
        response = sales_list
        return response

    def admin_get_all_sales_records(self):
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return {"message": "Sorry, you must be an administrator"}

        self.curr.execute("SELECT * FROM sales")
        data = self.curr.fetchall()
        if not data:
            return {"message":"No sale records"}

        for i, items in enumerate(data):
            sales_id, category_id, product_id, sold_quantity, price, attended_by = items

              # get products
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product_name = self.curr.fetchone()
            
            # get user who sold product
            attended_by = get_jwt_identity()

            fetched_data = dict(
                sales_id = sales_id,
                product_id = product_id,
                product_name = product_name,
                sold_quantity = sold_quantity,
                price = price,
                attended_by = attended_by
            )
            user = [user for user in sales_list if sales_id == user["sales_id"]]
            if user:
                response = sales_list
            elif not product_name:
                response = sales_list
            else:
                sales_list.append(fetched_data)
        response = sales_list
        return response

    def get_single_sale(self, sales_id):
        try:
            isinstance(int(sales_id), int)
            attended_by = get_jwt_identity()

            self.curr.execute("SELECT employee_no FROM users WHERE email=%s", (attended_by,))
            current_user = self.curr.fetchone()
            self.curr.execute("SELECT * FROM sales WHERE sales_id=%s and attended_by=%s", (sales_id,current_user))
            data = self.curr.fetchone()

            if not data:
                return {"message":"Sale Record Not Available"}, 404

            product_id = data[2]

            # get product name
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product_name = self.curr.fetchone()

            # get user attendant
            current_user = get_jwt_identity()

            fetched_data = dict(
                    sales_id=data[0],
                    product_id= data[2],
                    product_name = product_name,
                    product_price =data[4],
                    product_quantity = int(data[3]),
                    attended_by = current_user
                )
            return fetched_data
        except ValueError:
            response = {'message':'Sales ID should be an integer'}
            return response
        
    def admin_get_single_sale(self, sale_id):
        try:
            isinstance(int(sale_id), int)
            claims = get_jwt_claims()
            if claims['role'] != "admin":
                return {"message": "Sorry, you must be an administrator"}

            self.curr.execute("SELECT * FROM sales WHERE sales_id=%s", (sale_id,))
            data = self.curr.fetchone()

            if not data:
                return {"message":"Sale Record Not Available"}, 404

            product_id = data[2]

            # get product name
            self.curr.execute("SELECT product_name FROM products WHERE product_id=%s",(product_id,))
            product_name = self.curr.fetchone()

            # get user attendant
            current_user = get_jwt_identity()

            fetched_data = dict(
                    sales_id=data[0],
                    product_id= data[2],
                    product_name = product_name,
                    product_price =data[4],
                    product_quantity = int(data[3]),
                    attended_by = current_user
                )
            return fetched_data
        except ValueError:
            response = {'message':'Sales ID should be an integer'}
            return response

    def delete_sale(self, sales_id):
        try:
            isinstance(int(sales_id), int)
            sales = self.get_all_sales_records()
            check_product = [product for product in sales if product["sales_id"]==sales_id]
            if not check_product:
                return {"message":"Sale Record does not exist"}
            else:
                self.curr.execute("DELETE FROM sales WHERE sales_id=%s", (sales_id,))
                self.db.commit()
                return {"message":"Sale Record Deleted"}, 200
        except ValueError:
            response = {'message':'Sales ID should only be an integer'}
            return response

    # sale single products using ID
    def sale_single_product(self, product_id):
        try:
            isinstance(int(product_id), int)
            self.curr.execute("SELECT category_id, product_quantity, price FROM products WHERE product_id=%s",(product_id,))
            product = self.curr.fetchone()
            # product_id = product[0]
            existing_product_quantity = product[1]
            price = product[2]

            # get user attendant
            current_user = get_jwt_identity()
            self.curr.execute("SELECT employee_no FROM users WHERE email=%s",(current_user,))
            employee_no = self.curr.fetchone()

            self.curr.execute("INSERT INTO sales (category_id,product_id, product_quantity, price, attended_by) VALUES(%s, %s,  %s,  %s, %s)", (1, product_id, 1, price,employee_no,))
            self.db.commit()

            # update product quantity after sale
            new_product_quantity = int(existing_product_quantity) - 1
            if new_product_quantity < 0:
                return {"message":"product out of stock"}
            self.curr.execute("UPDATE products SET product_quantity=%s WHERE product_id=%s",(new_product_quantity, product_id,))
            self.db.commit()
            return {'message':'Sale record posted Successfully'}
        except ValueError:
            response = {'message':'Product ID should only be an integer'}
            return response