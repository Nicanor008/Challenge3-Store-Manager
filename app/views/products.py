from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from app.models.products import productsData, product_list

class Products(Resource):
    """Admin to add products to database
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = productsData()

    @jwt_required
    def post(self):
        """add a product to the database
        
        product is added by the admin
        """
        data = request.get_json()

        productid = data.get("productid")
        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price")  

         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return jsonify({"message": "Sorry, you don't have administrator rights"})
            
        # if product already exists
        product_exist = self.user.get_all_products()
        product_id_in_products = [product for product in product_exist if product["productid"]==productid]
        if len(product_id_in_products) != 0:
            return jsonify ({"message":"product already exist"})
        elif not data:
            return jsonify ({"message":"fields cannot be empty"})
        elif not productid:
            return jsonify ({"message":"Product ID required"})
        elif not product_name:
            return jsonify ({"message":"Product name required"})
        elif not price:
            return jsonify ({"message":"Price is a required field"})
        
        else:
            self.user.add_product(productid, product_category, product_name, product_quantity,price)
            return jsonify ({'message':'product added successfully'})

        # return response
    
    @jwt_required
    def get(self):
        """Fetch all products in database
        
        """
        products = productsData().get_all_products()
        return jsonify({"products":products})

class UpdateProduct(Resource):
    @jwt_required   
    def put(self, prodid):
        """updates a single requested product in a database
        """
        data = request.get_json()

        if not data:
            return {"message":"fields cannot be empty"}

        productid = data.get("productid")
        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price") 

        product = productsData().get_all_products()
        if not product:
            print(product_list)
            return {"message":"product does not exist"}
        else:
            query_result = productsData().update_product(productid, product_category, product_name, product_quantity, price, prodid)
            if not query_result:
                return {'message':'failed'}
            else:
                return {'message':'product updated'}

class DeleteProduct(Resource):
    """delete a product in a database
    
    The product should be existing in the database
    """
    def delete(self, prodid):
        # data = request.get_json()

        # if not data:
        #     return {"message":"fields cannot be empty"}
        productsData().delete_product(prodid)
        return {'message':'product deleted'}
