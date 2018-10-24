import re
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.models.users import UsersData

# The required format of an email-address
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"       
   

class Register(Resource, UsersData):
    """Admin to register users
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = UsersData()

    def post(self):
        data = request.get_json()

        employeeno = data["employeeno"]
        username = data["username"]
        email = data["email"]
        password =data["password"]
        role = data["role"]   

        result = self.user.save(employeeno, username, email, password,role)
        return {'response':'user added successfully'}


class Login(Resource, UsersData):

    def __init__(self):
        self.user = UsersData()

    def post(self):
        """login users"""
        data = request.get_json()

        email = data["email"]
        password =data["password"]

        result = self.user.login(email, password)
        access_token = create_access_token(identity=email)
        return jsonify(token = access_token, message = "Login successful!")
