from base_test import BaseTest
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
            headers = (dict(Authorization = 'Bearer ' + self.token_attendant)),
            data=json.dumps(dict({
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 1,
                "price" : 34000
            })),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # test if price is empty
        empty_sale = self.client.post( 
            self.sale_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_attendant)),
            data=json.dumps(dict({
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 1,
                "price" : ""
            })),
            content_type='application/json'
        )
        result_empty_sale = json.loads(empty_sale.data.decode('utf-8'))
        self.assertEqual(result_empty_sale['message'], 'price required')
        self.assertEqual(empty_sale.status_code, 404)

        # test product does not exist
        empty_name = self.client.post( 
            self.sale_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_attendant)),
            data=json.dumps(dict({
                "product_name" : "lapy laptop",
                "product_quantity" : 1,
                "price" : 4000
            })),
            content_type='application/json'
        )
        result_empty_name = json.loads(empty_name.data.decode('utf-8'))
        self.assertEqual(result_empty_name['message'], 'product does not exist')
        self.assertEqual(empty_name.status_code, 400)
    
    def test_get_sale(self):
        response = self.client.get( #admin can view all sales
            self.sale_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

