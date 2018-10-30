from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.sales import salesData

class Sales(Resource):
    """Store attendant to add sale record to database. Also can get a sale record from database that he/she posted
        """
    def __init__(self):
        self.user = salesData()

    @jwt_required
    def post(self):
        data = request.get_json()

        salesid = data.get('salesid')
        product_category = data.get('product_category')
        product_name = data.get('product_name')
        product_quantity = data.get('product_quantity')
        price = data.get('price')
        # attended_by = data.get('attended_by')  should be obtained automatically from the logged in user

        if not data:
            response = jsonify({"message":"fields cannot be empty"})
        elif not salesid:
            response = jsonify({"message":"salesid required"})
        elif not product_name:
            response = jsonify({"message":"product name required"})
        elif not price:
            response = jsonify({"message":"price required"})
        else:
            self.user.post_sale(salesid, product_category, product_name, product_quantity, price)
            response = jsonify({"message":"Sale record successfully added"})
        return response
    
    @jwt_required
    def get_all_sales(self):
        sales = self.user.get_all_sales_records()
        return jsonify({"Sales":sales})

            
