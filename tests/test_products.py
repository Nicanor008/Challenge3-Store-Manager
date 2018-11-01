from base_test import BaseTest
import json

class TestProducts(BaseTest):
    def test_post_product(self):
        response = self.client.post(
            self.products_url,
            data=json.dumps(self.products),
            headers=(dict(Authorization = "Bearer " +self.token_admin)),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product added successfully')
        self.assertEqual(response.status_code, 201)

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
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product deleted')
        self.assertEqual(response.status_code, 200)
    

    # get products
    def test_get_products(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
    
    
    def test_post_empty_category(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Product category required')
        self.assertEqual(response.status_code, 404)

    def test_post_empty_quantity(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Product quantity required')
        self.assertEqual(response.status_code, 404)

    def test_post_empty_product_name(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Product name required')
        self.assertEqual(response.status_code, 404)
    
    def test_product_exists(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'product already exist')
        self.assertEqual(response.status_code, 409)
    
    def test_no_products_available(self):
        response = self.client.get(
            self.products_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'No products available')
        self.assertEqual(response.status_code, 204)

    def test_modify_no_category(self):
        response = self.client.get(
            self.single_product_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Product category cannot be empty')
        self.assertEqual(response.status_code, 404)

    def test_modify_no_product_name(self):
        response = self.client.get(
            self.single_product_url,
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Product Name required')
        self.assertEqual(response.status_code, 404)
    
    def test_modify_product(self):
        # add a product first then delete it
        response = self.client.put(
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
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product successfully updated')
        self.assertEqual(response.status_code, 201)
    
    def test_attendant_to_modify_product(self):
        response = self.client.put(
            self.products_url,
            headers = (dict(Authorization = 'Bearer ' + self.token_attendant )),
            data=json.dumps(dict({
                "product_category" : "Smartphones",
                "product_name" : "Techno Boom",
                "product_quantity" : 2,
                "price" : 19000,
                "added_by" : 12
            })),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Sorry, you don\'t have administrator rights')
        self.assertEqual(response.status_code, 403)


    