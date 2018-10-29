import unittest 
import json
from app import create_app


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
    
    # test register a store admin
    def test_Register_user(self):
        response = self.client.post(
            '/auth/signup',
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
        self.assertEqual(result['message'], 'user added successfully')
        self.assertEqual(response.status_code, 200)

        #test wrong email address 
    def test_wrong_email(self):
        response = self.client.post(
            '/auth/signup',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nic",
                email="nickiniccom",
                password="nicki",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Invalid Email address')
        self.assertEqual(response.status_code, 200)
    
    # blank password
    def test_incorrect_email(self):
        response = self.client.post(
            '/auth/signup',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nic",
                email="nicki@nic.com",
                password="",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Password field cannot be blank')
        self.assertEqual(response.status_code, 200)

    # blank email address
    def test_incorrect_password(self):
        response = self.client.post(
            '/auth/signup',
            data=json.dumps(dict(
                employeeno=1234,
                username="Nic",
                email="",
                password="nicki",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Email cannot be blank')
        self.assertEqual(response.status_code, 200)


    def test_successful_Login(self):
        response = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nicki@nic.com",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Login successful!')
        self.assertEqual(response.status_code, 200)
    
    # empty email on login
    def test_empty_email_onLogin(self):
        response = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'email required')
        self.assertEqual(response.status_code, 200)

    # empty password on login
    def test_empty_password_onLogin(self):
        response = self.client.post(
            '/auth/login',
            data = json.dumps(dict(
                email="nic@nic.com",
                password = ""
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'password required')
        self.assertEqual(response.status_code, 200)
        
