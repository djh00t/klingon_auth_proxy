import unittest
import login
from flask import json

class TestLoginApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src.login.app.testing = True
        cls.client = src.login.app.test_client()

    # No changes needed if the test is working correctly

    def test_login_failure(self):
        # Test login with incorrect credentials
        response = self.client.post('/login', data={'username': 'test-admin', 'password': 'wrongpassword'})
        # Check for 401 Unauthorized
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
