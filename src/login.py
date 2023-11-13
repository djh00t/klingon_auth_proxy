"""
This module contains a FastAPI app that provides a login page and authentication functionality.
The app reads a username and password from a file and generates a JWT token if the credentials are valid.
The token is set as a cookie in the response and the user is redirected to the specified URL.
"""

# FILEPATH: src/login.py

import logging
from fastapi import FastAPI, Request, Form, Cookie, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from .secrets import SECRET_KEY, HTACCESS_FILE

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create FastAPI app
app = FastAPI()

# Initialize templates for FastAPI. If the templates directory doesn't exist,
# create it and add a default index.html file.
if not os.path.exists("./templates"):
    os.mkdir("./templates")
    with open("./templates/index.html", "w") as file:
        file.write("<h1>Hello world!</h1>")
templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Check user and password credentials
def check_credentials(username: str, password: str):
    """
    Check if the given username and password are valid credentials.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    with open(HTACCESS_FILE, 'r') as file:
        for line in file:
            if line.strip():
                valid_user, valid_pass = line.strip().split(':', 1)
                if username == valid_user and password == valid_pass:
                    return True
    return False

@app.get("/login")
async def login_get(request: Request):
    logger.info(f"Looking for login.html in: {os.path.abspath('templates')}")
    return templates.TemplateResponse("templates/login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...), url: str = Form('/')):
    """
    Authenticates user credentials and generates a JWT token if the credentials are valid.
    Sets the token as a cookie in the response and redirects to the specified URL.

    Args:
    - response (Response): The response object to set the cookie and redirect.
    - username (str): The username entered by the user.
    - password (str): The password entered by the user.
    - url (str): The URL to redirect to after successful authentication. Defaults to '/'.

    Returns:
    - response (Response): The response object with the token cookie set and redirected to the specified URL.

    Raises:
    - HTTPException: If the credentials are invalid.
    """
    if check_credentials(username, password):
        token = jwt.encode(
            {"user": username, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        response = RedirectResponse(url=url, status_code=303)
        response.set_cookie(key="auth_token", value=token, httponly=True, samesite='Lax')
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
