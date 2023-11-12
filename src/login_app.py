
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login process. It accepts both GET and POST requests.
    If the request is a POST request, it checks the credentials and creates a token if they are valid.
    If the credentials are invalid, it returns a 401 error.
    If the request is a GET request, it renders the login.html template.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_credentials(username, password):
            # Create a token and set it in a cookie
            token = jwt.encode(
                {'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                SECRET_KEY,
                algorithm="HS256"
            )
            resp = make_response(redirect('/'))
            resp.set_cookie('auth_token', token)
            return resp
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)