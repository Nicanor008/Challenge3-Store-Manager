import re
import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.users import UsersData
from app.models.db import init_db

# The required format of an email-address
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"       

user = UsersData()

class Register(Resource, UsersData):
    """Admin to register users
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = UsersData()

    def post(self):
        data = request.get_json()

        employee_no = data.get("employee_no")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")   

        # handle already existing user

        # fields should not be empty
        if not data:
            response =  jsonify({"message":"Fields cannot be empty"})
        elif not employee_no:
            response =  jsonify({"message":"employee number cannot be blank"})
        elif not email:
            response =  jsonify({"message":"Email cannot be blank"})
        elif not password:
            response =  jsonify({"message":"Password field cannot be blank"})
        elif not username:
            response =  jsonify({"message":"username field cannot be blank"})
        elif not role:
            response =  jsonify({"message":"role field cannot be blank"})
        elif not re.match(email_format, email):
            response = jsonify({"message": "Invalid Email address"})  
        else:
            result = self.user.save(employee_no, username, email, password,role)
            response = {'message':'user added successfully'}

        return response


class Login(Resource, UsersData):

    def __init__(self):
        self.user = UsersData()
        self.db = init_db()
        self.curr = self.db.cursor()

    def post(self):
        """login users"""
        data = request.get_json()

        email = data["email"]
        password =data["password"]

        if not data:
            response = jsonify({"message":"email and password required"})
        elif not email:
            response = jsonify({"message":"email required"})
        elif not password:
            response = jsonify({"message":"password required"})
        elif not re.match(email_format, email):
            response = jsonify({"message": "Invalid Email address"})
        else:
            current_user = self.user.login(email, password)            
            if current_user:
                expires = datetime.timedelta(minutes=60)
                access_token = create_access_token(identity=email, expires_delta=expires)
                response = jsonify({"token":access_token, "message":"Login successful"})
            else:
                response =  jsonify({"Message":"wrong login credentials"})
           
        return response

class Users(Resource):
    # fetch all users in database
    def get(self, email):
        response = user.get_user(email)
        return jsonify({"Users":response})