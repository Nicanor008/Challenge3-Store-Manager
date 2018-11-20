from tests.base_test import BaseTest
import json

class TestSale(BaseTest):
    def test_post_sale(self):
        self.client.post( # insert a product to be sold
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_id" : 110,
                "product_category" : "Smartphones",
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 3,
                "price" : 70000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        response = self.client.post( 
            self.sale_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 1,
                "price" : 34000
            })),
            content_type='application/json'
        )
    
    def test_get_sale(self):
        response = self.client.get( 
            self.sale_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

