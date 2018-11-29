from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims, get_jwt_identity)
from app.models.sales import salesData, sales_list
from app.models.products import ProductsData
from app.models.db import init_db

class Sales(Resource):
    """Store attendant to add sale record to database. Also can get a sale record from database that he/she posted
    """
    def __init__(self):
        self.user = salesData()
        self.products = ProductsData()
        self.db = init_db()
        self.curr = self.db.cursor()

    @jwt_required
    def post(self):
        data = request.get_json()

        product_name = data.get('product_name')
        product_quantity = data.get('product_quantity')
        price = data.get('price')

         # user must be an attendant
        claims = get_jwt_claims()
        if claims['role'] == "admin":
            return make_response(jsonify({"message": "Sorry, you must be a Store Attendant"}), 403)

        # check if product exists
        products = self.products.get_all_products()
        product = [product for product in products if product_name == product["product_name"]]
        if not product:
            return make_response(jsonify({"message":"product does not exist"}), 400)
        
        # check quantity
        products = self.products.get_all_products()
        check_quantity = [product for product in products if product["product_quantity"] > product_quantity]
        zero_quantity = [product for product in products if product["product_quantity"] == 0]
        if not check_quantity:
            return make_response(jsonify({"message":"Product quantity too high"}),413)
        elif zero_quantity:
            return make_response(jsonify({"message":"Product out of stock"}))
        elif product_quantity == 0:
            return make_response(jsonify({"message":"Quantity to be sold cannot be zero"}))
        elif not product_name:
            return make_response(jsonify({"message":"product name required"}), 404)
        elif not price:
            return make_response(jsonify({"message":"price required"}), 404)
        else:
            sale = self.user.post_sale(product_name, product_quantity, price)
            return sale
    
    @jwt_required
    def get(self):
        """fetch all sale records
        Accessible to only admins
        """
        sales = self.user.get_all_sales_records()
        return sales

class Sale_SingleProduct(Resource):
    def __init__(self):
        self.user = salesData()
        self.products = ProductsData()
    
    @jwt_required
    def post(self, product_id):
        claims = get_jwt_claims()
        if claims['role'] != "attendant":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}), 403)
        
        sale_product = self.user.sale_single_product(product_id)
        return sale_product

class AdminGetSales(Resource):
    def __init__(self):
        self.user = salesData()

    @jwt_required
    def get(self):
        """fetch all sale records
        Accessible to only admins
        """
        sales = self.user.admin_get_all_sales_records()
        return sales
class DeleteSale(Resource):
    def __init__(self):
        self.user = salesData()

    @jwt_required
    def delete(self, sales_id):
        delete_sale = self.user.delete_sale(sales_id)
        return delete_sale

# get individual sale record
class GetSingleSale(Resource):
    def __init__(self):
        self.user = salesData()

    @jwt_required
    def get(self, sales_id):     
        sale = self.user.get_single_sale(sales_id)
        return sale

# get individual sale record
class AdminGetSingleSale(Resource):
    def __init__(self):
        self.user = salesData()

    @jwt_required
    def get(self, sale_id):     
        sale = self.user.admin_get_single_sale(sale_id)
        return sale

class UpdateSale(Resource):
    def __init__(self):
        self.user = salesData()
