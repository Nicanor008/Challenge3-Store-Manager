from app.models.db import init_db

class productsData():
    def __init__(self):
        self.db = init_db()                             
        self.curr = self.db.cursor()
    
        select_user = """SELECT * FROM products"""
        self.curr.execute(select_user)
        self.result = self.curr.rowcount > 1

    def add_user(self, productid, product_category, product_name, product_quantity,price):

        payload = {
            'productid':productid,
            'product_category':product_category,
            'product_name':product_name,
            'product_quantity':product_quantity,
            'price': price
        }

        if self.result:
            return {"product already exist"}

        # if employeeno is in payload:
        #     return {"message":"user already exists"}

        query = """INSERT INTO products(productid, product_category, product_name, product_quantity,price) 
        VALUES(%(productid)s, %(product_category)s,  %(product_name)s,  %(product_quantity)s,  %(price)s)"""

        # curr = self.db.cursor()
        self.curr.execute(query, payload)
        return self.db.commit()
    
    # update a product
    def update_product(self, productid, product_category, product_name, product_quantity,price):
        payload = {
            'productid':productid,
            'product_category':product_category,
            'product_name':product_name,
            'product_quantity':product_quantity,
            'price': price
        }

        if self.result:
            return {"product already exist"}

        # if employeeno is in payload:
        #     return {"message":"user already exists"}

        query = """UPDATE products SET productid=%(productid)s, product_category=%(product_category)s, 
        product_name=%(product_name)s, product_quantity=%(product_quantity)s, price=%(price)s WHERE productid=%(prodid)s """

        # curr = self.db.cursor()
        self.curr.execute(query, payload)
        return self.db.commit()

    def delete_product(self):

        query = """DELETE FROM products WHERE productid=%(prodid)s"""
        self.curr.execute(query)
        return self.db.commit()