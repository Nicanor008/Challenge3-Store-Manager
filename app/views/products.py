from flask import request, jsonify, make_response
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
            return make_response(jsonify({"message":"product already exist"}))
        elif not data:
            return make_response(jsonify({"message":"fields cannot be empty"}))
        elif not product_category:
            return make_response(jsonify({"message":"Product category required"}))
        elif not product_quantity:
            return make_response(jsonify({"message":"Product_quantity required"}))
        elif not product_name:
            return make_response(jsonify({"message":"Product name required"}))
        elif not price:
            return make_response(jsonify({"message":"Price is a required field"}))
        
        else:
            self.user.check_category(product_category,product_name, product_quantity, price)
            return make_response(jsonify({'message':'product added successfully'}))

        # return response
    
    @jwt_required
    def get(self):
        """Fetch all products in database
        
        """
        products = productsData().get_all_products()
        return make_response(jsonify({"products":products}))

class UpdateProduct(Resource):
    def __init__(self):
        self.user = productsData()

    @jwt_required   
    def put(self, prodid):
        """updates a single requested product in a database
        """
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}))

        data = request.get_json()

        if not data:
            return {"message":"fields cannot be empty"}

        product_category = data.get("product_category")
        product_name = data.get("product_name")
        product_quantity =data.get("product_quantity")
        price = data.get("price") 

        # products = self.user.get_all_products()
        # check_product = [product for product in products if product['productid'] == prodid]
        # if len(check_product) == 0:
        #     return make_response(jsonify({"message":"product does not exist"}))
        if not product_category:
            return make_response(jsonify({"message":"Product category cannot be empty"}))
        elif not product_name:
            return make_response(jsonify({"message":"Product Name required"}))
        else:
            self.user.update_product(product_category, product_name, product_quantity, price, prodid)
            
            return make_response(jsonify({'message':'product successfully updated'}))
            

class DeleteProduct(Resource):
    """delete a product in a database
    
    The product should be existing in the database
    """
    def __init__(self):
        self.user = productsData()

    @jwt_required
    def delete(self, prodid):
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}))

        # if product exists, delete, if not prompt a user
        # if product already exists
        products = self.user.get_all_products()
        check_product = [product for product in products if product["productid"] == prodid]
        if not check_product:
            self.user.delete_product(prodid)
            return make_response(jsonify({'message':'product deleted'}))
        else:
            return make_response(jsonify({"message":"product does not exist"}))

# class GetSingleProduct(Resource):
#     def __init__(self):
#         self.user = productsData()

#     @jwt_required
#     def get(self, product_id):
#         # get a single product. accessible to all users
#         product = self.user.get_single_products(product_id)
#         return {"Product":product}
