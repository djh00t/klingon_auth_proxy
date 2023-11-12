
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

# Dummy user data - replace with your user validation logic
USERS = {"admin": "password123"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in the user by checking the credentials provided in the request form.
    If the credentials are valid, it generates a JWT token and sets it as a cookie in the response.
    If the credentials are invalid, it returns a 401 error.
    """
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            token = jwt.encode({'user': username}, SECRET_KEY, algorithm="HS256")
            resp = make_response(redirect('/'))
            resp.set_cookie('auth_token', token)
            return resp
        else:
            return 'Invalid credentials', 401

    return render_template('login.html')  # Create a login.html template

if __name__ == '__main__':
    app.run(debug=True, port=5000)
