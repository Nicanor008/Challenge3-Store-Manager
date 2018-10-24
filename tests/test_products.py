import json
from base_test import BaseTest

class TestProducts(BaseTest):
    def setup(self):
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

    # admin login
        self.login_admin = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicki@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.token_admin = result["token"]
    
    # attendant login
        self.login_attendant = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicque@nic.com",
                password = "nicque"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.token_attendant = result['token']
    
        # products
        self.products = {
            "productsid":123444,
            "product_category" : "Smartphones",
            "product_name" : "Samsung Galaxy S7",
            "product_quantity" : 1,
            "price" : 70000,
            "added_by" : 12
        }


    # test modify a single product. Accessible to only admin
    def test_modifyProduct(self):
        update_result = self.client.put(
            '/products/123444',
            headers=dict(Authorization = "Bearer " + self.token_admin )
            data=json.dumps(
                "product quantity" : 3,
                "price": 80000
            ),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])

    
    # test delete product . accessible to admin
    def test_deleteProduct(self):
        update_result = self.client.delete(
            '/products/123444',
            headers=dict(Authorization = "Bearer " + self.token_admin)
            data=json.dumps(
                "product quantity" : 3,
                "price": 80000
            ),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        if result:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    