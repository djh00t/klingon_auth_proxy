import unittest
import src.login_app
from flask import json

class TestLoginApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src.login_app.app.testing = True
        cls.client = login_app.app.test_client()

    def test_login_success(self):
        # Test login with correct credentials
        response = self.client.post('/login', data={'username': 'admin', 'password': 'password123'})
        # Check for redirect (302) and set-cookie header
        self.assertEqual(response.status_code, 302)
        self.assertTrue('Set-Cookie' in response.headers)

    def test_login_failure(self):
        # Test login with incorrect credentials
        response = self.client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'})
        # Check for 401 Unauthorized
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
