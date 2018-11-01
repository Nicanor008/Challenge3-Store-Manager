from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.sales import salesData, sales_list
from app.models.products import ProductsData

class Sales(Resource):
    """Store attendant to add sale record to database. Also can get a sale record from database that he/she posted
    """
    def __init__(self):
        self.user = salesData()
        self.products = ProductsData()

    @jwt_required
    def post(self):
        data = request.get_json()

        product_name = data.get('product_name')
        product_quantity = data.get('product_quantity')
        price = data.get('price')

        # check if product exists
        products = self.products.get_all_products()
        product = [product for product in products if product_name == product["product_name"]]
        if not product:
            return make_response(jsonify({"message":"product does not exist"}), 400)
        
        # check quantity
        products = self.products.get_all_products()
        check_quantity = [product for product in products if int(product["product_quantity"]) > product_quantity]
        print(check_quantity)
        if not check_quantity:
            return make_response(jsonify({"message":"Product quantity too high"}),413)

        if not product_name:
            response = make_response(jsonify({"message":"product name required"}), 400)
        elif not price:
            response = make_response(jsonify({"message":"price required"}), 400)
        else:
            self.user.post_sale(product_name, product_quantity, price)
            response = make_response(jsonify({"message":"Sale record successfully added"}), 201)
        return response
    
    @jwt_required
    def get(self):
        """fetch all sale records
        Accessible to only admins
        """
        sales = self.user.get_all_sales_records()
        if not sales:
            return make_response(jsonify({"message":"No sale records"}))
            
        return make_response(jsonify({"Sales":sales}), 200)
