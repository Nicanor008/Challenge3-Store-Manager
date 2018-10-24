from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from instance.config import app_config


challenge3 = Blueprint('api', __name__, url_prefix='/')
api = Api(challenge3)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    
    # register the blueprint
    app.register_blueprint(challenge3)


    return app