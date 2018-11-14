from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from app.models.products import ProductsData, product_list

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
            return make_response(jsonify({"message":"Product category required"}),404)
        elif not product_quantity:
            return make_response(jsonify({"message":"Product_quantity required"}),404)
        elif not product_name:
            return make_response(jsonify({"message":"Product name required"}),404)
        elif not price:
            return make_response(jsonify({"message":"Price is a required field"}), 404)
        
        else:
            add_product = self.user.add_product(product_category,product_name, product_quantity, price)
            return add_product
    
    @jwt_required
    def get(self):
        """Fetch all products in database
        """
        products = self.user.get_all_products()
        if products:
            return make_response(jsonify({"products":products}),200)
        else:
            return make_response(jsonify({"message":"No products available"}))

class UpdateProduct(Resource):
    def __init__(self):
        self.user = ProductsData()

    @jwt_required   
    def put(self, product_id):
        """updates a single requested product in a database
        """
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}), 403)

        data = request.get_json()

        if not data:
            return make_response(jsonify({"message":"fields cannot be empty"}),404)

        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price") 

        if not product_category:
            return make_response(jsonify({"message":"Product category cannot be empty"}), 404)
        elif not product_name:
            return make_response(jsonify({"message":"Product Name required"}), 404)
        else:
            data = self.user.update_product(product_category, product_name, product_quantity, price, product_id)
            return data            

class DeleteProduct(Resource):
    """delete a product in a database
    
    The product should be existing in the database
    """
    def __init__(self):
        self.user = ProductsData()

    @jwt_required
    def delete(self, product_id):
        delete_product = self.user.delete_product(product_id)
        return delete_product

# get individual product
class GetSingleProduct(Resource):
    def __init__(self):
        self.user = ProductsData()

    @jwt_required
    def get(self, product_id):
        products = self.user.get_all_products()
        check_product = [product for product in products if product["productid"] == product_id]
        if not check_product:
            product = self.user.get_single_product(product_id)
            return product
        else:
            return make_response(jsonify({"message":"product does not exist"}), 404)
