import unittest
from src import app
import jwt
import os
from http.server import HTTPServer
from socketserver import BaseRequestHandler
from http.client import HTTPConnection
import threading

class TestAuthHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generating a test secret key
        cls.test_secret_key = 'test_secret_key'
        app.SECRET_KEY = cls.test_secret_key
        # Starting the server in a new thread
        cls.server = HTTPServer(('', app.PORT), app.AuthHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def test_valid_token(self):
        # Generate a valid token
        valid_token = jwt.encode({'user': 'test_user'}, self.test_secret_key, algorithm="HS256")
        # Make a request with the valid token
        conn = HTTPConnection("localhost", app.PORT)
        conn.request("GET", "/", headers={"Authorization": f"Bearer {valid_token}"})
        response = conn.getresponse()
        # Test that the response is 200 OK
        self.assertEqual(response.status, 200)

    def test_invalid_token(self):
        # Make a request with an invalid token
        conn = HTTPConnection("localhost", app.PORT)
        conn.request("GET", "/", headers={"Authorization": "Bearer invalid_token"})
        response = conn.getresponse()
        # Test that the response is 403 Forbidden
        self.assertEqual(response.status, 403)

if __name__ == '__main__':
    unittest.main()
