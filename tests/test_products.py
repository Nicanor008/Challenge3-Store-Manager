from base_test import BaseTest
import json

class TestProducts(BaseTest):
    def test_post_product(self):
        response = self.client.post(
            '/products',
            data=json.dumps(self.products),
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product added successfully')
        self.assertEqual(response.status_code, 200)

    # test modify a single product. Accessible to only admin
    def test_modifyProduct(self):
        self.client.post(
            '/products',
            data=json.dumps({
                "productsid":12374,
                "product_category" : "Smartphones",
                "product_name" : "Samsung Galaxy S7",
                "product_quantity" : 2,
                "price" : 140000,
                "added_by" : 12
            }),
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        response = self.client.put(
            '/products/123444',
            headers=dict(Authorization = "Bearer " + self.token_admin ),
            data=json.dumps(self.product_update),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product updated')
        self.assertEqual(response.status_code, 200)

    # modify a product that does not exist

    # modify a product as a store attendant


    # test delete product . accessible to admin only
    def test_deleteProduct(self):
        # add a product first then delete it
        self.client.post(
            '/products',
            data=json.dumps({
                "productsid":1374,
                "product_category" : "Smartphones",
                "product_name" : "Techno Spark",
                "product_quantity" : 3,
                "price" : 19000,
                "added_by" : 12
            }),
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        response = self.client.delete(
            '/products/123444',
            headers=dict(Authorization = "Bearer " + self.token_admin),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'product deleted')
        self.assertEqual(response.status_code, 200)
    
    # delete a product that does not exist

    # delete a product as a store attendant

    # get products
    # def test_get_products(self):
    #      # add a product first then delete it
    #     response = self.client.get(
    #         '/products',
    #         headers=dict(Authorization = "Bearer " + self.token_admin),
    #         content_type='application/json'
    #     )
    #     json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)

    # get null products

    