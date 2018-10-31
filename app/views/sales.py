from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.sales import salesData, sales_list
from app.models.products import productsData

class Sales(Resource):
    """Store attendant to add sale record to database. Also can get a sale record from database that he/she posted
        """
    def __init__(self):
        self.user = salesData()
        self.products = productsData()

    @jwt_required
    def post(self):
        data = request.get_json()

        product_name = data.get('product_name')
        product_quantity = data.get('product_quantity')
        price = data.get('price')
        # attended_by = data.get('attended_by')  should be obtained automatically from the logged in user

        # check if product exists
        products = self.products.get_all_products()
        product = [product for product in products if product_name == product["product_name"]]
        if not product:
            return {"message":"product does not exist"}
        
        # check quantity
        products = self.products.get_all_products()
        check_quantity = [product for product in products if int(product["product_quantity"]) > product_quantity]
        print(check_quantity)
        if not check_quantity:
            return {"message":"Product quantity too high"}

        if not data:
            response = jsonify({"message":"fields cannot be empty"})
        elif not product_name:
            response = jsonify({"message":"product name required"})
        elif not price:
            response = jsonify({"message":"price required"})
        else:
            self.user.post_sale(product_name, product_quantity, price)
            response = jsonify({"message":"Sale record successfully added"})
        return response
    
    @jwt_required
    def get(self):
        """fetch all sale records

        Accessible to only admins
        """
        # if sales_list == []:
            # return {"message":"No sale record available"}
        # else:
        sales = self.user.get_all_sales_records()
        return jsonify({"Sales":sales})

            
