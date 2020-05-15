from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # Above we ran the request for register a new user
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
            # /auth endpoint requires to send json data.We convert data form to json in order to successfully received
            # headers say to web server in witch content type to look(Content-Type) and what kind of data we are sending
            # auth request returns a token(a dictionary like {'access_token': 'dhfhjdhsakh'(encrypted data jwt)}

                self.assertIn('access_token', json.loads(auth_response.data).keys())
                # Test see if in 'access_token' and auth_request data keys username and password

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # Above we ran the request once
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # Above we ran the request twice so it already exists

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))
