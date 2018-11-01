import json
import unittest
from app import create_app
from app.models.db import DbSetup


class BaseTest(unittest.TestCase):
    def setUp(self, config_name):
        self.app = create_app(config_name)
        self.app.testing = True
        self.client = self.app.test_client()

        # base tests url
        self.register = '/auth/signup'
        self.login = '/auth/login'
        self.products_url = '/products'
        self.single_product_url = '/products/110'

        with self.app.app_context():
            DbSetup(config_name).create_tables()
    
    def tearDown(self):
        # drop tables



    # admin login to post products
        self.login_admin = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="nic@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(self.login_admin.data.decode('utf-8'))
        self.token_admin = result["token"]

        self.register_attendant = self.client.post(
            self.register,
            data=json.dumps({
                "employee_no":1234,
                "username":"Nic",
                "email":"nicki@nic.com",
                "password":"nicki",
                "role":"attendant"
            }),
            content_type='application/json'
        )

        self.login_attendant = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="nicki@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        attendant_result = json.loads(self.login_attendant.data.decode('utf-8'))
        self.token_attendant = attendant_result["token"]

        # product in stock
        self.products = {
            "productid" : 110,
            "product_category" : "Smartphones",
            "product_name" : "Samsung Galaxy S7",
            "product_quantity" : 1,
            "price" : 70000,
            "added_by" : 12
        }

        # product after modifing
        self.product_update = {
            "productsid":12344,
            "product_category" : "Smartphones",
            "product_name" : "Samsung Galaxy S7",
            "product_quantity" : 2,
            "price" : 140000,
            "added_by" : 12
        }
