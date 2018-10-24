import unittest 
import json
from app import create_app


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
    
    # test register a store attendant 
    def test_RegisterAttendant(self):
        response = self.client.post(
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
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])

    # test admin login
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
    
    # test attendant login
    def test_AttendantLogin(self):
        response = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicque@nic.com",
                password = "nicque"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['response'])
    
    # tests to logout all users, involves deletion of tokens
    def test_logout(self):
        response = self.client.delete(
            '/auth/logout',
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 200)


        
