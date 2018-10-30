import json
import unittest
from app import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # base tests url
        self.register = '/auth/signup'
        self.login = '/auth/login'
        self.products_url = '/products'
        self.single_product_url = '/products/110'

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
