
"""
This module contains a Flask application that provides a login functionality. 
It uses JWT for authentication and authorization. 
The module defines a function to get or create a secret key, which is used to sign the JWT tokens. 
The module also defines a dummy user data for user validation. 
The login function handles GET and POST requests, and returns a response with a JWT token if the user is authenticated. 
"""
from flask import Flask, request, make_response, redirect, render_template
from datetime import datetime, timedelta, timezone
import jwt
import os
import secrets
from itsdangerous import json
import json

app = Flask(__name__)

# Constants
APP_PORT = os.environ.get("APP_PORT", 9111)
HTACCESS_FILE = os.environ.get("HTACCESS_FILE", "../secrets")

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
            # Debug
            print(f"Secret key read from {file_path}")
            return file.read().strip()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(32)
        with open(file_path, "w") as file:
            file.write(secret_key)
            # Debug
            print(f"Secret key written to {file_path}")
        return secret_key

# Variables
SECRET_KEY = get_or_create_secret_key(os.environ.get('SECRET_KEY_FILE', 'secret.key'))
"""
# SECRET_KEY
Generate SECRET_KEY if it doesn't exist otherwise read the file.
"""


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
        print(f"Contents of {HTACCESS_FILE}:")
        for line in file:
            print(line.strip())
            if line.strip():
                valid_user, valid_pass = line.strip().split(':', 1)
                if username == valid_user and password == valid_pass:
                    return True
    return False

@app.route('/', methods=['GET'])
def root():
    return redirect('/login', code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login process for the user. It checks if the user is already authenticated, 
    if not, it checks the user's credentials and generates a JWT token which is then stored in a cookie.
    """
    # Get the original URL from the query parameter
    original_url = request.args.get('url', '/')

    # Redirect to the original URL if the user is already authenticated
    if request.cookies.get('auth_token'):

        # Decode the auth token
        try:
            jwt.decode(request.cookies.get('auth_token'), SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            # Redirect to login page if the token has expired
            return redirect(url_for('login', url=original_url))
        else:
            # Redirect to the original URL if the token is valid
            return redirect(original_url)
           
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_credentials(username, password):
            token = jwt.encode(
                {'user': username, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
                SECRET_KEY,
                algorithm="HS256"
            )
            resp = make_response(redirect(original_url))  # Redirect to the original URL
            resp.set_cookie('auth_token', token, httponly=True, samesite='Lax')
            return resp
        else:
            return render_template('login.html', error="Invalid credentials", original_url=original_url), 401

    return render_template('login.html', original_url=original_url)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, extra_files=[HTACCESS_FILE], port=APP_PORT)