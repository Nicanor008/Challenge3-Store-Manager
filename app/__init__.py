from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from instance.config import app_config
from flask_jwt_extended import JWTManager
from app.models.db import create_tables
from app.views.users import Register, Login, SingleUsers, All_Users
from app.views.products import Products, UpdateProduct, DeleteProduct
from app.models.users import users
from app.views.sales import Sales


version2 = Blueprint('api', __name__, url_prefix='/')
api = Api(version2)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    create_tables()
    

    # register the blueprint
    app.register_blueprint(version2)

    api.add_resource(Register, 'auth/signup')
    api.add_resource(Login, 'auth/login')
    api.add_resource(Products, 'products')
    api.add_resource(UpdateProduct, 'products/<prodid>')
    api.add_resource(DeleteProduct, 'products/<prodid>')
    api.add_resource(All_Users, 'auth/users')
    api.add_resource(SingleUsers, 'auth/users/<email>')
    api.add_resource(Sales, 'sales')


    app.config['JWT_SECRET_KEY'] = 'thisismysecretkey'
    jwt = JWTManager(app)
    
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'role':user['role']}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["email"]
  

    # # token attempts to access an endpoint
    @jwt.expired_token_loader
    def my_expired_token_callback():
        return jsonify({
            'message': 'The token has expired'
        }), 401

    return app