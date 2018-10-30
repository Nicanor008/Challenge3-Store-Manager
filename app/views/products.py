from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.products import productsData, product_list

class Products(Resource):
    """Admin to add products to database
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = productsData()

    @jwt_required
    def post(self):
        data = request.get_json()

        productid = data.get("productid")
        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price")  

        if not data:
            response = jsonify ({"message":"fields cannot be empty"})
        elif not productid:
            response = jsonify ({"message":"Product ID required"})
        elif not product_name:
            response = jsonify ({"message":"Product name required"})
        elif not price:
            response = jsonify ({"message":"Price is a required field"})
        else:
            productsData().add_product(productid, product_category, product_name, product_quantity,price)
            response = jsonify ({'message':'product added successfully'})

        return response
    
    @jwt_required
    def get(self):
        products = productsData().get_all_products()
        return jsonify({"products":products})

class UpdateProduct(Resource):
    @jwt_required   
    def put(self, prodid):
        data = request.get_json()

        if not data:
            return {"message":"fields cannot be empty"}

        productid = data.get("productid")
        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price") 


        product = [product for product in product_list if productid == product["productid"]]
        if not product:
            print(product_list)
            return {"message":"product does not exist"}
        else:
            query_result = productsData().update_product(productid, product_category, product_name, product_quantity, price, prodid)
            if query_result:
                return {'message':'product updated'}
            else:
                return {'message':'failed'}

class DeleteProduct(Resource):
    def delete(self, prodid):
        # data = request.get_json()

        # if not data:
        #     return {"message":"fields cannot be empty"}
        productsData().delete_product(prodid)
        return {'message':'product deleted'}
