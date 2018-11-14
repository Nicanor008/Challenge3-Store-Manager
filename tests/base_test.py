import json
import unittest
from app import create_app
from instance.config import app_config
from app.models.db import drop_tables, create_tables


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.app.config.from_object(app_config['testing'])   
        self.app.testing = True
        self.client = self.app.test_client()

        # base tests url
        self.register = '/auth/signup'
        self.login = '/auth/login'
        self.products_url = '/products'
        self.single_product_url = '/products/1'
        self.sale_url = '/sales'
        self.single_user = 'auth/users/nic@nic.com'
        self.all_users = 'auth/users'

        self.context = self.app.app_context()

        with self.context:
            create_tables()
        
        self.register_admin = self.client.post(
            self.register,
            data = json.dumps(dict(
                username="nicki",
                email="nickip@gmail.com",
                password = "nicki",
                role = "admin"
            )),
            content_type = 'application/json'
        )


        self.login_admin = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="nickip@gmail.com",
                password = "nickip"
            )),
            content_type = 'application/json'
        )
        result = json.loads(self.login_admin.data)
        self.token_admin = result['token']


        self.register_attendant = self.client.post(
            self.register,
            data = json.dumps(dict(
                username="nicanor",
                email="nicanor@nic.com",
                password = "nicnic",
                role = "attendant"
            )),
            content_type = 'application/json'
        )

    # attendant login to post products
        self.login_attendant = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="nicanor@nic.com",
                password = "nicnic"
            )),
            content_type = 'application/json'
        )
        result = json.loads(self.login_admin.data.decode('utf-8'))
        self.token_attendant = result["token"]

        # product in stock
        self.products = {
            "product_id" : 110,
            "product_category" : "Smartphones",
            "product_name" : "Samsung Galaxy S7",
            "product_quantity" : 1,
            "price" : 70000,
            "added_by" : 12
        }

        # product after modifing
        self.product_update = {
            "product_id":12344,
            "product_category" : "Smartphones",
            "product_name" : "Samsung Galaxy S7",
            "product_quantity" : 2,
            "price" : 140000,
            "added_by" : 12
        }
        

    def tearDown(self):
        drop_tables()