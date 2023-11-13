"""
This module defines a FastAPI app that requires authentication using JWT tokens.
It defines a root endpoint that returns a message for authenticated users.
"""
import os
import logging
import bcrypt
import uvicorn
from passlib.apache import HtpasswdFile
from fastapi import FastAPI, Request, Form, Cookie, HTTPException, Depends, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .secrets import SECRET_KEY, HTACCESS_FILE, HASHING_ALGORITHM, JWT_HASHING_ALGORITHM
import hashlib

# Create a logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# Create FastAPI app
app = FastAPI()

# Security
security = HTTPBearer()

# Set APP_PORT from environment variable or default to 9111
APP_PORT = os.environ.get("APP_PORT", 9111)

def check_credentials(username: str, password: str):
    """
    Check if the given username and password are valid credentials.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    ht = HtpasswdFile(HTACCESS_FILE)
    if ht.check_password(username, password):
        logger.info(f"Credentials for user {username} are valid.")
        return True
    else:
        logger.info(f"Credentials for user {username} are invalid.")
        return False

# Create Jinja2Templates instance
templates = Jinja2Templates("./templates")

# Check if templates directory exists and create it if it doesn't
if not os.path.exists('templates'):
    os.makedirs('templates')

# Check if login.html exists and create it if it doesn't
login_html_path = os.path.join('templates', 'login.html')
if not os.path.exists(login_html_path):
    with open(login_html_path, 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f7f7; text-align: center; padding: 50px; }
        form { background-color: white; padding: 40px; border-radius: 10px; display: inline-block; }
        input { margin: 10px 0; padding: 10px; width: 200px; border-radius: 5px; border: 1px solid #ddd; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <h2>Login</h2>
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
""")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Returns the payload of a valid JWT token from the Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): The Authorization header credentials.

    Raises:
        HTTPException: If the token is invalid or the Authorization header is missing.

    Returns:
        The payload of the JWT token.
    """
    if credentials:
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[JWT_HASHING_ALGORITHM])
            logger.info(f"JWT token for user {payload['sub']} decoded.")
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="Authorization header missing")

@app.get("/")
async def root(request: Request):
    referrer_url = request.headers.get("referer")
    logger.info(f"Referrer URL: {referrer_url}")
    logger.info(f"Redirecting / request to /login")
    return RedirectResponse(url="/login")

@app.get("/auth")
@app.get("/login")
async def login_get(request: Request):
    referrer_url = request.headers.get("referer")
    logger.info(f"Referrer URL: {referrer_url}")
    logger.info(f"Looking for login.html in: {os.path.abspath('templates')}")
    # You can save this URL in a session variable or cookie as needed
    # Example: Save in a cookie
    response = templates.TemplateResponse("login.html", {"request": request})
    response.set_cookie(key="referrer_url", value=referrer_url)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth")
@app.post("/login")
async def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
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
        token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=JWT_HASHING_ALGORITHM)
        response.set_cookie(key="Authorization", value=f"Bearer {token}")
        original_url = request.cookies.get("original_url", "/")
        logger.debug(f"Credentials for user {username} are valid.")
        return RedirectResponse(url=original_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.debug(f"Failed to authenticate user {username}.")
        raise HTTPException(status_code=401, detail="Invalid credentials")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT, log_level="debug")
