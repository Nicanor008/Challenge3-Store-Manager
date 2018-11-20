from tests.base_test import BaseTest
import json

class TestProducts(BaseTest):
    def test_post_product(self):

        self.client.post(
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_id" : 110,
                "product_category" : "Smartphones",
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 1,
                "price" : 70000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        response = self.client.post(
            self.products_url,
            data=json.dumps(self.products),
            headers=(dict(Authorization = "Bearer " +self.token_admin)),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product already exist')
        self.assertEqual(response.status_code, 409)

    # test delete product . accessible to admin only
    def test_deleteProduct(self):
        # add a product first then delete it
        self.client.post(
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_category" : "Smartphones",
                "product_name" : "Techno Spark",
                "product_quantity" : 3,
                "price" : 19000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        response = self.client.delete(
            self.single_product_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)    

    # get products
    def test_get_products(self):
        self.client.post(
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_category" : "Smartphones",
                "product_name" : "Techno Spark",
                "product_quantity" : 3,
                "price" : 19000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_post_empty_category(self):
        response = self.client.post(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_empty_quantity(self):
        response = self.client.post(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_empty_product_name(self):
        response = self.client.post(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
    
    def test_modify_no_category(self):
        response = self.client.put(
            self.single_product_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_modify_no_product_name(self):
        response = self.client.put(
            self.single_product_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_modify_product(self):
        # add a product first then delete it
        self.client.post(
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_category" : "Smartphones",
                "product_name" : "Techno Spark",
                "product_quantity" : 3,
                "price" : 19000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        response = self.client.put(
            self.single_product_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict({
                "product_category" : "Smartphones",
                "product_name" : "Techno Spark",
                "product_quantity" : 3,
                "price" : 19000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
