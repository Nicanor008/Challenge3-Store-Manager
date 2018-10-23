from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config
from app.views.users import Register


challenge3 = Blueprint('api', __name__, url_prefix='/')
api = Api(challenge3)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    
    # register the blueprint
    app.register_blueprint(challenge3)

    app.config['JWT_SECRET_KEY'] = 'thisismysecretkey'
    jwt = JWTManager(app)

    api.add_resource(Register, '/auth/register')

    return app