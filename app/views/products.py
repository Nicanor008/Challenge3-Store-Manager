from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.products import productsData

class Products(Resource, productsData):
    """Admin to add products to database
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = productsData()

    @jwt_required
    def post(self):
        data = request.get_json()

        if not data:
            return {"message":"fields cannot be empty"}

        productid = data["productid"]
        product_category = data["product_category"]
        product_name = data["product_name"]
        product_quantity =data["product_quantity"]
        price = data["price"]   

        self.user.add_user(productid, product_category, product_name, product_quantity,price)
        return {'response':'product added successfully'}
    
class UpdateProduct(Resource):
    @jwt_required
    def put(self, prodid):
        data = request.get_json()

        if not data:
            return {"message":"fields cannot be empty"}

        productid = data["productid"]
        product_category = data["product_category"]
        product_name = data["product_name"]
        product_quantity =data["product_quantity"]
        price = data["price"] 

        productsData().update_product(productid, product_category, product_name, product_quantity, price)
        return {'response':'product updated'}

class DeleteProduct(Resource):
    def delete(self, prodid):
        # data = request.get_json()

        # if not data:
        #     return {"message":"fields cannot be empty"}
        productsData().delete_product()
        return {'response':'product deleted'}
