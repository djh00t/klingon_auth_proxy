
"""
This module contains an HTTP server that requires authentication using JSON Web Tokens (JWTs).
The server reads a secret key from a file, or generates a new one if the file does not exist.
The server expects clients to send a JWT in a cookie with the name "token".
If the JWT is valid, the server responds with a 200 OK status code.
If the JWT is invalid or missing, the server responds with a 401 Unauthorized or 403 Forbidden status code.
"""
import http.server
import socketserver
import jwt
import os
import secrets

PORT = 9111

def get_or_create_secret_key(file_path):
    """
    Returns the secret key stored in the file at the given file path, or creates a new secret key and stores it in the file if the file does not exist.

    Args:
        file_path (str): The path to the file containing the secret key.

    Returns:
        str: The secret key.
    """
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(32)
        with open(file_path, "w") as file:
            file.write(secret_key)
        return secret_key

SECRET_KEY = get_or_create_secret_key(os.environ.get('SECRET_KEY_FILE', 'secret.key'))

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    """
    Handles authentication for HTTP requests.

    If a valid token is present in the request's cookie, the request is allowed to proceed.
    Otherwise, a 401 Unauthorized response is sent.
    """
    def do_GET(self):
        authorization_header = self.headers.get('Authorization')  # Extract token from Authorization header
        token = authorization_header[7:] if authorization_header and authorization_header.startswith('Bearer ') else None

        if not token:
            self.send_response(401)
            self.end_headers()
            return

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            self.send_response(200)
        except Exception:
            self.send_response(403)
        self.end_headers()

def run(server_class=socketserver.TCPServer, handler_class=AuthHandler, port=PORT):
    """
    Runs the server with the given server class, handler class, and port.

    Args:
        server_class (class): The server class to use.
        handler_class (class): The handler class to use.
        port (int): The port to serve on.
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving at port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
