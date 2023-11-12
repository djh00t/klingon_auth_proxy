
"""
This module contains a Flask application that provides a login functionality. 
It uses JWT for authentication and authorization. 
The module defines a function to get or create a secret key, which is used to sign the JWT tokens. 
The module also defines a dummy user data for user validation. 
The login function handles GET and POST requests, and returns a response with a JWT token if the user is authenticated. 
"""
from flask import Flask, request, make_response, redirect, render_template
import jwt
import os
import secrets

app = Flask(__name__)

def get_or_create_secret_key(file_path):
    """
    Returns the secret key stored in the given file path, or creates a new one if the file does not exist.
    
    Args:
    - file_path (str): The path to the file containing the secret key.
    
    Returns:
    - str: The secret key.
    """
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(32)
        with open(file_path, "w") as file:
            file.write(secret_key)
        return secret_key

SECRET_KEY = get_or_create_secret_key("secret.key")
HTACCESS_FILE = "./secrets"

def check_credentials(username, password):
    """
    Check if the given username and password are valid by comparing them to the contents of the .htaccess file.
    
    Args:
        username (str): The username to check.
        password (str): The password to check.
    
    Returns:
        bool: True if the username and password are valid, False otherwise.
    """
    with open(HTACCESS_FILE, 'r') as file:
        for line in file:
            if line.strip():
                valid_user, valid_pass = line.strip().split(':', 1)
                if username == valid_user and password == valid_pass:
                    return True
    return False

# No changes needed if the function is working correctly

if __name__ == '__main__':
    app.run(debug=True)
