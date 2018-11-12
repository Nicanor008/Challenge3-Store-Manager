import re
import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_claims)
from app.models.users import UsersData
from app.models.db import init_db

# The required format of an email-address
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"       

# user = UsersData()

class Register(Resource, UsersData):
    """Admin to register users
        Returns jsonify users data accordingly
    """
    def __init__(self):
        self.user = UsersData()

    @jwt_required
    def post(self):
        """add a store attendant to the database
        """
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return jsonify({"message": "Sorry, you don't have administrator rights"})
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")   

        roles = ['admin', 'attendant'] 

        # if user already exists
        user_exist = self.user.get_all_users()
        print(user_exist)
        user = [user for user in user_exist if user['email'] == email]
        print(user)
        if user:
            return make_response(jsonify({"message":"user already exist"}))
        try:
            if not email:
                response =  make_response(jsonify({"message":"Email cannot be blank"}), 404)
            elif not password:
                response =  make_response(jsonify({"message":"Password field cannot be blank"}), 404)
            elif not username:
                response =  make_response(jsonify({"message":"username field cannot be blank"}), 404)
            elif not role in roles:
                response =  make_response(jsonify({"message":"Role can only be ADMIN or ATTENDANT"}), 404)
            elif not re.match(email_format, email):
                response = make_response(jsonify({"message": "Invalid Email address"}), 400)  
            else:
                self.user.save( username, email, password,role)
                response = make_response(jsonify({'message':'user added successfully'}), 201)

            return response
        except Exception:
            return make_response(jsonify({"message":"user already exist"}))


class Login(Resource, UsersData):

    def __init__(self):
        self.user = UsersData()
        self.db = init_db()
        self.curr = self.db.cursor

    def post(self):
        """login users
        
        users should be already registered 
        """
        data = request.get_json()

        email = data["email"]
        password =data["password"]

        if not email:
            response = make_response(jsonify({"message":"email required"}), 404)
        elif not password:
            response = make_response(jsonify({"message":"password required"}), 404)
        elif not re.match(email_format, email):
            response = make_response(jsonify({"message": "Invalid Email address"}), 400)
        else:
            current_user = self.user.login(email, password) 
            if current_user:
                expires = datetime.timedelta(minutes=60)
                user = self.user.get_user(email)
                access_token = create_access_token(identity=user, expires_delta=expires)
                response = jsonify({"token":access_token, "message":"Login successful", "role":current_user})
            else:
                response =  jsonify({"Message":"wrong login credentials"}, 401)
           
        return response

class SingleUsers(Resource):
    """fetch single user in database using email

    Only accessible to admin
    """  
    def __init__(self):
        self.user = UsersData()

    @jwt_required          
    def get(self, email):
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return make_response(jsonify({"message": "Sorry, you don't have administrator rights"}), 403)
        
        response = self.user.get_user(email)
        return make_response(jsonify({"Users":response}),200)

class All_Users(Resource):
    """fetch all users in database
    
    only accessible to admin
    """  
    def __init__(self):
        self.user = UsersData()

    @jwt_required     
    def get(self):
         # user must be an admin
        claims = get_jwt_claims()
        if claims['role'] != "admin":
            return jsonify({"message": "Sorry, you don't have administrator rights"})
        response = self.user.get_all_users()
        return response
