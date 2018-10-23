import unittest 
import json
from app import create_app


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
       
       
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                name="Elsie Chep",
                username="Eldie",
                email="elsie@gmail.com",
                password="elsie",
                role="owner"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])

        
