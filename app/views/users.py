import re
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)

# The required format of an email-address
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"       
   

class Register(Resource,):
    """Admin to register users
        Returns jsonify users data accordingly
    """
    def post(self):
        data = request.get_json()

        email = data["email"]
        password =data["password"]
        role = data["role"]  
        name = data["name"]    