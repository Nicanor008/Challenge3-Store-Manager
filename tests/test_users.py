import json
from tests.base_test import BaseTest


class TestRegister(BaseTest):  
    # test register a user
    def test_Register_user(self):
        response = self.client.post(
            self.register,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps({
                "username":"Nic",
                "email":"nicki@nic.com",
                "password":"nicki",
                "role":"admin"
            }),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'user added successfully')
        self.assertEqual(response.status_code, 201)

        # test wrong email address 
    def test_wrong_email(self):
        response = self.client.post(
            self.register,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict(
                employee_no=1234,
                username="Nic",
                email="nickiniccom",
                password="nicki",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Invalid Email address')
        self.assertEqual(response.status_code, 400)
    
    # blank password
    def test_empty_password(self):
        response = self.client.post(
            self.register,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict(
                employee_no=12348,
                username="Nic",
                email="nicki@nic.com",
                password="",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Password field cannot be blank')
        self.assertEqual(response.status_code, 404)

    # blank email address
    def test_blank_email(self):
        response = self.client.post(
            self.register,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            data=json.dumps(dict(
                employee_no=12346,
                username="Nic",
                email="",
                password="nicki",
                role="admin"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Email cannot be blank')
        self.assertEqual(response.status_code, 404)
    
    # empty email on login
    def test_empty_email_onLogin(self):
        response = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="",
                password = "nicki"
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'email required')
        self.assertEqual(response.status_code, 404)

    # empty password on login
    def test_empty_password_onLogin(self):
        response = self.client.post(
            self.login,
            data = json.dumps(dict(
                email="nic@nic.com",
                password = ""
            )),
            content_type = 'application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'password required')
        self.assertEqual(response.status_code, 404) 

    # invalid email on login
    def test_wrong_email_onlogin(self):
        response = self.client.post(
            self.login,
            data=json.dumps(dict(
                email="nickniccom",
                password="nicki"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Invalid Email address')
        self.assertEqual(response.status_code, 400)   
    
    # test get single user
    def test_get_single_user(self):
        self.client.post(
           self.register,
            data=json.dumps({
                "username":"Nic",
                "email":"nicki@nic.com",
                "password":"nicki",
                "role":"admin"
            }),
            content_type='application/json' 
        )
        response = self.client.get(
            self.single_user,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # if not admin
        response = self.client.get(
            self.single_user,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    # test all sales
    def test_get_all_users(self):
        response = self.client.get( #admin can view all users
            self.all_users,
            headers = (dict(Authorization = 'Bearer ' + self.token_admin)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # if not admin
        response = self.client.get(
            self.all_users,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
