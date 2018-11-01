from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from app.models.products import ProductsData

class Products(Resource):
    """Admin to add products to database
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = ProductsData()

    @jwt_required
    def post(self):
        """add a product to the database
        
        product is added by the admin
        """
        data = request.get_json()

        product_name = data.get("product_name")
        product_category = data.get("product_category")
        product_quantity =data.get("product_quantity")
        price = data.get("price")  

         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}))
            
        # if product already exists
        product_exist = self.user.get_all_products()
        check_product = [product for product in product_exist if product["product_name"]==product_name]
        if check_product:
            return make_response(jsonify({"message":"product already exist"}), 409)
        elif not product_category:
            return make_response(jsonify({"message":"Product category required"}),400)
        elif not product_quantity:
            return make_response(jsonify({"message":"Product_quantity required"}),400)
        elif not product_name:
            return make_response(jsonify({"message":"Product name required"}),400)
        elif not price:
            return make_response(jsonify({"message":"Price is a required field"}), 400)
        
        else:
            self.user.add_product(product_category,product_name, product_quantity, price)
            return make_response(jsonify({'message':'product added successfully'}),201)
    
    @jwt_required
    def get(self):
        """Fetch all products in database
        """
        products = self.user.get_all_products()
        if not products:
            return make_response(jsonify({"message":"No products available"}),204)
        
        return make_response(jsonify({"products":products}),200)

class UpdateProduct(Resource):
    def __init__(self):
        self.user = ProductsData()

    @jwt_required   
    def put(self, prodid):
        """updates a single requested product in a database
        """
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}), 403)

        data = request.get_json()

        if not data:
            return make_response(jsonify({"message":"fields cannot be empty"}),400)

        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price") 

        if not product_category:
            return make_response(jsonify({"message":"Product category cannot be empty"}), 400)
        elif not product_name:
            return make_response(jsonify({"message":"Product Name required"}), 400)
        else:
            data = self.user.update_product(product_category, product_name, product_quantity, price, prodid)
            return make_response(jsonify({'message':'product successfully updated'}), 201)

            

class DeleteProduct(Resource):
    """delete a product in a database
    
    The product should be existing in the database
    """
    def __init__(self):
        self.user = ProductsData()

    @jwt_required
    def delete(self, prodid):
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}),403)

        products = self.user.get_all_products()
        check_product = [product for product in products if product["productid"] == prodid]
        if not check_product:
            self.user.delete_product(prodid)
            return make_response(jsonify({'message':'product deleted'}), 200)
        else:
            return make_response(jsonify({"message":"product does not exist"}), 400)
