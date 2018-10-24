import unittest 
import json
from app import create_app


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
    
    # test register a store admin
    def test_RegisterAdmin(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nic",
                email="nicki@nic.com",
                password="nicki",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])

    # test register a store attendant 
    def test_RegisterAdmin(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nic",
                email="nicki@nic.com",
                password="nicki",
                role="attendant"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])

    def test_AdminLogin(self):
        response = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicki@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        if result:
            self.assertEqual(response.status_code, 200, result['response'])
        else:
            self.assertEqual(response.status_code, 401, result['response'])


        
