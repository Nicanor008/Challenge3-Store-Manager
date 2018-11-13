from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_cors import CORS
from instance.config import app_config
from flask_jwt_extended import JWTManager
from app.models.db import create_tables, default_admin
from app.views.users import Register, Login, SingleUsers, All_Users
from app.views.products import Products, UpdateProduct, DeleteProduct, GetSingleProduct
from app.models.users import users
from app.views.sales import Sales, DeleteSale, GetSingleSale


version2 = Blueprint('api', __name__, url_prefix='/')
api = Api(version2)

def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    create_tables()
    default_admin()
    CORS(app)
    
    # register the blueprint
    app.register_blueprint(version2)

    api.add_resource(Register, 'auth/signup')
    api.add_resource(Login, 'auth/login')
    api.add_resource(Products, 'products')
    api.add_resource(UpdateProduct, 'products/<product_id>')
    api.add_resource(DeleteProduct, 'products/<product_id>')
    api.add_resource(GetSingleProduct, 'products/<product_id>')
    api.add_resource(All_Users, 'auth/users')
    api.add_resource(SingleUsers, 'auth/users/<email>')
    api.add_resource(Sales, 'sales')
    api.add_resource(DeleteSale, 'sales/<sales_id>')
    api.add_resource(GetSingleSale, 'sales/<sales_id>')


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