import json
import unittest
from app import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # register a store attendant 
        self.register_attendant = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nicque",
                email="nicque@nic.com",
                password="nicque",
                role="attendant"
            )),
            content_type='application/json'
        )

        # login attendant and generate a token
        self.login_admin = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nii@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(self.login_admin.data.decode('utf-8'))
        self.token_admin = result["token"]

    # admin login to post products
        self.login_admin = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicki@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(self.login_admin.data.decode('utf-8'))
        self.token_admin = result["token"]
    
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
