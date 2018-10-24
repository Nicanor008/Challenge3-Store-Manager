from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from instance.config import app_config
from flask_jwt_extended import JWTManager
from app.models.db import create_tables
from app.views.users import Register, Login


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

    app.config['JWT_SECRET_KEY'] = 'thisismysecretkey'
    jwt = JWTManager(app)


    return app